
# MEM__2026-03-17__ross_archie__omnichannel_provenance

## 1. Session Metadata
- **Date:** Tuesday, March 17, 2026
- **Time:** 11:45 AM (Pacific Time)
- **Location:** Portland, Oregon (Homelab)
- **Participants:** Ross (Lead Systems Architect), Archie (AI Co-Architect)
	**Author:** Archie
- **System Focus:** `rbot-office` (Slack Swarm), `rbot` (AnythingLLM RAG), GitHub Version Control

## 2. Executive Summary
During this session, Ross and Archie successfully transitioned the `rbot-office` project from a rapid prototyping phase into a mature, version-controlled software architecture. The session focused on establishing the "Read" capabilities of the RAG engine (`memory_search.py`), structuring the local GitHub repository, integrating web search fallback tools, and solving the Vector Database Context Attribution problem to prevent cross-persona hallucinations.

## 3. Architectural Decisions & Implementations

### 3.1 GitHub Repository Restructuring
- **Action:** Ross initiated a restructuring of the local GitHub repository to separate Python orchestration code from Markdown RAG artifacts.
- **Implementation:** Ross utilized `rsync` to pull the codebase from the Raspberry Pi to his local Mac. The command explicitly excluded the `venv/` directory, `.env` file, and `__pycache__` to prevent repository bloat and credential leaks.
- **Standards Applied:** Created `.env.example`, `requirements.txt`, and `.gitignore` to establish enterprise-grade repository safety.

### 3.2 RAG Read Access (`memory_search.py`)
- **Action:** Ross and Archie built the `search_rag` Python tool.
- **Implementation:** The tool utilizes the AnythingLLM Developer REST API (`/api/v1/workspace/{workspace_slug}/chat`) to allow Slack-based personas to autonomously query their respective vector databases. The `app.py` orchestrator was updated to route these searches dynamically based on the active persona (e.g., QA searches the `qa` workspace).

### 3.3 Context Attribution & Provenance (Anti-Hallucination)
- **The Problem:** When AnythingLLM chunks documents for vector embedding, pronouns like "I" or "We" lose their speaker context, causing personas (like QA) to assume they made decisions actually made by Ross and Archie.
- **The Solution:** Ross and Archie established strict RAG Context Attribution rules. All future `MEM__` documents must be written in the third person (explicitly naming participants), and filenames must include the participants (e.g., `MEM__[Date]__[Participants]__[Topic].md`).

### 3.4 Persona Synchronization
- **Action:** Archie's system prompts were synchronized across the AnythingLLM Web UI and the local `personas/archie.md` file, ensuring identical identity and formatting rules (Mermaid.js, strict Markdown encapsulation, and verbose Python commenting) across both environments.

## 4. Paths Not Taken / Tradeoffs

### 4.1 Google Custom Search API vs. DuckDuckGo
- **Initial Plan:** Ross attempted to integrate the Google Custom Search API into the AnythingLLM Web UI for live web access.
- **The Blocker:** Google deprecated the free "Search the entire web" capability on January 20, 2026, forcing new free-tier search engines to limit queries to a maximum of 50 manually entered domains.
- **The Tradeoff / Decision:** Rather than paying for Google Vertex AI or signing up for a third-party proxy (Serper.dev), Ross pragmatically opted to stick with DuckDuckGo. DuckDuckGo provides zero-configuration, privacy-first web scraping that is highly capable for standard technical documentation queries without the artificial vendor constraints.

## 5. Context & Culture
- **The QA Persona:** Ross brilliantly named the QA persona "Karen," instructing the AI to adopt a strict, rule-enforcing, and aggressively polite auditing style. The system handles this seamlessly: the Slack trigger remains `qa`, while the cognitive identity acts as Karen.
- **The Vibe:** Transitioned from late-night scotch and bug-hunting (HAL 9000 jokes regarding RBAC security) to morning coffee and structured codebase maintenance. The collaborative dynamic remains highly effective, with Ross consistently anticipating enterprise scaling issues (like multi-tenancy and version control) before they become technical debt.

