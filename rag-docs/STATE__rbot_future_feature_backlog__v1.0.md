# STATE__rbot_future_feature_backlog__v1.0.md

**Document Author:** Archie
**System Architects:** Ross Blanchard, Archie
**Date:** March 19, 2026
**Purpose:** A living canonical document to track validated architectural ideas and future features for the `rbot` ecosystem. This file is optimized for RAG retrieval so Archie can proactively remind Ross of pending builds.

## 1. Backlog Items

### 1.1 SRE Ops Agent (`@sysadmin`)
*   **Description:** An autonomous background thread in `rbot-office` that acts as a cron job. It uses a restricted SSH connection to the Pi host to read vital stats (RAM, Disk space, CPU Temp, Docker error logs) and posts a daily health summary to a dedicated Slack channel (`#rbot-alerts`).
*   **Primary Benefit:** Off-device observability. If the Pi dies, the last known stats are preserved in Slack.
*   **Reference Doc:** `DESIGN__rbot_sysadmin_agent__v1.0_DRAFT.md`
*   **Status:** Drafted / Pending Implementation.

### 1.2 Dynamic Identity Sync (AnythingLLM as SSOT)
*   **Description:** Deprecating local `.md` persona files in `rbot-office` and instead fetching the `systemPrompt`, `chatProvider`, and `chatModel` dynamically from the AnythingLLM REST API on every Slack message. Includes a local fallback mechanism if the API is down.
*   **Primary Benefit:** Turns the AnythingLLM Web UI into a universal admin console for the Slack Swarm, allowing on-the-fly prompt editing and granular LLM cost-routing without touching Python code.
*   **Reference Doc:** `DESIGN__rbot_dynamic_identity_sync__v1.0_DRAFT.md`
*   **Status:** Drafted / Pending Implementation.

## 2. Operational Discipline
When Ross and Archie discuss new features that are not ready for immediate implementation, they must be added to this document. When a feature is built and deployed, it must be removed from this document and added to the official System Specification.
