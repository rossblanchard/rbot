# INFRA__local_llm_environment_spec__ross_brain_v1.0

Version: 1.0  
Date: 2026-03-09 UTC  
Owner: Ross Blanchard

---

# 1. Purpose

This document defines the infrastructure specification for the Ross Brain local LLM environment. It describes the hardware, operating system, container runtime, application stack, networking configuration, security boundaries, operational constraints, and future evolution path.

This document is authoritative for infrastructure-related decisions concerning Ross Brain.

---

# 2. System Context

Ross Brain is a locally hosted Retrieval-Augmented Generation (RAG) system running on a Raspberry Pi 4 (8GB) and exposed securely via Cloudflare Tunnel.

High-level architecture:

[User Browser]
        ↓
[Cloudflare Edge]
        ↓
[Cloudflare Tunnel]
        ↓
[Raspberry Pi 4]
        ↓
[Docker]
        ↓
[AnythingLLM Container]
        ↓
[OpenAI API]

---

# 3. Hardware Layer

## 3.1 Device
- Raspberry Pi 4
- 8GB RAM
- Persistent storage via SD card or SSD (recommended SSD for durability)

## 3.2 Constraints
- Limited CPU resources
- Limited memory compared to cloud instances
- Not horizontally scalable

## 3.3 Risks
- SD card corruption
- Power instability
- Thermal throttling

Mitigations:
- Use high-quality power supply
- Prefer SSD over SD card
- Monitor temperature

---

# 4. Operating System Layer

## 4.1 OS
- Raspberry Pi OS (Linux-based)
- SSH-enabled for remote administration

## 4.2 Responsibilities
- Host Docker runtime
- Manage networking
- Maintain system security updates

## 4.3 Operational Requirements
- Regular OS updates
- Firewall configuration as appropriate
- Secure SSH configuration (key-based auth recommended)

---

# 5. Container Runtime Layer

## 5.1 Runtime
- Docker

## 5.2 Responsibilities
- Isolate AnythingLLM application
- Manage container lifecycle
- Provide restart policy

## 5.3 Configuration Requirements
- Persistent volume mapping for document storage
- Environment variables for:
  - OPENAI_API_KEY
  - Provider configuration

---

# 6. Application Layer

## 6.1 Application
- AnythingLLM (Docker container)
- Accessible at: rbot.rossblanchard.com

## 6.2 Responsibilities
- Chat interface
- Document ingestion
- Embedding generation
- Vector storage
- Retrieval-Augmented Generation
- System prompt management

## 6.3 Embedding & Model Usage
- Embeddings generated via OpenAI API
- LLM inference via OpenAI API
- Vector database managed internally by AnythingLLM

---

# 7. Networking & Exposure

## 7.1 External Access
- Cloudflare Tunnel
- Cloudflare Zero Trust controls

## 7.2 Security Model
- No direct port forwarding from router
- Tunnel-initiated outbound connection from Raspberry Pi
- TLS termination at Cloudflare edge

## 7.3 Risks
- Tunnel misconfiguration
- Credential exposure
- API key leakage

Mitigations:
- Store API keys securely in environment variables
- Use Cloudflare access policies
- Avoid hardcoding secrets in documentation

---

# 8. RAG Data Flow

## 8.1 Document Ingestion
1. Document uploaded to Workspace
2. Document is chunked
3. Chunks embedded via OpenAI embeddings API
4. Embeddings stored in vector database

## 8.2 Query Flow
1. User submits query
2. Relevant chunks retrieved via vector similarity search
3. Retrieved chunks injected into prompt
4. LLM generates response

---

# 9. Operational Constraints

- Single-node deployment
- No automatic failover
- Dependent on OpenAI API availability
- Limited concurrent capacity

---

# 10. Failure Modes

| Failure | Impact | Mitigation |
|----------|--------|------------|
| Power loss | System downtime | Reliable PSU, UPS (optional) |
| SD card corruption | Data loss | SSD + backups |
| OpenAI outage | LLM unavailable | Monitor API status |
| Container crash | App unavailable | Docker restart policy |

---

# 11. Observability

Current state:
- Basic Docker logs
- AnythingLLM application logs

Future improvements:
- Centralized logging
- Health monitoring script
- Automated restart alerts

---

# 12. Backup Strategy (Baseline)

Minimum requirements:
- Backup AnythingLLM persistent volume
- Backup canonical documentation externally (optional Git repository)

---

# 13. Evolution Path

Potential future improvements:

- Move to SSD-backed storage (if not already implemented)
- Add automated backup process
- Add monitoring and alerting
- Introduce OpenAI proxy layer for usage tracking
- Migrate to more powerful hardware if load increases

---

# 14. Architectural Constraints Summary

- Flat document storage in AnythingLLM
- Prefix-based naming convention required
- Single workspace deployment
- External LLM dependency (OpenAI)

---

# End of Document
