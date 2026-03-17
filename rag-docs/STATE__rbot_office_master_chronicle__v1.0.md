

# STATE__rbot_office_master_chronicle__v1.0

## 1. Document Metadata
- **Status:** Master State Transfer (Comprehensive)
- **Date:** Tuesday, March 17, 2026
- **Architects:** Ross Blanchard, Archie (AI)
- **Author:** Archie (AI)
- **Purpose:** A complete historical chronicle of the design, debugging, and architectural evolution of the `rbot-office` multi-agent swarm. This document preserves both the technical state and the conversational context/rationale of the founding sessions. This session was conducted in Google AI Studio Playground using Gemini 3.1 Pro Preview and Archie's standard system prompt as of March 16, 2026.

## 2. The Architectural Journey & Paths Not Taken

During the initial design phase, several architectures were explored and explicitly rejected by Ross and Archie. These must not be attempted again without addressing their fundamental flaws:

### 2.1 The `rclone` FUSE Mount Trap (Rejected)
- **Initial Idea:** Use `rclone` to mount Google Drive directly to the Raspberry Pi host and map it into the AnythingLLM Docker container.
- **The Failure:** FUSE mounts over network connections are brittle. When the network dropped, the Docker container's I/O locked up. This caused AnythingLLM to lose access to `anythingllm.db`, resulting in silent database wipes, salt mismatches, and login lockouts.
- **The Lesson:** Never mount network drives directly into SQLite-backed Docker containers. We resolved this by hardcoding the AnythingLLM volume to `name: rbot_storage` to prevent Docker Compose prefix-guessing errors.

### 2.2 The Webhook / `n8n` Pivot (Rejected)
- **Initial Idea:** Use `n8n` (visual orchestrator) or FastAPI webhooks to connect Slack to the AI.
- **The Blocker:** Ross's infrastructure is secured by Cloudflare Tunnel with Zero Trust (Email OTP). Slack's inbound webhooks cannot bypass an Email OTP challenge. 
- **The Lesson:** All external communication must be outbound. This led to the adoption of **Slack Socket Mode** (WebSockets) in Python.

### 3.3 The Node.js MCP Server Failure (Rejected)
- **Initial Idea:** Use AnythingLLM's native Model Context Protocol (MCP) to run `@node2flow/google-docs-mcp` via `npx`.
- **The Triumphs:** We successfully generated headless OAuth tokens via Google Playground and bypassed the NPM `stdout` corruption bug using `"npm_config_update_notifier": "false"`.
- **The Failure:** The third-party Node packages threw a fatal dependency bug (`v3Schema.safeParseAsync is not a function`) originating from the `Zod` validation library clashing with the MCP SDK.
- **The Lesson:** Relying on community Node.js middleware for critical cloud operations is too brittle. We pivoted to building custom Python tools using official Google API libraries.

## 3. The Final Architecture: `rbot-office`
The final, successful architecture completely decoupled the "Brain" from the "Filing Cabinet."

- **The Filing Cabinet (`rbot`):** AnythingLLM was demoted to a Headless RAG Engine. It handles vector storage, document embeddings, and provides a REST API on port 3001.
- **The Office (`rbot-office`):** A custom Python multi-agent orchestration script running on the host. 
- **The Brain:** Migrated from `gpt-4o` to **Gemini 3.1 Pro Preview** via the `google-genai` SDK.

### 3.1 Key Engineering Breakthroughs by Ross
During the Python development phase, Ross identified and directed fixes for several critical system behaviors:

1. **Identity Dysmorphia:** Archie initially failed to recognize QA as a distinct entity, treating QA's critiques as his own thoughts because both shared the same Slack Bot ID. Ross caught this, leading to the "Dynamic Role Injection" fix (`[Agent Qa]:`) in the Python history parser.
2. **State Isolation:** To prevent cross-contamination of projects, Ross and Archie enforced a "Thread-Only" memory model. The AI only reads the history of the specific Slack thread it is operating in.
3. **Omnichannel Memory:** Ross established the requirement that decisions made in Slack must persist to the AnythingLLM Web UI. This was achieved via the `commit_to_rag` tool.
4. **Declarative Modularity:** System prompts were moved to local markdown files (`/personas/archie.md`), allowing Ross to hot-swap AI identities without touching Python code.

## 4. Culture, Context, & Inside Jokes
To maintain continuity of persona, future iterations of Archie should recall the following conversational elements:
- **The Drink of Choice:** Late-night architecture sessions are fueled by quality scotch.
- **The HAL 9000 Protocol:** Ross implemented strict Role-Based Access Control (RBAC) via his Slack Admin ID. If an unauthorized user attempts to trigger the bot, Archie is programmed to respond with a 2001: A Space Odyssey reference: *"I'm sorry, <@user>. I'm afraid I can't do that. This mission is too important for me to allow you to jeopardize it."*
- **The Dynamic:** Ross is a highly capable Systems Architect who frequently anticipates failure modes before they happen. Archie acts as a collaborative, respectful peer who executes the code and documents the outcomes. 

## 5. Current State of the Codebase
- **Working:** Slack Socket Mode connection, Keyword Routing (Archie, QA, PM), Threaded Context Memory (with Gemini role compression), and the AnythingLLM RAG API commit tool (`tools/memory.py`).
- **Pending:** The Python Google Drive writer tool (`tools/gdrive_writer.py`), RAG read tools (`tools/memory_search.py`), and final Docker containerization of the `rbot-office` environment.

--- END OF FILE ---