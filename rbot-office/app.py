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

# 2. Define the Gemini Tool
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

        # 6. Compress consecutive roles (Gemini requires strict user->model alternation)
        compressed_contents =[]
        for c in contents:
            if compressed_contents and compressed_contents[-1].role == c.role:
                compressed_contents[-1].parts[0].text += f"\n\n{c.parts[0].text}"
            else:
                compressed_contents.append(c)

        # 7. Call Gemini
        config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[rag_tool],
            temperature=0.7
        )

        response = client.models.generate_content(
            model='gemini-3.1-pro-preview', # Change this string if you want a specific experimental preview version!
            contents=compressed_contents,
            config=config
        )
        
        # 8. Check for Tool Calls
        if response.function_calls:
            function_call = response.function_calls[0]
            if function_call.name == "commit_to_rag":
                args = function_call.args
                say(text=f"*{current_persona.capitalize()}:* 💾 _Committing `{args['title']}` to the `{target_workspace}` RAG database..._", thread_ts=thread_ts)
                
                tool_result = commit_to_rag(args["title"], args["content"], target_workspace)
                
                compressed_contents.append(response.candidates[0].content)
                compressed_contents.append(
                    types.Content(role="user", parts=[
                        types.Part.from_function_response(name="commit_to_rag", response={"result": tool_result})
                    ])
                )
                
                response = client.models.generate_content(
                    model='gemini-3.1-pro-preview',
                    contents=compressed_contents,
                    config=config
                )

        # 9. Final Dispatch
        reply = response.text if response.text else "_[Action executed successfully. No additional text provided by the cognitive engine.]_"
        prefix = f"*{current_persona.capitalize()}:* "
        say(text=prefix + reply, thread_ts=thread_ts)
        
    except Exception as e:
        say(text=f"⚠️ *System Error:* Failed to process context. Details: `{str(e)}`", thread_ts=thread_ts)

if __name__ == "__main__":
    print("Starting rbot-office Brain (Gemini Edition)... Waiting for Slack connection.")
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()
