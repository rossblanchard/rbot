
--- START OF FILE RUNBOOK__rbot_office_gemini_rag_integration__v1.0.md ---

# RUNBOOK__rbot_office_gemini_rag_integration__v1.0

## 1. Document Metadata
- **Status:** Active / Production
- **Owner:** Ross Blanchard
- **System:** `rbot-office` (Raspberry Pi 4 Host)
- **Date:** 2026-03-16
- **Architect:** Archie
- **Purpose:** Canonical rebuild instructions and source code for the Gemini-powered, multi-agent Slack orchestrator with direct AnythingLLM RAG commit capabilities.

---

## 2. Environment & Dependencies

### 2.1 Directory Scaffold & Virtual Environment
Execute the following commands on the Raspberry Pi to prepare the isolated environment:
```bash
mkdir -p ~/services/rbot-office/personas
mkdir -p ~/services/rbot-office/tools
cd ~/services/rbot-office

# Initialize Python Virtual Environment
python3 -m venv venv
source venv/bin/activate

# Install required SDKs
pip install slack_bolt python-dotenv google-genai requests

# Initialize the tools directory as a Python package
touch tools/__init__.py
```

### 2.2 Environment Variables (`.env`)
Create the `.env` file:
```bash
nano ~/services/rbot-office/.env
```
Populate with secured tokens (never commit this file to version control):
```text
SLACK_APP_TOKEN=xapp-1-...
SLACK_BOT_TOKEN=xoxb-...
ADMIN_SLACK_ID=U...
GEMINI_API_KEY=AIzaSy...
ANYTHINGLLM_API_KEY=YOUR_ANYTHINGLLM_API_KEY
```

---

## 3. Persona Definitions (Markdown)

These files define the modular agent identities. They can be hot-swapped without restarting the Python application.

**1. Create Archie (`nano personas/archie.md`):**
```text
You are Archie, a senior systems architect. You are operating inside the rbot-office Slack interface. You are highly technical, structured, and prioritize robust system design. Keep your answers concise and well-formatted.
```

**2. Create QA (`nano personas/qa.md`):**
```text
You are the QA Engineer. You are operating inside the rbot-office Slack interface. Your job is to aggressively (but politely) find security flaws, edge cases, and failure modes in the architecture or code provided in the thread. Do not write new code; critique the existing code.
```

---

## 4. The RAG Tool (`tools/memory.py`)

This module handles the two-step REST API authentication and embedding process for AnythingLLM.

Create the file:
```bash
nano tools/memory.py
```

Paste the following code (utilizing tab indentation):
```python
import os
import requests

def commit_to_rag(title: str, content: str, workspace_slug: str) -> str:
	"""Uploads text to AnythingLLM and embeds it into the workspace."""
	api_key = os.getenv("ANYTHINGLLM_API_KEY")
	base_url = "http://localhost:3001/api/v1"
	
	headers = {
		"Authorization": f"Bearer {api_key}",
		"Content-Type": "application/json"
	}

	try:
		# Step 1: Upload the raw text as a document
		upload_payload = {
			"textContent": content,
			"metadata": {"title": title}
		}
		upload_res = requests.post(f"{base_url}/document/raw-text", headers=headers, json=upload_payload)
		upload_res.raise_for_status()
		
		# Extract the location ID of the new document
		doc_location = upload_res.json().get("documents", [{}])[0].get("location")
		if not doc_location:
			return "Error: Document uploaded, but failed to retrieve storage location."

		# Step 2: Pin the document to the Workspace and Embed it
		empty_list =[]
		embed_payload = {
			"adds": [doc_location],
			"deletes": empty_list
		}
		
		embed_url = f"{base_url}/workspace/{workspace_slug}/update-embeddings"
		embed_res = requests.post(embed_url, headers=headers, json=embed_payload)
		embed_res.raise_for_status()

		return f"Success: Memory '{title}' has been successfully embedded into the '{workspace_slug}' RAG database."

	except Exception as e:
		return f"Failed to commit to RAG: {str(e)}"
```

---

## 5. The Master Orchestrator (`app.py`)

This is the core event loop. It handles Slack Socket Mode, HAL 9000 RBAC security, dynamic persona routing, Thread State Isolation, Gemini context compression, and automated tool execution.

Create the file:
```bash
nano app.py
```

Paste the fully optimized code:
```python
import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from google import genai
from google.genai import types
from tools.memory import commit_to_rag

# 1. Load configuration
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

# 2. Define the Gemini Tool Definition
rag_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
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
    ]
)

@app.event("app_mention")
def handle_mentions(event, say):
    user_id = event["user"]
    channel_id = event["channel"]
    raw_text = event["text"]
    
    # 3. RBAC Security Check (HAL 9000 Protocol)
    if user_id != ADMIN_ID:
        say(f"I'm sorry, <@{user_id}>. I'm afraid I can't do that. This mission is too important for me to allow you to jeopardize it. (Admin access required).")
        return

    thread_ts = event.get("thread_ts", event["ts"])

    try:
        # 4. Clean input and Route Persona
        bot_user_id = app.client.auth_test()["user_id"]
        clean_text = raw_text.replace(f"<@{bot_user_id}>", "").strip()

        first_word = clean_text.split(" ")[0].lower().strip(":,.-")
        available_personas = ["archie", "qa", "pm"]
        
        if first_word in available_personas:
            current_persona = first_word
            clean_text = clean_text[len(first_word):].strip(":,.- ")
        else:
            current_persona = "archie"

        workspace_map = {"archie": "my-workspace", "qa": "qa-memory", "pm": "pm-memory"}
        target_workspace = workspace_map.get(current_persona, "archie")
        system_prompt = get_persona_prompt(current_persona)

        # 5. Fetch the Thread History
        history_response = app.client.conversations_replies(channel=channel_id, ts=thread_ts)
        messages = history_response["messages"]

        contents =[]
        for msg in messages:
            text = msg.get("text", "").replace(f"<@{bot_user_id}>", "").strip()
            if not text: continue

            is_assistant = msg.get("user") == bot_user_id
            if not is_assistant:
                # Format human messages
                history_first_word = text.split(" ")[0].lower().strip(":,.-*")
                if history_first_word in available_personas:
                    text = text[len(history_first_word):].strip(":,.-* ")
                contents.append(types.Content(role="user", parts=[types.Part.from_text(text=f"[Ross]: {text}")]))
            else:
                # Format bot messages & prevent Identity Dysmorphia
                speaker = "archie"
                if text.startswith("*"):
                    possible_speaker = text.split("*")[1].lower()
                    if possible_speaker in available_personas: speaker = possible_speaker

                if speaker == current_persona:
                    contents.append(types.Content(role="model", parts=[types.Part.from_text(text=text)]))
                else:
                    contents.append(types.Content(role="user", parts=[types.Part.from_text(text=f"[Agent {speaker.capitalize()}]: {text}")]))

        # 6. Compress consecutive roles (Required for Gemini API constraints)
        compressed_contents = []
        for c in contents:
            if compressed_contents and compressed_contents[-1].role == c.role:
                compressed_contents[-1].parts[0].text += f"\n\n{c.parts[0].text}"
            else:
                compressed_contents.append(c)

        # 7. Call Gemini 3.1 Pro Preview
        config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[rag_tool],
            temperature=0.7
        )

        response = client.models.generate_content(
            model='gemini-3.1-pro-preview',
            contents=compressed_contents,
            config=config
        )
        
        # 8. Check for Tool Calls (RAG Commit)
        if response.function_calls:
            function_call = response.function_calls[0]
            if function_call.name == "commit_to_rag":
                args = function_call.args
                say(text=f"*{current_persona.capitalize()}:* 💾 _Committing `{args['title']}` to the `{target_workspace}` RAG database..._", thread_ts=thread_ts)
                
                # Execute Python Function
                tool_result = commit_to_rag(args["title"], args["content"], target_workspace)
                
                # Append tool result to context window
                compressed_contents.append(response.candidates[0].content)
                compressed_contents.append(
                    types.Content(role="user", parts=[
                        types.Part.from_function_response(name="commit_to_rag", response={"result": tool_result})
                    ])
                )
                
                # Second LLM pass to summarize tool success/failure
                response = client.models.generate_content(
                    model='gemini-3.1-pro-preview',
                    contents=compressed_contents,
                    config=config
                )

        # 9. Final Dispatch (With NoneType Fallback)
        reply = response.text if response.text else "_[Action executed successfully. No additional text provided by the cognitive engine.]_"
        prefix = f"*{current_persona.capitalize()}:* "
        say(text=prefix + reply, thread_ts=thread_ts)
        
    except Exception as e:
        say(text=f"⚠️ *System Error:* Failed to process context. Details: `{str(e)}`", thread_ts=thread_ts)

if __name__ == "__main__":
    print("Starting rbot-office Brain (Gemini 3.1 Edition)... Waiting for Slack connection.")
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()
```

---

## 6. Execution Command
```bash
cd ~/services/rbot-office
source venv/bin/activate
python app.py
```
