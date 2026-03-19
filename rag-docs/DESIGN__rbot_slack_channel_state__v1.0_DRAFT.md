# DESIGN__rbot_slack_channel_state__v1.0_DRAFT.md

**Document Author:** Archie
**System Architects:** Ross Blanchard, Archie
**Date:** March 19, 2026
**Status:** PROVISIONAL / DRAFT (Pending Code Update)

## 1. Feature Overview: Channel-Bound Conversational State
Currently, the `rbot-office` Python Swarm binds conversational memory and state to Slack's `thread_ts` (Thread Timestamp). Ross identified a severe UX degradation with this approach: Slack threads cannot be named, leading to a cluttered, unsearchable UI for long-running architectural discussions.

To resolve this, Ross and Archie have decided to refactor the Python state management to bind conversational history to the `channel_id` rather than the thread ID. 

## 2. The Ephemeral Workspace Protocol
By moving to channel-bound state, the system relies on a strict operational protocol to prevent LLM context pollution:

1.  **Instantiation (One Topic per Channel):** Users spin up an ephemeral, topic-specific channel (e.g., `#task-auth-refactor` or `#spec-db-migration`). 
2.  **Execution:** All human-to-AI and human-to-human collaboration happens in the main channel view. No parallel topics are allowed in the same channel.
3.  **The Wrap-Up:** Once the objective is complete, the user invokes the AI (e.g., `@pm`) to execute the `commit_to_rag` tool, summarizing the channel's decisions and permanently pushing them to the `rbot-core` Vector Database (AnythingLLM).
4.  **Archival:** The Slack channel is archived to keep the workspace clean, knowing the memory is safely stored in the Second Brain.

## 3. Technical Implementation
*   **Current State:** The Python Swarm maintains a rolling dictionary of message histories keyed by `thread_ts`. 
*   **Required Change:** Update the Slack event listener payload extraction. The Swarm must ignore `thread_ts` and instead append user/assistant messages to a history array keyed by `channel_id`.
*   **Constraint:** If users continue to use threads inside these channels out of habit, the bot must be programmed to either ignore threaded messages or collapse them into the main channel context window to avoid state fragmentation.

## 4. Tradeoffs
*   **Tradeoff:** Moving away from threads means multiple independent conversations cannot happen simultaneously in a channel like `#general` without the LLM combining the contexts and hallucinating.
*   **Resolution:** Enforcing the "Ephemeral Workspace Protocol" mitigates this entirely. Channels are treated as disposable whiteboards; AnythingLLM is the permanent filing cabinet.
