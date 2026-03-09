# INFRA__slack_persona_collaboration_service__v1

## 1. Overview

The Slack Persona Collaboration Service v1 is a Raspberry Pi–hosted bridge service that connects a private Slack workspace to the Ross Brain (AnythingLLM) runtime. It enables semi-automatic, role-based collaboration inside Slack threads while maintaining strict human-in-the-loop control.

This version (v1) implements thread-scoped state only. No cross-thread memory or global persona persistence is included.

---

## 2. Goals

- Enable controlled multi-persona collaboration inside Slack
- Restrict execution to explicit mentions only
- Maintain state per Slack thread
- Prevent autonomous loops or uncontrolled agent chatter
- Minimize infrastructure cost (Slack free tier + OpenAI API only)
- Run fully under Ross-controlled infrastructure (Raspberry Pi)

---

## 3. Non-Goals (v1)

- Cross-thread persistent persona memory
- Autonomous multi-round debates
- Auto-participation in channels
- Cross-workspace federation
- Long-term archival memory beyond Slack thread scope

---

## 4. High-Level Architecture

```
Slack Workspace (Private)
        ↓
Slack Bot (Events API)
        ↓
Bridge Service (FastAPI on Raspberry Pi)
        ↓
Thread State Store (SQLite)
        ↓
Orchestrator
        ↓
Persona Engine (LLM Calls)
        ↓
Slack Thread Replies
```

---

## 5. Deployment Environment

- Host: Raspberry Pi 4 (8GB)
- Runtime: Python 3.11+
- Framework: FastAPI
- Database: SQLite (local file)
- Exposure: Cloudflare Tunnel
- LLM Provider: OpenAI API
- Optional: AnythingLLM API integration (future phase)

---

## 6. Slack Bot Configuration

### Required Features
- Bot token
- Event subscriptions enabled
- message.channels scope
- app_mentions:read
- chat:write

### Security
- Slack signing secret verification required
- Bot token stored in environment variables
- OpenAI API key stored in environment variables

### Behavior Constraints
- Respond only when explicitly mentioned
- Operate only within Slack threads
- No auto-initiation of conversation

---

## 7. Thread State Model (SQLite)

Table: thread_state

Fields:
- thread_id (PRIMARY KEY)
- channel_id
- created_at
- updated_at
- current_phase (planning | critique | revision | finalized)
- summary_snapshot (TEXT)
- open_issues (TEXT JSON)
- last_persona

Table: message_log

Fields:
- id (PRIMARY KEY)
- thread_id
- persona
- message
- timestamp

All memory is scoped to thread_id.

---

## 8. Persona Model

Each persona is defined by:

- Unique name (e.g., Architect, QA, Engineer)
- System prompt template
- Role-specific behavioral constraints
- Max token limit

Personas are stateless by default. Thread state is injected into each call via:

- summary_snapshot
- recent thread messages
- open_issues list

---

## 9. Orchestration Model

### Trigger Types

- @archie → Architect response
- @qa → QA critique
- @engineer → Engineering refinement
- @roundtable → Single collaboration cycle

### Roundtable Flow

1. Architect response
2. QA critique
3. Engineer refinement
4. Synthesized summary
5. Thread state update
6. Slack reply (threaded)

Hard limits:
- One collaboration cycle per trigger
- No recursive persona invocation
- No autonomous follow-up

---

## 10. Guardrails

- Explicit mention required
- Thread-only memory
- Max token limits per persona
- Hard stop after response
- No persona-to-persona direct messaging
- No background autonomous processing

---

## 11. Failure Modes

| Failure Mode | Mitigation |
|--------------|------------|
| Infinite loops | Single-cycle enforcement |
| Token explosion | Strict token caps + summary snapshots |
| Slack spam | Mention-only trigger |
| State corruption | Thread-scoped transactional updates |
| Unauthorized access | Private workspace + signature verification |

---

## 12. Evolution Path

Future phases may introduce:

Phase B:
- Cross-thread persona memory

Phase C:
- Ross Brain (AnythingLLM) RAG integration

Phase D:
- Controlled autonomous collaboration loops

Each phase requires updated documentation and decision logging.

---

## 13. Architectural Principles

- Human-directed collaboration only
- Deterministic orchestration
- Explicit state management
- Minimal surface area
- Zero SaaS dependency beyond Slack + OpenAI
- Observability over magic

---

## 14. Milestone Plan (v1)

Milestone 1:
- Slack app configured
- FastAPI bridge scaffolded
- Signature verification implemented

Milestone 2:
- SQLite thread state schema implemented
- Basic persona routing working

Milestone 3:
- Roundtable orchestration implemented
- Guardrails validated

Milestone 4:
- Logging and observability added
- Hardening pass

---

## 15. Status

Status: Approved for Implementation
Scope: v1 Thread-Scoped Collaboration Only
Date: 2026-03-09

This document is the authoritative baseline for INFRA__slack_persona_collaboration_service__v1.