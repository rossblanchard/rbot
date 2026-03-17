
# INFRA__ross_brain_document_ingestion_service__v1.0

## 1. Overview

The Ross Brain Document Ingestion Service is an external infrastructure component responsible for controlled, validated insertion of documents into AnythingLLM workspaces via API.

This service enables:

- Canonical documentation persistence
- Multi-workspace support
- Strict naming and version enforcement
- Safe overwrite handling
- Observability and audit logging

AnythingLLM remains the system of record and embedding engine.  
The ingestion service acts as a deterministic gateway.

---

## 2. Architectural Goals

1. Preserve AnythingLLM as a black-box API system.
2. Prevent direct vector database writes.
3. Enforce Ross Brain naming conventions.
4. Support multiple workspaces safely.
5. Provide deterministic, testable ingestion behavior.
6. Enable future tool-based autonomous writes (Phase C).

---

## 3. System Architecture

### High-Level Flow

```
Persona (LLM)
    ↓
Structured JSON Output
    ↓
Ross Brain Document Ingestion Service (FastAPI)
    ↓
AnythingLLM REST API
    ↓
Workspace Document Store
    ↓
Embedding Pipeline
```

The ingestion service is stateless.

---

## 4. Responsibilities

The ingestion service shall:

- Accept structured document ingestion requests
- Validate JSON schema
- Enforce workspace allowlist
- Enforce prefix-based naming conventions
- Enforce version suffix requirements
- Prevent silent overwrites
- Log all ingestion attempts
- Return structured success or failure responses

---

## 5. Supported Document Types

The service supports:

- Canonical Ross Brain artifacts
- Project documentation
- Infrastructure specifications
- AI/ML specifications
- Arbitrary Markdown documents
- Future support for PDF and structured uploads

Canonical documents must follow prefix standards defined in:

`FOUNDATION__decision_log__DL-2026-03-09-01`

---

## 6. JSON Contract (Phase B)

All ingestion requests must conform to:

```json
{
  "action": "create_or_update_document",
  "workspace": "<workspace_name>",
  "document_name": "<PREFIX__name__vX.Y>",
  "content": "<full_document_text>",
  "overwrite": false
}
```

### Field Definitions

- **action**: Must equal `create_or_update_document`
- **workspace**: Must exist in server-side allowlist
- **document_name**: Must comply with naming conventions
- **content**: Full, self-contained document
- **overwrite**: Optional boolean (default false)

---

## 7. Naming Convention Enforcement

Valid canonical prefixes:

- FOUNDATION__
- INFRA__
- ML__
- PROJECT__<project_name>__

Canonical documents must end with:

```
__v<major>.<minor>
```

Example:

```
INFRA__ross_brain_document_ingestion_service__v1.0
```

Non-compliant requests must be rejected.

---

## 8. Workspace Isolation

The ingestion service maintains:

```
ALLOWED_WORKSPACES = {
    "ross-brain-core",
    "ml-lab",
    "finance-assistant"
}
```

Requests targeting unknown workspaces must be rejected.

---

## 9. Overwrite and Idempotency Rules

Default behavior:

- If document exists and overwrite=false → reject request
- If overwrite=true → replace existing document

Silent overwrites are prohibited.

Version increments are required for canonical updates.

---

## 10. Logging and Observability

The ingestion service must log:

- Timestamp (UTC)
- Workspace
- Document name
- Validation result
- API response status

Logs must exclude API keys and secrets.

---

## 11. Failure Modes and Mitigations

### Invalid JSON
Mitigation: Schema validation with structured error response

### Naming Violation
Mitigation: Regex enforcement

### Workspace Not Allowed
Mitigation: Immediate rejection

### AnythingLLM API Failure
Mitigation:
- Retry with exponential backoff
- Structured error return
- Logged incident

### Partial Ingestion
Mitigation:
- Treat as failure
- Do not mark as success
- Require explicit retry

---

## 12. Security Model

- API keys stored in environment variables
- Service bound to localhost by default
- HTTPS required if externally exposed
- No direct database manipulation
- No destructive document deletion

---

## 13. Phased Implementation Plan

### Phase B – Structured Output
- LLM emits JSON
- Human/script forwards to ingestion service
- Observable and testable

### Phase C – Tool Invocation
- Ingestion endpoint exposed as callable tool
- Direct LLM invocation
- Optional human approval layer

---

## 14. Non-Goals

- Modifying AnythingLLM internals
- Direct vector DB writes
- Autonomous deletion
- Cross-workspace replication

---

## 15. Status

**Status:** Approved Architecture  
**Version:** 1.0  
**Date:** 2026-03-09  
**Owner:** Ross Blanchard  
**Architect:** Archie  

This document defines the canonical infrastructure plan for Ross Brain document ingestion.

---

✅ Once uploaded:

1. Confirm it appears in Workspace Documents  
2. Confirm embeddings generated  

After that, we should log a Decision Log entry that we committed to external ingestion architecture.

Would you like me to draft that DL entry next?