
# 🧠 rbot: Sovereign "Second Brain" & Omnichannel AI Platform

Welcome to **rbot** — a highly modular, decoupled, multi-agent AI ecosystem designed to run entirely on a localized Raspberry Pi 4 homelab. 

Architected by Ross Blanchard and Archie (an AI Systems Architect), the `rbot` system solves two massive problems with modern AI tools: **Amnesia** and **Subscription Fatigue**.

1. **The Amnesiac AI Problem:** By permanently separating the Cognitive Engine (LLM APIs) from the Vector Memory (AnythingLLM) and the Collaboration Interface (Slack), `rbot` provides an omnichannel, context-aware AI team that retains permanent memory of past architectural decisions, code reviews, and project specs.
2. **The Economic Problem:** Instead of paying $20+ a month for locked-in subscriptions to multiple AI chat products, `rbot` operates on a highly economical **Pay-As-You-Go** model. You can switch between flagship providers (Google Gemini, OpenAI, Anthropic) on the fly. Furthermore, the system's modularity allows simple, low-complexity agentic personas to be routed to local, self-hosted LLMs (like Ollama), driving inference costs down to absolute zero.

## 🏗️ High-Level Architecture

The system utilizes an **Interface Segregation** pattern, allowing for two distinct ways to interact with the AI depending on the cognitive load of the task. Both interfaces read and write to the exact same memory brain, and both can mix-and-match LLM providers seamlessly.

1. **The Solo Workbench (`rbot-core`):** A fast, distraction-free Web UI (powered by AnythingLLM) secured behind a Cloudflare Zero Trust tunnel. Ideal for administration, solo research, document uploading, and rapid chatting with any major LLM API.
2. **The Collaborative Swarm (`rbot-office`):** A headless Python orchestration engine connected to Slack via outbound WebSockets. Ideal for multi-human, multi-agent collaboration, autonomous tool execution, and code review.

```mermaid
graph TD
    subgraph "Hardware: Raspberry Pi 4"
        subgraph "Docker Engine"
            subgraph "Docker Bridge Network (rbot-network)"
                ALLM[Container: rbot-core<br/>AnythingLLM / Vector DB<br/>Port 3001]
                OFFICE[Container: rbot-office<br/>Headless Python Swarm<br/>No Exposed Ports]
            end
            
            VOL1[(Volume: rbot-storage)]
            VOL2[(Volume: rbot-office-config)]
        end
    end

    %% Internal Connections
    ALLM --- VOL1
    OFFICE --- VOL2
    OFFICE <-->|REST API via Docker DNS| ALLM

    %% External Interfaces
    USER_SOLO([Ross Blanchard: Browser/Mobile]) -->|HTTPS / Zero Trust| CF[Cloudflare Tunnel]
    CF -->|Local Ingress| ALLM

    USER_COLLAB([Team Collaboration]) <-->|Slack UI| SLACK[Slack Workspace]
    SLACK <-->|Outbound Socket Mode| OFFICE

    %% External Services
    ALLM -->|API Chat| LLMS[Cognitive Engines:<br/>Gemini, OpenAI, Anthropic, Ollama]
    OFFICE -->|API Function Calling| LLMS
    OFFICE -->|Extended Python Tools| TOOLS[External APIs / Scripts]
    ALLM -.->|Standard Native Tools| TOOLS
```

## 🔍 Detailed System Topology & Execution Flow

When a user interacts with the `rbot-office` collaborative swarm, the system dynamically routes the request, loads the appropriate persona, and executes a multi-step reasoning loop using the currently selected LLM provider.

```mermaid
flowchart TB
    %% External Actors
    UserSolo([Ross Blanchard: Browser/Mobile])
    UserCollab([Team Collaboration])

    %% Public Cloud Services & Frontends
    subgraph Cloud Ecosystem
        Slack["Slack Workspace<br>(Collaborative Swarm UI)"]
        LLMs["Cognitive Engines<br>(Gemini / OpenAI / Anthropic / Ollama)"]
        GDrive["Google Drive API<br>(Folder: rbot)"]
        WWW["Live Internet<br>(DuckDuckGo Engine)"]
    end

    %% Edge Security
    subgraph Edge
        CF["Cloudflare Tunnel<br>Zero Trust Email OTP"]
    end

    %% Local Hardware (Raspberry Pi)
    subgraph Raspberry Pi 4 Host

        subgraph DockerBridge ["Docker Bridge Network (rbot-network)"]
            
            %% rbot-office (Python Swarm)
            subgraph Office["rbot-office Container (Python Orchestrator)"]
                Socket["Slack Socket Mode<br>Listener"]
                Router{"Persona Router<br>(Keyword Parse)"}
                Personas[("Markdown Personas<br>archie.md, qa.md, pm.md")]
                ExecLoop(("Multi-Step<br>Execution Loop"))
                
                subgraph Tools ["Tool Execution Engine"]
                    T_Web["search_web<br>(Scraper)"]
                    T_Drive["save_to_drive<br>(Memory Streamer)"]
                    T_Read["search_rag<br>(Context Fetch)"]
                    T_Write["commit_to_rag<br>(Embed & Store)"]
                end

                Socket -->|"Extract thread_ts & clean_text"| Router
                Router <-->|"Load System Prompt"| Personas
                Router -->|"Pass Context & Identity"| ExecLoop
                ExecLoop <-->|"Trigger & Read Results"| Tools
            end

            %% rbot-core (AnythingLLM)
            subgraph Core ["rbot-core Container (AnythingLLM)"]
                API["AnythingLLM Web UI & REST API<br>(Port 3001)"]
                
                subgraph VectorDatabases["Vector Databases (Isolated State)"]
                    DB_A[("my-workspace")]
                    DB_Q[("qa")]
                    DB_P[("pm")]
                end
                
                API <--> DB_A & DB_Q & DB_P
            end
            
        end
    end

    %% --- Data Flow Routing ---

    %% Front-End Interactions
    UserCollab == "1a. Multi-Agent Chat" ==> Slack
    UserSolo == "1b. Fast Solo Chat & RAG Admin" ==> CF
    CF -. "Proxied HTTPS<br>(Non-Collaborative UI)" .-> API
    
    %% Slack to Python (Bypassing Cloudflare)
    Slack == "2. Outbound WSS<br>(Event Push)" ==> Socket

    %% AI Cognitive Loop
    ExecLoop == "3. Context + Tool Schemas" ==> LLMs
    LLMs == "4. JSON Function Calls" ==> ExecLoop
    API -. "Direct API Chat" .-> LLMs
    
    %% External Tool Execution
    T_Web -- "HTTP Scraping" --> WWW
    T_Drive -- "Headless OAuth 2.0" --> GDrive
    
    %% Internal Tool Execution (The RAG Bridge)
    T_Read -- "http://rbot:3001/api/v1/workspace/{slug}/chat" --> API
    T_Write -- "http://rbot:3001/api/v1/document/raw-text" --> API

    %% Styling
    classDef primary fill:#1e40af,stroke:#93c5fd,stroke-width:2px,color:#fff;
    classDef tools fill:#047857,stroke:#6ee7b7,stroke-width:2px,color:#fff;
    classDef database fill:#b45309,stroke:#fcd34d,stroke-width:2px,color:#fff;
    classDef gateway fill:#475569,stroke:#cbd5e1,stroke-width:2px,color:#fff;

    class ExecLoop,Router,Socket primary;
    class T_Web,T_Drive,T_Read,T_Write tools;
    class DB_A,DB_Q,DB_P,Personas,VOL1,VOL2 database;
    class CF,API,Slack gateway;
```

## ✨ Core Features

- **Provider Agnostic & Economical:** Switch freely between Google Gemini, OpenAI, and Anthropic APIs on the fly in both the Web UI and the Slack Swarm. Route simple tasks to local LLMs (like Ollama) to reduce inference costs to zero, escaping the $20/month subscription trap.
- **Omnichannel RAG Persistence:** Decisions made in a Slack thread can be autonomously summarized by the AI (`commit_to_rag` tool) and pushed directly into the central vector database. Those memories can later be recalled in Slack (`search_rag` tool) or directly in the Web UI.
- **Dynamic Persona Routing:** The Slack swarm isn't just one bot. By analyzing keyword triggers (e.g., `archie`, `qa`, `pm`), the Python engine dynamically hot-swaps system prompts and routes queries to strictly segregated vector databases to prevent cross-persona hallucinations (Identity Dysmorphia).
- **Role-Based Access Control (RBAC):** Critical infrastructure tools (like writing to Google Drive or committing to the RAG database) are cryptographically locked to a specific Slack Admin ID.
- **Headless Tool Execution:** The Python swarm utilizes headless OAuth to stream finalized markdown documents and system specs directly from RAM to the `rbot` Google Drive folder, bypassing brittle SD card writes.
- **Multi-Step Reasoning Loops:** The Python orchestrator utilizes a `while` execution loop, allowing the active cognitive engine to chain multiple tools together (e.g., *Search the Live Web -> Read the Results -> Synthesize a Spec -> Commit to RAG*) entirely autonomously.

## 📂 Repository Structure

This repository is split into two primary domains:

- `/docs`: Canonical markdown artifacts, architectural diagrams, memory reflections (`MEM__`), and operational runbooks. Designed to be ingested directly by the RAG engine.
- `/rbot-office`: The core Python orchestration codebase, including the Slack Socket Mode listener, local tool scripts, and Markdown persona definitions.

## 🔒 Security Philosophy (Zero Trust)

This system is designed with extreme paranoia regarding inbound connections to the homelab:
1. The `rbot-core` Web UI exposes zero public ports. It is exclusively routed through a **Cloudflare Tunnel** and protected by a Zero Trust Email OTP challenge.
2. The `rbot-office` Slack integration uses **Socket Mode** (outbound WebSockets). Slack's servers cannot initiate inbound webhook requests to the Raspberry Pi.
3. The internal REST API communication between the Swarm and the Vector Database happens entirely within an isolated Docker Bridge network.

## 🚀 Built With
- **Hardware:** Raspberry Pi 4 (8GB)
- **RAG/Vector DB:** [AnythingLLM](https://anythingllm.com/) (`rbot-core`)
- **Orchestration:** Python 3.11+, Slack Bolt SDK (`rbot-office`)
- **Cognitive Engines:** Google GenAI SDK (Gemini), OpenAI API, Anthropic API, Ollama (Local)
- **Tooling:** DuckDuckGo (`ddgs`), Google Drive API
