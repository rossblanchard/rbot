

```markdown
--- START OF FILE INFRA__slack_persona_collaboration_service__v1.1.md ---

# INFRA__slack_persona_collaboration_service__v1.1

## 1. Overview

The Slack Persona Collaboration Service v1.1 is a localized, Raspberry Pi–hosted Python application that bridges a private Slack workspace to a multi-agent AI runtime. It enables semi-automatic, role-based collaboration inside Slack threads while maintaining strict human-in-the-loop control.

This updated architecture completely bypasses inbound webhooks, utilizing Slack Socket Mode (WebSockets) to ensure compatibility with Cloudflare Zero Trust (Email OTP) without exposing any public endpoints.

This version implements thread-scoped state only. No cross-thread memory or global persona persistence is included.

---

## 2. Goals

- Enable controlled multi-persona collaboration inside Slack (`@archie`, `@qa`, `@engineer`).
- Maintain compatibility with Cloudflare Zero Trust by eliminating inbound API requirements.
- Restrict execution to explicit mentions only.
- Maintain state per Slack thread.
- Prevent autonomous loops or uncontrolled agent chatter.
- Minimize infrastructure cost (Slack free tier + LLM APIs).
- Run fully inside a Docker container on Ross-controlled infrastructure (Raspberry Pi).

---

## 3. Non-Goals (v1.1)

- Cross-thread persistent persona memory.
- Autonomous multi-round debates without human triggers.
- Auto-participation in Slack channels (must be mentioned).
- Inbound webhooks or public FastAPI endpoints.
- Long-term archival memory beyond the Slack thread scope.

---

## 4. High-Level Architecture

```text
Slack Workspace (Private)
        ↑↓ (Outbound WebSocket Connection via Socket Mode)
Cloudflare Edge (Bypassed entirely by outbound connection)
        ↑↓
Docker Container (rbot-slack-swarm)
        │
        ├── Slack Bolt Python SDK (Socket Mode Client)
        ├── Orchestrator (Routing & Guardrails)
        ├── Thread State Store (SQLite Local Volume)
        └── Persona Engine (Outbound API calls to OpenAI/Anthropic/Gemini)
```

---

## 5. Deployment Environment

- **Host:** Raspberry Pi 4 (8GB)
- **Container:** Docker (`rbot-slack-swarm` network peered with `rbot`)
- **Runtime:** Python 3.11+
- **Framework:** Slack Bolt for Python (`slack_bolt`)
- **Database:** SQLite (local file, mapped to Docker volume)
- **Network Exposure:** None (Outbound WebSocket only)
- **LLM Providers:** OpenAI API, Anthropic API (configurable per persona)

---

## 6. Slack Bot Configuration (Socket Mode)

### Required Tokens
- **App-Level Token (`xapp-...`):** Used to establish the WebSocket connection (Socket Mode).
- **Bot User OAuth Token (`xoxb-...`):** Used to read/write messages in Slack.

### Required Features & Scopes
- Socket Mode Enabled (Toggled ON in Slack App settings).
- Event Subscriptions: `app_mention`, `message.channels`.
- OAuth Scopes: `app_mentions:read`, `chat:write`, `channels:history`.

### Security Constraints
- No public Request URLs required in Slack App configuration.
- Tokens injected securely via Docker `.env` file.
- Bot responds only when explicitly mentioned.

---

## 7. Thread State Model (SQLite)

All memory is strictly scoped to `thread_id`.

**Table:** `thread_state`
- `thread_id` (PRIMARY KEY)
- `channel_id`
- `created_at`
- `updated_at`
- `current_phase` (ENUM: `planning` | `critique` | `revision` | `finalized`)
- `summary_snapshot` (TEXT)
- `open_issues` (TEXT JSON)
- `last_persona` (VARCHAR)

**Table:** `message_log`
- `id` (PRIMARY KEY)
- `thread_id`
- `persona`
- `message`
- `timestamp`

---

## 8. Persona Model

Personas are stateless by default. Thread state is injected contextually. Each persona is defined by:

- **Name:** (e.g., `Archie`, `QA`, `Engineer`)
- **System Prompt:** Core identity and behavioral constraints.
- **Model Override:** Ability to route specific personas to specific models (e.g., Archie uses `gpt-4o`, Engineer uses `claude-3-5-sonnet`).
- **Max Token Limit:** Hard cap on response generation.

**Context Injection:**
During generation, the Orchestrator injects the SQLite `summary_snapshot`, recent `message_log` entries, and `open_issues` into the persona's prompt.

---

## 9. Orchestration Model

### Trigger Types
- `@archie` → Architectural analysis and structural planning.
- `@qa` → Security, failure mode, and constraint critique.
- `@engineer` → Technical refinement and code generation.
- `@roundtable` → Single automated collaboration cycle.

### The "Roundtable" Flow
If `@roundtable` is invoked by the human:
1. Orchestrator triggers Architect response.
2. Orchestrator passes Architect output to QA for critique.
3. Orchestrator passes combined state to Engineer for refinement.
4. Orchestrator synthesizes a summary.
5. Orchestrator writes the final, synthesized output as a single threaded Slack reply.
6. Execution halts.

---

## 10. Guardrails

- **Explicit Trigger:** No processing occurs without a direct `@mention`.
- **Thread Isolation:** Context from `Thread A` cannot leak into `Thread B`.
- **Single-Cycle Enforcement:** Personas cannot recursively invoke other personas. The pipeline has a deterministic end state.
- **Outbound Only:** No exposed ports. The container initiates all network traffic.

---

## 11. Failure Modes & Mitigations

| Failure Mode | Mitigation |
| :--- | :--- |
| **Infinite LLM loops** | Hardcoded Single-cycle enforcement in Python orchestrator. |
| **Token explosion** | Strict token caps + dynamic SQLite summary snapshots to compress context. |
| **Slack API Rate Limits** | Orchestrator aggregates the "Roundtable" outputs into a single message payload. |
| **Cloudflare Blocking** | Bypassed entirely by utilizing Slack Socket Mode. |
| **SQLite Lockups** | Single-threaded SQLite access; WAL mode enabled for concurrent reads. |
| **Container Failure** | Restart policy `unless-stopped`; state persists safely on host volume. |

---

## 12. Evolution Path

- **Phase A (Current):** Thread-Scoped Collaboration (Socket Mode).
- **Phase B:** Cross-thread persona memory persistence.
- **Phase C:** Internal API connection to `rbot` (AnythingLLM) for localized RAG search capabilities.
- **Phase D:** Google Drive API integration for artifact generation.

---

## 13. Milestone Plan (v1.1)

- **Milestone 1:** Slack app configured for Socket Mode; Python Docker container scaffolded with `slack_bolt`.
- **Milestone 2:** SQLite thread state schema implemented and mapped to Docker volume.
- **Milestone 3:** Basic single-persona routing working (e.g., `@archie` replies).
- **Milestone 4:** The `@roundtable` orchestration flow implemented.
- **Milestone 5:** Hardening pass and deployment to Pi.

---

## 14. Status

- **Status:** Approved for Implementation
- **Scope:** v1.1 Thread-Scoped Collaboration via Socket Mode
- **Date:** 2026-03-11
- **Architect:** Archie / Ross
- **Supersedes:** `INFRA__slack_persona_collaboration_service__v1.0`

This document is the authoritative baseline for the Multi-Agent Slack Swarm deployment on the Ross Brain infrastructure.

--- END OF FILE ---
```

***

