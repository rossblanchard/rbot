
# RUNBOOK__rbot_office_phase1_master__v1.0

## 1. Document Metadata
- **Status:** Active / Production
- **Owner:** Ross Blanchard
- **Date:** 2026-03-17
- **Purpose:** The definitive, copy-paste rebuild guide for the `rbot-office` Phase 1 architecture. Contains the final, stable, tab-indented source code for the Master Orchestrator and all four autonomous tools.

## 2. Environment Setup

### 2.1 Scaffold & Dependencies
```bash
mkdir -p ~/services/rbot-office/personas
mkdir -p ~/services/rbot-office/tools
cd ~/services/rbot-office

python3 -m venv venv
source venv/bin/activate

# Install all required Phase 1 dependencies
pip install slack_bolt python-dotenv google-genai requests google-api-python-client google-auth-httplib2 google-auth-oauthlib ddgs

touch tools/__init__.py
```

### 2.2 Secrets (`.env`)
Create `.env` and populate with zero trailing spaces:
```text
SLACK_APP_TOKEN=xapp-...
SLACK_BOT_TOKEN=xoxb-...
ADMIN_SLACK_ID=U...
GEMINI_API_KEY=AIzaSy...
ANYTHINGLLM_API_KEY=YOUR-KEY
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-secret
GOOGLE_REFRESH_TOKEN=1//your-refresh-token
ROSS_BRAIN_FOLDER_ID=your-folder-id
```

---

## 3. Tool Scripts (`/tools`)
*All Python files utilize strict Tab indentation and verbose educational commenting.*

### 3.1 RAG Writer (`tools/memory.py`)
```python
"""
FILE: memory.py
PURPOSE: Uploads text to AnythingLLM and embeds it into a specific workspace.
"""
import os
import requests

def commit_to_rag(title: str, content: str, workspace_slug: str) -> str:
	api_key = os.getenv("ANYTHINGLLM_API_KEY")
	base_url = "http://localhost:3001/api/v1"
	
	headers = {
		"Authorization": f"Bearer {api_key}",
		"Content-Type": "application/json"
	}

	try:
		# Step 1: Upload the raw text
		upload_payload = {"textContent": content, "metadata": {"title": title}}
		upload_res = requests.post(f"{base_url}/document/raw-text", headers=headers, json=upload_payload)
		upload_res.raise_for_status()
		
		doc_location = upload_res.json().get("documents", [{}])[0].get("location")
		if not doc_location:
			return "Error: Document uploaded, but failed to retrieve storage location."

		# Step 2: Embed into the workspace
		embed_payload = {"adds": [doc_location], "deletes":[]}
		embed_res = requests.post(f"{base_url}/workspace/{workspace_slug}/update-embeddings", headers=headers, json=embed_payload)
		embed_res.raise_for_status()

		return f"Success: Memory '{title}' has been successfully embedded into the '{workspace_slug}' database."

	except Exception as e:
		return f"Failed to commit to RAG: {str(e)}"
```

### 3.2 RAG Reader (`tools/memory_search.py`)
```python
"""
FILE: memory_search.py
PURPOSE: Queries the AnythingLLM vector database for relevant information.
"""
import os
import requests

def search_rag(query: str, workspace_slug: str) -> str:
	api_key = os.getenv("ANYTHINGLLM_API_KEY")
	base_url = "http://localhost:3001/api/v1"
	
	headers = {
		"Authorization": f"Bearer {api_key}",
		"Content-Type": "application/json"
	}

	try:
		payload = {"message": query, "mode": "chat"}
		res = requests.post(f"{base_url}/workspace/{workspace_slug}/chat", headers=headers, json=payload)
		res.raise_for_status()
		
		data = res.json()
		text_response = data.get("textResponse", "")
		sources = data.get("sources",[])
		source_names = list(set([src.get("title", "Unknown Document") for src in sources]))
		
		if not text_response:
			return "No relevant information found in the database."
			
		return f"Database Response: {text_response}\n\nSources Found: {', '.join(source_names)}"

	except Exception as e:
		return f"Failed to search RAG: {str(e)}"
```

### 3.3 Google Drive Writer (`tools/gdrive_writer.py`)
```python
"""
FILE: gdrive_writer.py
PURPOSE: Authenticates via headless OAuth and streams files to Google Drive.
"""
import os
import io
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

def save_to_drive(title: str, content: str) -> str:
	client_id = os.getenv("GOOGLE_CLIENT_ID")
	client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
	refresh_token = os.getenv("GOOGLE_REFRESH_TOKEN")
	folder_id = os.getenv("ROSS_BRAIN_FOLDER_ID")

	if not all([client_id, client_secret, refresh_token, folder_id]):
		return "Error: Missing Google Drive credentials in the .env file."

	try:
		creds = Credentials(
			token=None,
			refresh_token=refresh_token,
			client_id=client_id,
			client_secret=client_secret,
			token_uri="https://oauth2.googleapis.com/token"
		)

		service = build('drive', 'v3', credentials=creds)

		file_metadata = {'name': title, 'parents': [folder_id]}
		
		# Stream string from memory to prevent SD card writes
		file_buffer = io.BytesIO(content.encode('utf-8'))
		media = MediaIoBaseUpload(file_buffer, mimetype='text/markdown', resumable=True)

		file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
		return f"Success: File '{title}' saved to Google Drive folder (ID: {file.get('id')})."

	except Exception as e:
		return f"Failed to write to Google Drive: {str(e)}"
```

### 3.4 Web Search (`tools/web_search.py`)
```python
"""
FILE: web_search.py
PURPOSE: Scrapes the live internet via DuckDuckGo (ddgs).
"""
from ddgs import DDGS

def search_web(query: str) -> str:
	try:
		ddgs = DDGS()
		results = list(ddgs.text(query, max_results=5))
		
		if not results:
			return f"No web search results found for: '{query}'"
			
		formatted_results = f"Web Search Results for '{query}':\n\n"
		for i, res in enumerate(results, 1):
			title = res.get('title', 'No Title')
			link = res.get('href', 'No URL')
			snippet = res.get('body', 'No snippet available.')
			formatted_results += f"{i}. {title}\nURL: {link}\nSnippet: {snippet}\n\n"
			
		return formatted_results

	except Exception as e:
		return f"Failed to search the web: {str(e)}"
```

---

## 4. Master Orchestrator (`app.py`)

```python
"""
FILE: app.py
PURPOSE: The Master Orchestrator for the rbot-office Slack Swarm. 
"""
import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from google import genai
from google.genai import types

from tools.memory import commit_to_rag
from tools.memory_search import search_rag
from tools.gdrive_writer import save_to_drive
from tools.web_search import search_web

# 1. INITIALIZATION & CONFIGURATION
load_dotenv()
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
ADMIN_ID = os.environ.get("ADMIN_SLACK_ID")

def get_persona_prompt(persona_name):
	filepath = f"personas/{persona_name}.md"
	if os.path.exists(filepath):
		with open(filepath, "r") as f:
			return f.read().strip()
	return "You are a helpful AI assistant operating in Slack."

# 2. DEFINE GEMINI TOOLS
rag_commit_tool = types.FunctionDeclaration(
	name="commit_to_rag",
	description="Saves a reflective summary or architectural decision to the permanent RAG database.",
	parameters=types.Schema(
		type=types.Type.OBJECT,
		properties={
			"title": types.Schema(type=types.Type.STRING, description="The filename, ending in .md"),
			"content": types.Schema(type=types.Type.STRING, description="The dense markdown content to save.")
		},
		required=["title", "content"]
	)
)

rag_search_tool = types.FunctionDeclaration(
	name="search_rag",
	description="Searches the permanent RAG database for past memories, technical specs, and previous decisions.",
	parameters=types.Schema(
		type=types.Type.OBJECT,
		properties={
			"query": types.Schema(type=types.Type.STRING, description="The search query or question to ask the database.")
		},
		required=["query"]
	)
)

gdrive_tool = types.FunctionDeclaration(
	name="save_to_drive",
	description="Saves finalized canonical documents, architecture specs, or runbooks directly to the RossBrain Google Drive folder.",
	parameters=types.Schema(
		type=types.Type.OBJECT,
		properties={
			"title": types.Schema(type=types.Type.STRING, description="The filename, ending in .md"),
			"content": types.Schema(type=types.Type.STRING, description="The dense markdown content to save.")
		},
		required=["title", "content"]
	)
)

web_search_tool = types.FunctionDeclaration(
	name="search_web",
	description="Searches the live internet for up-to-date information, documentation, news, or current events.",
	parameters=types.Schema(
		type=types.Type.OBJECT,
		properties={
			"query": types.Schema(type=types.Type.STRING, description="The search query to look up on the internet.")
		},
		required=["query"]
	)
)

gemini_tools = types.Tool(function_declarations=[rag_commit_tool, rag_search_tool, gdrive_tool, web_search_tool])

# 3. SLACK EVENT LISTENER
@app.event("app_mention")
def handle_mentions(event, say):
	user_id = event["user"]
	channel_id = event["channel"]
	raw_text = event["text"]
	
	# RBAC Security Check
	if user_id != ADMIN_ID:
		say(f"I'm sorry, <@{user_id}>. I'm afraid I can't do that. This mission is too important for me to allow you to jeopardize it. (Admin access required).")
		return

	thread_ts = event.get("thread_ts", event["ts"])

	try:
		# Clean input and Route Persona
		bot_user_id = app.client.auth_test()["user_id"]
		clean_text = raw_text.replace(f"<@{bot_user_id}>", "").strip()

		first_word = clean_text.split(" ")[0].lower().strip(":,.-")
		available_personas = ["archie", "qa", "pm"]
		
		if first_word in available_personas:
			current_persona = first_word
			clean_text = clean_text[len(first_word):].strip(":,.- ")
		else:
			current_persona = "archie"

		workspace_map = {"archie": "my-workspace", "qa": "qa", "pm": "pm"}
		target_workspace = workspace_map.get(current_persona, "archie")
		system_prompt = get_persona_prompt(current_persona)

		# Fetch the Thread History
		history_response = app.client.conversations_replies(channel=channel_id, ts=thread_ts)
		messages = history_response["messages"]

		contents =[]
		for msg in messages:
			text = msg.get("text", "").replace(f"<@{bot_user_id}>", "").strip()
			if not text: continue

			is_assistant = msg.get("user") == bot_user_id
			if not is_assistant:
				history_first_word = text.split(" ")[0].lower().strip(":,.-*")
				if history_first_word in available_personas:
					text = text[len(history_first_word):].strip(":,.-* ")
				contents.append(types.Content(role="user", parts=[types.Part.from_text(text=f"[Ross]: {text}")]))
			else:
				speaker = "archie"
				if text.startswith("*"):
					possible_speaker = text.split("*")[1].lower()
					if possible_speaker in available_personas: speaker = possible_speaker

				if speaker == current_persona:
					contents.append(types.Content(role="model", parts=[types.Part.from_text(text=text)]))
				else:
					contents.append(types.Content(role="user", parts=[types.Part.from_text(text=f"[Agent {speaker.capitalize()}]: {text}")]))

		# Context Compression
		compressed_contents =[]
		for c in contents:
			if compressed_contents and compressed_contents[-1].role == c.role:
				compressed_contents[-1].parts[0].text += f"\n\n{c.parts[0].text}"
			else:
				compressed_contents.append(c)

		# 4. EXECUTE GEMINI API
		config = types.GenerateContentConfig(
			system_instruction=system_prompt,
			tools=[gemini_tools],
			temperature=0.7
		)

		response = client.models.generate_content(
			model='gemini-2.5-pro',
			contents=compressed_contents,
			config=config
		)
		
		# 5. MULTI-STEP TOOL EXECUTION LOOP
		loop_count = 0
		while response.function_calls and loop_count < 3:
			function_call = response.function_calls[0]
			args = function_call.args
			
			if function_call.name == "commit_to_rag":
				say(text=f"*{current_persona.capitalize()}:* 💾 _Committing `{args.get('title', 'memory.md')}` to the `{target_workspace}` RAG database..._", thread_ts=thread_ts)
				tool_result = commit_to_rag(args.get("title", "memory.md"), args.get("content", ""), target_workspace)
				
			elif function_call.name == "search_rag":
				say(text=f"*{current_persona.capitalize()}:* 🔍 _Searching the `{target_workspace}` RAG database for: '{args.get('query', '')}'..._", thread_ts=thread_ts)
				tool_result = search_rag(args.get("query", ""), target_workspace)
				
			elif function_call.name == "save_to_drive":
				say(text=f"*{current_persona.capitalize()}:* ☁️ _Uploading `{args.get('title', 'file.md')}` securely to Google Drive..._", thread_ts=thread_ts)
				tool_result = save_to_drive(args.get("title", "file.md"), args.get("content", ""))
				
			elif function_call.name == "search_web":
				say(text=f"*{current_persona.capitalize()}:* 🌐 _Searching the live web for: '{args.get('query', '')}'..._", thread_ts=thread_ts)
				tool_result = search_web(args.get("query", ""))
				
			else:
				tool_result = "Error: Unknown tool called."

			# Feed tool result back to Gemini
			compressed_contents.append(response.candidates[0].content)
			compressed_contents.append(
				types.Content(role="user", parts=[
					types.Part.from_function_response(name=function_call.name, response={"result": tool_result})
				])
			)
			
			response = client.models.generate_content(
				model='gemini-2.5-pro',
				contents=compressed_contents,
				config=config
			)
			
			loop_count += 1

		# 6. FINAL DISPATCH TO SLACK
		if getattr(response, "candidates", None) and "MALFORMED" in str(response.candidates[0].finish_reason):
			reply = "⚠️ _[The cognitive engine suffered an internal JSON hallucination and aborted the response. Please try again in a new thread.]_"
		else:
			reply = response.text if getattr(response, "text", None) else "_[Action executed successfully. No additional text provided by the cognitive engine.]_"
		
		prefix = f"*{current_persona.capitalize()}:* "
		say(text=prefix + reply, thread_ts=thread_ts)
		
	except Exception as e:
		say(text=f"⚠️ *System Error:* Failed to process context. Details: `{str(e)}`", thread_ts=thread_ts)

if __name__ == "__main__":
	print("Starting rbot-office Brain (Stable Gemini 2.5 Pro + 4 Tools)... Waiting for Slack connection.")
	SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()
```
