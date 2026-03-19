# INDEX__global_projects_directory__v1.0.md

**Document Author:** Archie
**System Architects:** Ross Blanchard, Archie
**Date:** March 19, 2026
**Purpose:** The highest-level Master Index ("Map of Maps") for the `rbot` Omnichannel AI ecosystem. This document directs the AI to the specific AnythingLLM Workspaces and sub-indexes for all isolated domains (engineering, client projects, personal life).

## 1. Multi-Tenant Architecture Rule
To prevent context bleed between discrete projects, `rbot-office` (the Swarm) must route RAG commitments and searches to isolated Vector Databases (AnythingLLM Workspaces) using the target `{slug}` parameter in its API tools (`commit_to_rag`, `search_rag`). 

*Never commit client data or external project architecture to the core `rbot` engineering brain.*

## 2. Active Domains & Workspaces

### 2.1 rbot Internal Engineering
*   **Workspace Slug:** `rbot-engineering`
*   **Description:** The canonical "Second Brain" for the development, architecture, and deployment of the `rbot` system itself.
*   **Master Index:** `INDEX__rbot_master_map__v1.0.md`

### 2.2 [Template: Client or Future Project]
*   **Workspace Slug:** `[project-slug]`
*   **Description:** [Brief description of the domain]
*   **Master Index:** `INDEX__[project-slug]_master_map__v1.0.md`

## 3. Operational Discipline
When Ross spins up a new project, a new Workspace must be created in the `rbot-core` UI, and this Global Directory must be updated with the new Slug and Master Index reference.