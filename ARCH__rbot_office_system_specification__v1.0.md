# ARCH__rbot_office_system_specification__v1.0

## 1. System Overview
**System Name:** `rbot-office`
**Description:** A headless, Python-based multi-agent orchestration service. It bridges omnichannel interfaces (Slack) with a central RAG vector database (AnythingLLM) and external APIs (Google Drive), enabling autonomous tool execution, persistent reflective memory, and strict persona segregation.
**Date:** 2026-03-15
**Architect:** Archie / Ross

## 2. Core Architectural Principles
- **Decoupled Memory:** AnythingLLM acts strictly as the central vector database and document manager. `rbot-office` acts as the compute and orchestration layer.
- **Declarative Configuration:** AI models, API keys, and routing logic are strictly separated from Python execution code via `.env` and `.yaml` files.
- **File-Based Personas:** Agent identities and system prompts are maintained in plain-text markdown files for immediate hot-swapping without code deployment.
- **Omnichannel Consistency:** Reflective summaries generated in Slack are pushed to AnythingLLM via REST API, ensuring memory persists across all front-end interfaces.

## 3. Directory Structure
The application will be deployed as a Dockerized Python environment on the Raspberry Pi host.

```text
/home/ross/services/rbot-office/
├── docker-compose.yml       # Container definition
├── Dockerfile               # Python environment build
├── requirements.txt         # Dependencies (slack_bolt, google-api-python-client, requests)
├── .env                     # SECRETS: Slack tokens, OpenAI/Anthropic keys, AnythingLLM API key
├── config.yaml              # Declarative routing mapping (Persona -> Model -> Workspace ID)
├── app.py                   # Core execution loop and Slack Socket Mode listener
├── /personas/               # Markdown files defining system prompts
│   ├── archie.md
│   ├── qa_engineer.md
│   └── project_manager.md
└── /tools/                  # Modular Python functions
    ├── memory_commit.py     # Pushes documents to AnythingLLM API
    ├── memory_search.py     # Queries AnythingLLM API
    └── gdrive_writer.py     # Authenticates and writes to specific Google Drive folder ID
```

## 4. Component Specifications

### 4.1 Configuration Layer (`config.yaml`)
Maps Slack triggers to specific models and AnythingLLM workspace segregations.
```yaml
personas:
  archie:
    trigger: "@archie"
    prompt_file: "personas/archie.md"
    model: "gemini-1.5-pro"
    workspace_slug: "archie-brain"
    tools:["memory_commit", "memory_search", "gdrive_writer"]
  qa:
    trigger: "@qa"
    prompt_file: "personas/qa_engineer.md"
    model: "claude-3-5-sonnet"
    workspace_slug: "qa-memory"
    tools: ["memory_search"]
```

### 4.2 The Orchestration Loop (`app.py`)
1. **Listen:** Slack Bolt (Socket Mode) intercepts `@archie` mention in a thread.
2. **Contextualize:** Application reads `config.yaml`, loads `archie.md`, and retrieves the last 10 messages in the Slack thread.
3. **Execute:** Payload is sent to the LLM API.
4. **Tool Routing:** If the LLM invokes `memory_commit`, `app.py` halts, runs `tools/memory_commit.py`, appends the success state, and re-prompts the LLM.
5. **Respond:** Final string is dispatched back to the Slack thread.

### 4.3 Reflective Memory Pipeline (`memory_commit.py`)
- **Trigger:** Human requests a summary, or the persona decides a milestone is reached.
- **Action:** LLM generates a dense markdown summary.
- **API Call:** `POST https://rbot.rossblanchard.com/api/v1/document/create`
- **Result:** The document is instantly embedded into the specific workspace's vector database, available for immediate recall in both Slack and the AnythingLLM Web UI.

### 4.4 Google Drive Pipeline (`gdrive_writer.py`)
- **Authentication:** Official `google-api-python-client` using Service Account or OAuth tokens.
- **Constraint:** Hardcoded `PARENT_FOLDER_ID` restricts write access exclusively to the `RossBrain` directory.
- **Action:** Generates canonical markdown or Google Docs based on conversational output.

## 5. Deployment Constraints
- Runs in a peered Docker network alongside the `rbot` (AnythingLLM) container to allow secure, local HTTP API calls without routing out to the public internet.
- Slack connection utilizes outbound WebSockets (Socket Mode) to bypass Cloudflare Zero Trust inbound restrictions.

## 6. Status
- **Phase:** Design Approved. Ready for Implementation.
- **Next Milestone:** Scaffold directory structure and implement `app.py` Slack Socket Mode listener.
