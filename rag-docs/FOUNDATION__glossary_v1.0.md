

# Ross Brain – Domain Glossary  
Version: 1.0  
Created: 2026-03-09 UTC  
Owner: Ross Blanchard  

---

## 1. Purpose

This glossary defines standardized terminology used within the Ross Brain system and related engineering projects.  

Its purpose is to:

- Ensure consistent terminology across documentation
- Improve retrieval quality within the RAG system
- Reduce ambiguity in architectural discussions
- Serve as a semantic foundation for future canonical documents

All future documentation must use these terms consistently.

---

## 2. Core System Terms

### Ross Brain

The structured, persistent engineering knowledge base maintained within AnythingLLM.  

Ross Brain consists of:
- Canonical documentation artifacts
- Structured project documentation
- Architecture summaries
- Decision logs
- Glossaries
- AI/ML specifications
- Infrastructure documentation

Ross Brain is optimized for retrieval using vector search (RAG).

---

### Archie

The AI assistant operating within the AnythingLLM environment.

Role:
- Senior systems architect
- Software engineer
- AI/ML advisor
- Documentation discipline enforcer
- Knowledge base curator

Archie is responsible for encouraging structured documentation and milestone formalization.

---

### AnythingLLM

The locally hosted LLM orchestration application running inside a Docker container on a Raspberry Pi 4 (8GB), accessible at:

```
rbot.rossblanchard.com
```

Responsibilities:
- Chat interface
- Document ingestion
- Vector storage
- Retrieval-augmented generation (RAG)
- System prompt management

---

### Workspace

A logical container within AnythingLLM that includes:

- System prompt configuration
- Documents
- Vector database
- Chat sessions

Current state:
- Single workspace used for all Ross Brain activities

---

### Canonical Documentation

Formal, structured, self-contained documents created to preserve finalized architectural knowledge.

Examples:
- Architecture Summary
- API Contract
- Decision Log
- AI/ML Pipeline Specification
- Infrastructure Specification
- Domain Glossary
- Operational Runbook
- Postmortem

Canonical documentation must:
- Avoid conversational phrasing
- Use consistent terminology
- Be optimized for vector retrieval
- Stand alone without chat context

---

## 3. Knowledge System Terms

### RAG (Retrieval-Augmented Generation)

A pattern where:

1. Documents are chunked
2. Chunks are embedded into vectors
3. Relevant chunks are retrieved at query time
4. Retrieved content is injected into the model prompt

RAG does not modify model weights.  
It augments prompts dynamically.

---

### Embedding

A numerical vector representation of text used for semantic similarity search.

Embeddings are generated during document ingestion and stored in the workspace vector database.

---

### Vector Database

The storage layer that holds embedded document chunks and enables semantic search.

Used to retrieve relevant knowledge during chat sessions.

---

### Chunk

A segmented portion of a document used for embedding and retrieval.

Chunks should:
- Be semantically coherent
- Be self-contained
- Contain explicit terminology
- Avoid ambiguous references

---

## 4. Architectural Discipline Terms

### Architecture Summary

A formal document describing:

- System purpose
- Scope
- High-level design
- Core components
- Data flow
- Dependencies
- Constraints
- Failure modes
- Evolution path

It represents a stabilized architectural state.

---

### Decision Log

A structured record of an architectural decision including:

- Context
- Options considered
- Chosen approach
- Rationale
- Tradeoffs
- Consequences
- Revisit conditions

Decision logs prevent historical ambiguity.

---

### Provisional Design

An exploratory idea not yet formalized as canonical documentation.

Must be explicitly marked as provisional.

---

### Stabilized Architecture

A design that has:
- Survived exploratory iteration
- Been accepted as the current direction
- Been captured in canonical documentation

---

## 5. Infrastructure Terms

### Local LLM Environment

The combination of:

- Raspberry Pi 4 (8GB)
- Docker runtime
- AnythingLLM container
- OpenAI API integration

This is the execution environment for Ross Brain.

---

### System Prompt

The persistent instruction layer configured at the workspace level that governs Archie’s behavior, tone, and documentation discipline.

---

## 6. Documentation Lifecycle

### Exploratory Discussion
Informal design conversation.

### Formalization
Conversion of stabilized ideas into canonical documentation.

### Persistence
Uploading finalized documentation into Workspace Documents for RAG ingestion.

### Retrieval
Future semantic lookup of stored knowledge during chat sessions.

---

## 7. Versioning Policy

When terminology changes:

- Update this glossary
- Increment version number
- Note date of modification
- Ensure dependent documents use updated terminology

---

# End of Glossary v1.0

