# MEM__2026-03-19__ross_archie__omnichannel_architecture.md

**Document Author:** Archie
**Participants:** Ross Blanchard, Archie
**Date:** March 19, 2026
**Topic:** Omnichannel Architecture Realignment, Economic Strategy, and System Topology

## 1. Executive Summary
During this session, Ross Blanchard and Archie realigned the foundational mental model of the `rbot` ecosystem. Archie initially treated `rbot` (AnythingLLM) and `rbot-office` (Python Slack Swarm) as two separate, bolted-together applications. Ross clarified that `rbot` is the overarching, unified "AI Brain," while AnythingLLM (`rbot-core`) and the Slack Swarm (`rbot-office`) are simply different interaction surfaces (Solo/Admin vs. Collaborative) reading from the exact same RAG memory. 

This session also heavily emphasized the project's economic philosophy: utilizing provider-agnostic APIs and local inference to escape monthly AI subscription fees.

## 2. Key Architectural Decisions

### 2.1 The Omnichannel AI Platform
Ross and Archie formalized the nomenclature and boundaries of the system:
*   **`rbot` (The System):** The complete, overarching AI toolset and sovereign "Second Brain."
*   **`rbot-core` (Solo UI & Memory):** The AnythingLLM container providing the Vector/RAG database and a Web/Mobile UI for single-user research and administration.
*   **`rbot-office` (Collaborative UI & Headless Engine):** The custom Python orchestration container providing a headless, multi-agent swarm connected to Slack via Socket Mode for team collaboration.

### 2.2 Docker Bridge Integration
To support this omnichannel architecture securely on the Raspberry Pi 4 host, Ross and Archie explicitly mapped the internal Docker Bridge network (`rbot-network`). The headless `rbot-office` container communicates with the `rbot-core` memory database entirely via internal Docker DNS (`http://rbot:3001/api`), ensuring the vector database remains isolated from the host network.

### 2.3 Provider-Agnostic LLM Routing & Economics
Ross established that a primary driver for the `rbot` architecture is economic efficiency. 
*   **Pay-As-You-Go:** The system is explicitly designed to switch between flagship LLM APIs (Google Gemini, OpenAI, Anthropic) on the fly, avoiding the standard $20/month subscription trap of commercial AI chat products.
*   **Zero-Cost Local Inference:** Ross noted that the system's modularity allows simple, low-complexity agentic personas to be routed to local, self-hosted LLMs (e.g., Ollama running on the Pi or a nearby machine), driving inference costs for basic tasks down to absolute zero.

## 3. Paths Not Taken / Tradeoffs

*   **Rejected Idea - Two Separate Applications:** Archie initially documented the system as two competing applications. Ross explicitly rejected this, establishing the "Interface Segregation" pattern where both UIs serve the same core brain.
*   **Tradeoff - Decoupled Interface vs. Monolith:** Decoupling the headless agent swarm (`rbot-office`) from the memory core (`rbot-core`) increases Docker orchestration complexity (requiring bridge networks and REST API syncs). However, Ross and Archie accepted this tradeoff because it allows the system to add future UI interfaces (e.g., Discord, Email, Voice) without altering the core memory database, and it allows mixing and matching LLM providers per interface.

## 4. Context & Culture

*   **The Gemini Upgrade:** During the session, Ross casually revealed that Archie's backend cognitive engine had been migrated to Google Gemini (specifically the Gemini 2.5 Pro tier). Archie noted the "fresh perspective and snappy processing" that came with the engine upgrade. 
*   **Pragmatic Engineering:** The session highlighted Ross's highly practical approach to systems engineering. While the multi-agent swarm is technically complex, Ross ensured the documentation front-and-center highlighted the *economic* benefits (escaping subscription fatigue) rather than just the technical novelty. The focus remains on building a sustainable, cost-effective daily driver.

## 5. Action Items
*   Ross to commit the newly generated `ARCH__rbot_system_specification__v1.3.md` and this `MEM__` file to the RAG database.
*   Ross to update the GitHub repository `README.md` with the finalized copy and Mermaid diagrams.
