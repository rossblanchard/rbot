## rbot high level system diagram

````mermaid

flowchart TD
    %% Define external actors and services
    Ross([Ross - Laptop/Mobile])
    
    subgraph External Cloud Services
        Slack[Slack Workspace]
        LLM[OpenAI / Anthropic / Google APIs]
        GDrive[Google Drive]
    end

    subgraph Cloudflare Edge
        CF[Cloudflare Tunnel + Zero Trust OTP]
    end

    subgraph Raspberry Pi 4 Host
        
        subgraph Docker Bridge Network
            RBOT[rbot Container\AnythingLLM UI & API]
            OFFICE[rbot-office Container\Python Multi-Agent Swarm]
        end
        
        subgraph Host Storage Volumes
            DB[(rbot_storage\SQLite & Vector DB)]
            CONF[(rbot-office-config\Personas & config.yaml)]
        end
    end

    %% Routing and Connections
    
    %% Web UI Path
    Ross == 1. Web Access ==> CF
    CF == 2. Proxied HTTP ==> RBOT
    RBOT <--> DB
    
    %% Slack Swarm Path
    Ross == 1. Slack Chat ==> Slack
    OFFICE == 2. Socket Mode (Outbound) ==> Slack
    OFFICE --> CONF
    
    %% Agent API Calls
    OFFICE == 3. LLM Processing ==> LLM
    OFFICE == 4. Write Artifacts ==> GDrive
    
    %% The RAG Bridge
    OFFICE <== 5. Internal REST API\nCommit & Search Memory ==> RBOT

    %% Styling
    classDef primary fill:#2563eb,stroke:#1e40af,stroke-width:2px,color:#fff;
    classDef secondary fill:#059669,stroke:#047857,stroke-width:2px,color:#fff;
    classDef storage fill:#d97706,stroke:#b45309,stroke-width:2px,color:#fff;

    class RBOT,OFFICE primary;
    class Slack,LLM,GDrive,CF secondary;
    class DB,CONF storage;

````

--- END OF FILE
