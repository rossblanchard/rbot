
# RUNBOOK__rbot_office_slack_openai_integration__v1.0

## 1. Document Metadata
- **Status:** Active / Verified
- **Owner:** Ross Blanchard
- **System:** Raspberry Pi 4 (rbot host) / Python Virtual Environment
- **Date:** 2026-03-15
- **Architect:** Archie
- **Purpose:** Documents the initial scaffolding, Slack Socket Mode configuration, Role-Based Access Control (RBAC), and OpenAI LLM integration for the `rbot-office` headless orchestration engine.

## 2. Prerequisites
- SSH access to the Raspberry Pi host.
- Administrative access to a Slack Workspace.
- An active OpenAI API Key (or Gemini/Anthropic key for future migration).

---

## 3. Slack Application Configuration

### 3.1 App Creation & Socket Mode
1. Navigate to the [Slack API Apps page](https://api.slack.com/apps).
2. Click **Create New App** -> **From scratch**.
3. Name the app `rbot-office` and select the target Slack workspace.
4. In the left navigation menu, select **Socket Mode**.
5. Toggle **Enable Socket Mode** to **On**.
6. Generate an App Token named `rbot-socket`. 
7. **Store Locally:** Copy the resulting token (`xapp-...`).

### 3.2 Permissions & Bot Token
1. In the left navigation menu, select **OAuth & Permissions**.
2. Scroll to **Scopes** -> **Bot Token Scopes** and add the following:
   - `app_mentions:read` (Required to detect `@rbot-office` tags).
   - `chat:write` (Required to send messages).
   - `channels:history` (Required to read thread context).
3. Scroll to the top of the page and click **Install to Workspace** (Approve the prompt).
4. **Store Locally:** Copy the Bot User OAuth Token (`xoxb-...`).

### 3.3 Event Subscriptions (The Data Pipe)
1. In the left navigation menu, select **Event Subscriptions**.
2. Toggle **Enable Events** to **On**.
3. Scroll to **Subscribe to bot events** -> click **Add Bot User Event**.
4. Add the `app_mention` event.
5. **CRITICAL:** Click the **Save Changes** button at the bottom of the screen.
6. Scroll to the top of the page and click the prompt to **Reinstall your app** to apply the new event rules.

### 3.4 Acquire Admin Slack ID (RBAC Security)
1. Open the Slack desktop or web client.
2. Click your user profile picture -> **Profile**.
3. Click the **More (Three Dots)** icon -> **Copy member ID**.
4. **Store Locally:** Copy the ID (`U...` or `W...`).

---

## 4. Host Environment Setup (Raspberry Pi)

### 4.1 Project Directory & Secrets
Execute via SSH on the Raspberry Pi:

```bash
# Create project directory
mkdir -p ~/services/rbot-office
cd ~/services/rbot-office

# Create the environment variables file
nano .env
```

Populate the `.env` file with the secured tokens:
```text
SLACK_APP_TOKEN=xapp-your-app-token-here
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
ADMIN_SLACK_ID=Uyour-member-id-here
OPENAI_API_KEY=sk-your-openai-api-key-here
```
*(Save and exit: `CTRL+O`, `Enter`, `CTRL+X`)*

### 4.2 Python Virtual Environment & Dependencies
Isolate the application dependencies from the global Pi OS environment.

```bash
# Initialize virtual environment
python3 -m venv venv

# Activate the environment
source venv/bin/activate

# Install required packages
pip install slack_bolt python-dotenv openai
```

---

## 5. Application Code Integration

Create the core execution script:
```bash
nano app.py
```

Inject the following Python architecture:
```python
import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from openai import OpenAI

# 1. Load configuration and initialize clients
load_dotenv()
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
ADMIN_ID = os.environ.get("ADMIN_SLACK_ID")

# 2. Define the Slack Event Listener
@app.event("app_mention")
def handle_mentions(event, say):
    user_id = event["user"]
    raw_text = event["text"]
    
    # 3. RBAC Security Gateway
    if user_id != ADMIN_ID:
        say(f"Sorry <@{user_id}>, my higher-level cognitive functions are locked to Admin access only.")
        return

    # 4. Input Sanitization (Strip the @bot tag)
    clean_text = raw_text.split(">", 1)[1].strip() if ">" in raw_text else raw_text

    # 5. LLM API Execution (The Brain)
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are Archie, a senior systems architect. You are currently operating inside the rbot-office Slack interface. Keep your answers concise, professional, and formatted well for Slack."},
                {"role": "user", "content": clean_text}
            ]
        )
        
        # 6. Output Dispatch
        reply = response.choices[0].message.content
        say(reply)
        
    except Exception as e:
        say(f"⚠️ *System Error:* Failed to connect to the cognitive engine. Details: `{str(e)}`")

# 7. Socket Mode Initialization
if __name__ == "__main__":
    print("Starting rbot-office Brain... Waiting for Slack connection.")
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()
```
*(Save and exit: `CTRL+O`, `Enter`, `CTRL+X`)*

---

## 6. Execution and Verification

### 6.1 Boot the Application
Ensure the virtual environment is active (`source venv/bin/activate`), then run:
```bash
python app.py
```
*Expected Output: `Starting rbot-office Brain... Waiting for Slack connection.`*

### 6.2 Slack Verification
1. Open the Slack application.
2. Navigate to a test channel and invite the bot (`@rbot-office`).
3. Issue a prompt: `@rbot-office What is the architectural advantage of using Slack Socket Mode?`

**Success Criteria:**
- The bot replies with an LLM-generated response.
- Unauthorized users receive the RBAC lockout message.
- The Cloudflare Tunnel is successfully bypassed via outbound WebSockets.

