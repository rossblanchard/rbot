

# SOP__slack_multi_agent_collaboration__v1.0

## 1. Document Metadata
- **Status:** Active
- **Owner:** Ross Blanchard
- **System:** `rbot-office` (Slack Interface)
- **Date:** 2026-03-16
- **Architect:** Archie
- **Purpose:** Defines the operational philosophy and user workflow for multi-agent collaboration within the Slack interface.

## 2. Core Philosophy: State Isolation via Threads
The `rbot-office` architecture relies on the Slack API's `conversations_replies` endpoint. 
To prevent the AI's context window from suffering "context collapse" (hallucinating details from unrelated conversations), the system enforces a strict **Thread-Only Memory Model**.

### The "Conference Room" Analogy
- **The Main Channel:** Treated as a loud, open-plan office. Used *only* to initiate new topics. The AI does not read the main channel's history.
- **The Thread:** Treated as a private conference room dedicated to a single project. The AI reads 100% of the messages inside the thread, allowing multiple humans and multiple AI personas to collaborate seamlessly with shared context.

## 3. The Multi-Agent Workflow

To successfully collaborate with the AI Swarm, users must adhere to the following workflow:

### Step 1: Initiating a Project (Main Channel)
To start a new task, tag the bot in the main channel and specify the desired persona.
> **Ross:** "@rbot-office archie, let's design a new database schema."
*(The system creates a new Thread. This establishes the context baseline).*

### Step 2: Single-Agent Iteration (In Thread)
Continue the conversation inside the newly created Thread. 
> **Ross:** "@rbot-office change the user table to include an email column."
*(Archie reads the thread history, sees the original design, and updates the schema).*

### Step 3: Multi-Agent Handoff (In Thread)
To bring another persona into the "Conference Room," tag the bot inside the *same* thread and specify the new persona.
> **Ross:** "@rbot-office qa, please review Archie's schema above for security flaws."
*(The QA persona wakes up, reads the entire thread including Archie's previous output, and provides a critique).*

### Step 4: Final Synthesis (In Thread)
Bring in a synthesis persona to finalize the output.
> **Ross:** "@rbot-office pm, gather the specs Archie and QA just agreed upon and generate Jira tickets."
*(The PM persona reads the entire debate, synthesizes the resolution, and outputs the tickets).*

## 4. Operational Constraints
- **Context Limits:** If a thread exceeds 50-100 messages, the context window may max out. Users should ask the bot to "Summarize and commit this to RAG," then start a fresh thread for the next phase of the project.
- **Cross-Thread Contamination:** Bots physically cannot see messages outside of the current thread. Do not ask a bot in Thread B about a decision made in Thread A unless it has been committed to the RAG database.

