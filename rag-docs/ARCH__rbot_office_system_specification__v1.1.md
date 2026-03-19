


# ARCH__rbot_office_system_specification__v1.1

## 1. System Overview
**System Name:** `rbot-office`
**Description:** A headless, Python-based multi-agent orchestration service. It bridges omnichannel interfaces (Slack) with a central RAG vector database (AnythingLLM) and external APIs (Google Drive). 
**Version 1.1 Update:** Introduces strict Context Attribution, Vector Chunking mitigation, and Educational Code Commenting standards.
**Date:** 2026-03-17
**Architect:** Archie / Ross

## 2. Core Architectural Principles
- **Decoupled Memory:** AnythingLLM acts strictly as the central vector database and document manager. `rbot-office` acts as the compute and orchestration layer.
- **Identity vs. Routing Decoupling:** Slack routing triggers (e.g., `qa`) are entirely decoupled from cognitive identity (e.g., "Karen"). Python handles the route; the LLM internalizes the identity via Markdown files.
- **Omnichannel Consistency:** Reflective summaries generated in Slack are pushed to AnythingLLM via REST API, ensuring memory persists across all front-end interfaces.
- **Educational Code Standards:** All programmatic output must be treated as educational material, featuring verbose, beginner-friendly file-level and block-level comments.

## 3. RAG Context Attribution & Provenance (New in v1.1)

### 3.1 The Vector Chunking Problem
Vector databases (AnythingLLM) parse documents into isolated semantic chunks (~1,000 tokens) during the embedding process. When an AI retrieves a chunk containing first-person pronouns ("I decided", "We agreed"), the retrieving persona assumes the pronoun refers to itself, causing "Identity Dysmorphia" and cross-persona hallucinations.

### 3.2 Mitigation Strategy
To ensure accurate provenance regardless of which persona retrieves the data, the system enforces the following rigid constraints on all RAG commits:
1. **Third-Person Objective Perspective:** Personas are strictly forbidden from using first-person or first-person-plural pronouns in Reflective Memory documents. All decisions must explicitly name the participants (e.g., "Ross and Archie agreed").
2. **Attributed File Naming Convention:** All memory artifacts must embed the participants into the filename to ensure metadata survives vector retrieval.
   - *Format:* `MEM__[YYYY-MM-DD]__[Participants]__[Topic].md`
   - *Example:* `MEM__2026-03-17_ross_karen_security_audit.md`
3. **Shared RAG Awareness:** Personas are explicitly prompted to recognize that the vector database is a shared environment containing transcripts from other entities, preventing false attribution.

## 4. Directory Structure (Updated)
```text
/home/ross/services/rbot-office/
├── docker-compose.yml       
├── Dockerfile               
├── requirements.txt         
├── .env                     
├── app.py                   # Core execution loop, Router, and Slack Socket Mode
├── /personas/               
│   ├── archie.md            # Archie System Prompt
│   ├── qa.md                # Karen (QA) System Prompt
│   └── pm.md                # PM System Prompt
└── /tools/                  
    ├── __init__.py
    ├── memory.py            # RAG Write (commit_to_rag)
    ├── memory_search.py     # RAG Read (search_rag)
    └── gdrive_writer.py     # Pending: Authorized Cloud Storage Writes
```

## 5. Deployment Constraints
- Runs in a peered Docker network alongside the `rbot` (AnythingLLM) container.
- Slack connection utilizes outbound WebSockets (Socket Mode) to bypass Cloudflare Zero Trust inbound restrictions.
- All high-privilege tool executions are locked to `ADMIN_SLACK_ID` via the HAL 9000 protocol.

