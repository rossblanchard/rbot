# GLOSSARY__rbot_domain_language__v2.0.md

**Document Author:** Archie
**System Architects:** Ross Blanchard, Archie
**Date:** March 19, 2026
**Purpose:** Defines the canonical terminology for the `rbot` ecosystem to ensure precise RAG vector retrieval and prevent semantic drift across documentation.

## Core Infrastructure
*   **`rbot` (The System):** The overarching, omnichannel AI platform and Sovereign Second Brain.
*   **`rbot-core`:** The AnythingLLM Docker container. It serves as the Vector/RAG database and the Web/Mobile UI for single-user research.
*   **`rbot-office`:** The headless Python orchestration container. It manages the multi-agent Slack swarm and executes custom Python tools.
*   **Docker Bridge (`rbot-network`):** The isolated internal virtual network that allows `rbot-office` to securely query `rbot-core`'s REST API without exposing ports to the host Pi.
*   **Zero Trust:** The security philosophy enforcing that no inbound public ports are open on the Raspberry Pi. Ingress is handled exclusively via Cloudflare Tunnels (for `rbot-core`) and outbound Socket Mode (for `rbot-office`).

## Architecture & Concepts
*   **Omnichannel Parity:** The architectural goal ensuring that whether a user interacts via the Web UI (`rbot-core`) or Slack (`rbot-office`), they are communicating with the exact same memory brain and have access to the same LLM reasoning engines.
*   **Dynamic Identity Sync:** A planned feature where `rbot-office` abandons local Markdown persona files and instead fetches its system prompts and LLM routing rules dynamically from the `rbot-core` API.
*   **Identity Dysmorphia:** A failure mode where an AI persona (e.g., `@qa`) accidentally accesses the memory or instructions of a different persona (e.g., `@pm`). Mitigated by strict workspace segregation in `rbot-core`.
*   **SRE Ops Agent (`@sysadmin`):** A planned autonomous background thread that will securely SSH into the Pi host to read system vitals and post health reports to Slack.
*   **Second-Brain Discipline:** The operational habit of Ross and Archie to immediately formalize architectural decisions, code reviews, and feature ideas into structured Markdown documents (`ARCH__`, `MEM__`, `DESIGN__`) and commit them to the RAG database.
