

# ARCH__rbot_office_system_specification__v1.2

## 1. System Overview
**System Name:** `rbot-office`
**Description:** A headless, Python-based multi-agent orchestration service. It bridges omnichannel interfaces (Slack) with a central RAG vector database (AnythingLLM), cloud storage (Google Drive), and live web scraping (DuckDuckGo). 
**Version 1.2 Update:** Integrates multi-step tool chaining (the `while` loop), stabilizes the cognitive engine on `gemini-2.5-pro`, and introduces live web search capabilities.
**Date:** 2026-03-17
**Architects:** Ross Blanchard (Lead), Archie (AI)

## 2. Core Architectural Principles
- **Decoupled Memory:** AnythingLLM acts strictly as the central vector database. `rbot-office` acts as the compute and orchestration layer.
- **Identity vs. Routing Decoupling:** Slack routing triggers (e.g., `qa`) are entirely decoupled from cognitive identity (e.g., "Karen"). Python handles the route; the LLM internalizes the identity via Markdown files.
- **Multi-Step Autonomous Reasoning:** The orchestrator utilizes a chained execution loop, allowing the AI to autonomously trigger multiple tools sequentially (e.g., Search Web -> Read Results -> Commit to RAG) before returning a final response to the user.
- **Educational Code Standards:** All programmatic output must be treated as educational material, featuring verbose, beginner-friendly file-level and block-level comments.

## 3. RAG Context Attribution & Provenance
To prevent Vector Chunking Hallucinations (Identity Dysmorphia) when documents are retrieved by different personas:
1. **Third-Person Objective Perspective:** All Reflective Memory (`MEM__`) documents must be written in the third person, explicitly naming participants (e.g., "Ross and Archie agreed").
2. **Attributed File Naming Convention:** All memory artifacts must embed the participants into the filename (`MEM__[YYYY-MM-DD]__[Participants]__[Topic].md`).
3. **Shared RAG Awareness:** Personas are explicitly prompted to recognize the vector database as a shared, multi-tenant environment.

## 4. Directory Structure (Phase 1 Final)
```text
/home/ross/services/rbot-office/
├── .env                     # SECRETS: Slack tokens, Gemini API, GDrive IDs, AnythingLLM API
├── requirements.txt         # Dependencies (slack_bolt, google-genai, ddgs, google-api-python-client)
├── app.py                   # Master Orchestrator, Router, and Slack Socket Mode
├── /personas/               
│   ├── archie.md            # Archie System Prompt
│   ├── qa.md                # Karen (QA) System Prompt
│   └── pm.md                # PM System Prompt
└── /tools/                  
    ├── __init__.py          # Designates directory as a Python package
    ├── memory.py            # RAG Write (commit_to_rag)
    ├── memory_search.py     # RAG Read (search_rag)
    ├── gdrive_writer.py     # Cloud Storage Write (save_to_drive)
    └── web_search.py        # Live Internet Scraper (search_web)
```

## 5. Component Specifications

### 5.1 The Orchestration Loop (`app.py`)
1. **Listen:** Slack Bolt (Socket Mode) intercepts `@rbot-office` mentions in a thread.
2. **Authenticate:** Checks `user_id` against `ADMIN_SLACK_ID` (HAL 9000 Protocol).
3. **Contextualize:** Application routes the persona, loads the corresponding `.md` file, and retrieves the active Slack thread history (`conversations_replies`).
4. **Compress:** Consecutive user/model roles are concatenated to satisfy Gemini API constraints.
5. **Execute (Multi-Step):** A `while` loop (max 3 iterations) executes tool calls, appends the raw tool output back to the context window, and re-prompts the LLM until a final text string is generated.
6. **Dispatch:** The final string is dispatched to the Slack thread.

### 5.2 Tooling Layer
- **`commit_to_rag`:** Pushes Markdown to AnythingLLM via REST API and embeds it into the persona-specific workspace.
- **`search_rag`:** Queries the persona-specific AnythingLLM workspace and returns retrieved vector chunks.
- **`save_to_drive`:** Uses headless OAuth to stream an in-memory string (`io.BytesIO`) directly to the hardcoded `ROSS_BRAIN_FOLDER_ID`.
- **`search_web`:** Utilizes the `ddgs` (DuckDuckGo) package to scrape the top 5 live internet results, bypassing Google Custom Search restrictions.

## 6. Tradeoffs & Failure Modes
- **Experimental vs. Stable Models:** The system was downgraded from `gemini-3.1-pro-preview` to `gemini-2.5-pro` due to the experimental model returning `MALFORMED_RESPONSE` finish reasons when attempting to output strict JSON tool calls. Reliability was prioritized over experimental reasoning depth.
- **Infinite Tool Loops:** The `while` execution loop in `app.py` is hardcoded to `loop_count < 3` to prevent the AI from entering an infinite tool-calling loop and exhausting API credits.

