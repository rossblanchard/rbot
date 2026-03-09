# FOUNDATION__chat_session_management_guidelines__v1

## 1. Purpose
Establish operational discipline for managing chat session length, scope, and architectural entropy within the Ross Brain system.

## 2. Problem Statement
Large, mixed-topic chat sessions degrade reasoning quality due to:
- Context saturation
- Topic drift
- Retrieval noise
- Conflicting historical assumptions

This document defines reset and snapshot policies to maintain clarity and system integrity.

## 3. Session Scope Rules
- Each chat session should focus on a single project or milestone.
- Do not mix unrelated architectural domains in one thread.
- Treat chats as working sessions, not permanent memory stores.

## 4. Stabilization Triggers
When any of the following occur, generate canonical documentation:
- Architectural direction finalized
- Tradeoff decision made
- Component boundaries defined
- System scope changes materially

After documentation is generated, begin a fresh chat thread for the next phase.

## 5. Entropy Indicators
Start a fresh thread if:
- Prior constraints are forgotten or contradicted
- Responses become vague or repetitive
- Multiple topic pivots occur
- Token usage grows substantially without added clarity

## 6. Operational Discipline
- Snapshot state into structured artifacts.
- Store finalized documents in Workspace Documents.
- Use RAG retrieval instead of relying on long conversational memory.
- Prefer smaller, milestone-scoped sessions.

## 7. Model Constraint Acknowledgment
The model cannot:
- Self-reset
- Track entropy autonomously
- Enforce thread boundaries

Session management discipline must be applied by the human operator.

## 8. Version
v1
Date: 2026-03-09
