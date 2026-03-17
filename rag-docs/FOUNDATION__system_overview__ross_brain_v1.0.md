# Ross Brain – System Overview
Version: 1.0  
Date: 2026-03-09 UTC  
Status: Active

---

## 1. Purpose

Ross Brain is a structured, persistent engineering knowledge system designed to:

- Preserve architectural decisions and system designs
- Maintain structured, retrieval-optimized documentation
- Support AI-assisted engineering workflows
- Provide long-term institutional memory

Ross Brain operates within a locally hosted AnythingLLM environment and uses Retrieval-Augmented Generation (RAG) to enhance responses with stored canonical documentation.

---

## 2. Execution Environment

### 2.1 Hardware

- Device: Raspberry Pi 4
- Memory: 8GB RAM
- Role: Local AI orchestration host
- Location: Portland, Oregon (default operational context)

The Raspberry Pi hosts the AnythingLLM application inside a Docker container and serves as the orchestration layer between the user and external LLM providers.

---

### 2.2 Software Stack

- Container Runtime: Docker
- Application: AnythingLLM (self-hosted)
- LLM Provider: OpenAI API (remote)
- Access URL: rbot.rossblanchard.com

Responsibilities of AnythingLLM:

- Chat interface
- System prompt management
- Document ingestion
- Document chunking
- Embedding generation
- Vector storage
- Retrieval injection into prompts

The Raspberry Pi does not host the LLM model itself; it orchestrates API calls to OpenAI.

---

## 3. High-Level Architecture

[User (Ross)]  
    ↓  
[Web Interface – AnythingLLM]  
    ↓  
[System Prompt + Retrieved Documents]  
    ↓  
[OpenAI API]  
    ↓  
[Response Returned to AnythingLLM]  
    ↓  
[Rendered in Chat Interface]

Documents are embedded and stored locally within the workspace vector database.

---

## 4. Retrieval-Augmented Generation (RAG) Flow

### 4.1 Document Ingestion

1. Canonical document uploaded to Workspace Documents
2. Document is chunked into semantically coherent segments
3. Each chunk is converted into an embedding vector
4. Embeddings stored in vector database

---

### 4.2 Query-Time Retrieval

1. User submits query
2. Query is embedded into vector space
3. Similar document chunks are retrieved
4. Retrieved chunks are injected into the prompt
5. Augmented prompt is sent to OpenAI
6. Response is generated using both retrieved knowledge and model reasoning

Important:
- Model weights are not modified
- Knowledge is injected dynamically per request

---

## 5. Knowledge Organization Model

AnythingLLM workspace document storage is flat.

To compensate, Ross Brain uses a prefix-based naming convention (DL-2026-03-09-01):

- FOUNDATION__
- PROJECT__<project_name>__
- ML__
- INFRA__

This enforces logical grouping without relying on folder hierarchy.

---

## 6. Governance Model

Ross Brain operates under documentation discipline defined in the system prompt.

Key principles:

- Milestone-based documentation
- Explicit architectural stabilization points
- Structured, self-contained canonical artifacts
- Clear distinction between exploratory and finalized design
- Decision logging for tradeoffs

All finalized artifacts must be uploaded to Workspace Documents for persistent RAG inclusion.

---

## 7. Constraints

### 7.1 Platform Constraints

- Flat document storage (no enforced hierarchy)
- Dependent on OpenAI API availability
- Raspberry Pi resource limitations (CPU and memory)
- No local model hosting at present

### 7.2 Architectural Constraints

- Single workspace for all documentation (v1.0)
- Manual governance enforcement required
- Embedding quality dependent on external provider

---

## 8. Security Considerations

- OpenAI API key stored in environment configuration
- Docker container boundary provides process isolation
- External API dependency introduces network exposure
- Access to rbot.rossblanchard.com must be secured via HTTPS and authentication

---

## 9. Observability

Current Observability:

- Docker logs
- OpenAI usage dashboard

Future improvements may include:

- Structured usage logging
- Per-request metadata logging
- Proxy-based request auditing

---

## 10. Future Evolution Path

Potential evolution directions:

1. Multiple workspaces for domain separation
2. External Git-backed canonical document repository
3. Automated document synchronization
4. OpenAI proxy for usage tracking and logging
5. Hybrid local + remote LLM architecture
6. Automated documentation validation workflows

Ross Brain v1.0 prioritizes simplicity and structural discipline before increasing architectural complexity.

---

## 11. Success Criteria

Ross Brain is considered successful when:

- Architectural knowledge does not depend on chat history
- Decisions are logged and retrievable
- Terminology remains consistent
- Retrieval produces accurate contextual augmentation
- Documentation scales without structural entropy

---

# End of Document
