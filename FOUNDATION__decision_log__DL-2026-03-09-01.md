# Decision Log

## Decision ID  
DL-2026-03-09-01

## Title  
Adopt Prefix-Based Naming Convention Due to Flat Document Storage in AnythingLLM

## Date  
2026-03-09 UTC

## Status  
Accepted

---

## 1. Context

Ross Brain is implemented within a single AnythingLLM workspace running locally on a Raspberry Pi 4 (8GB).

During initial setup, it was observed that the Workspace Documents interface does not support true hierarchical folder storage. While the user interface may visually suggest folders, the underlying storage and vector indexing system treat documents as a flat collection.

As Ross Brain depends on structured, canonical documentation for Retrieval-Augmented Generation (RAG), a method is required to preserve logical grouping and semantic organization despite the flat storage constraint.

---

## 2. Problem Statement

AnythingLLM’s document storage model:

- Does not support true nested folder hierarchies
- Stores documents independently in a flat structure
- Embeds documents individually into the vector database
- Does not preserve directory semantics in retrieval

Without structural organization, the document corpus may become:

- Difficult to navigate
- Semantically inconsistent
- Harder to maintain
- Less predictable for long-term retrieval

A naming strategy is required to enforce logical categorization.

---

## 3. Options Considered

### Option A — Rely on UI Folder Structure

Use the visual folder feature in the AnythingLLM interface.

**Pros:**
- Minimal naming overhead

**Cons:**
- Not structurally enforced
- Does not affect vector storage
- Risk of inconsistency
- Misleading architectural abstraction

Rejected due to lack of true hierarchical enforcement.

---

### Option B — Create Separate Workspaces Per Category

Use multiple workspaces to simulate structure (e.g., Foundation, Projects, ML, Infra).

**Pros:**
- Clear separation
- Strong logical boundaries

**Cons:**
- Operational overhead
- Reduced cross-document retrieval
- Increased configuration complexity
- Premature multi-workspace architecture

Rejected due to unnecessary complexity at Ross Brain v1.0 stage.

---

### Option C — Adopt Prefix-Based Naming Convention (Selected)

Use standardized filename prefixes to simulate logical grouping in a flat document store.

Example:

- FOUNDATION__glossary_v1.0.md  
- PROJECT__<project_name>__architecture_summary.md  
- ML__pipeline_spec__<pipeline_name>.md  
- INFRA__deployment_architecture.md  

**Pros:**
- Enforces consistent categorization
- Improves visual sorting
- Improves semantic clarity
- Improves retrieval context via metadata
- Low operational complexity
- Scales as corpus grows

**Cons:**
- Requires discipline
- Slightly longer filenames

Selected as the most maintainable and scalable approach under platform constraints.

---

## 4. Decision

Ross Brain will use a standardized prefix-based naming convention for all canonical documentation stored in the AnythingLLM workspace.

Prefixes will indicate document category and logical grouping.

---

## 5. Naming Convention Standard (v1.0)

### Foundation Documents

FOUNDATION__<document_name>_v<version>.md

Example:
FOUNDATION__glossary_v1.0.md

---

### Project Documents

PROJECT__<project_name>__<document_type>.md

Examples:
PROJECT__ingestion_service__architecture_summary.md
PROJECT__ingestion_service__decision_log.md

---

### AI/ML Documents

ML__<document_type>__<artifact_name>.md

Example:
ML__pipeline_spec__document_embedding_pipeline.md

---

### Infrastructure Documents

INFRA__<document_name>.md

Example:
INFRA__deployment_architecture.md

---

## 6. Consequences

### Positive Consequences

- Improved navigability in flat document storage
- Clear logical grouping without folder dependency
- Better semantic clarity in vector metadata
- Long-term scalability of Ross Brain
- Reduced structural ambiguity

### Negative Consequences

- Requires manual discipline
- Slight increase in filename verbosity

---

## 7. Risks

- Naming drift if discipline is not maintained
- Inconsistent versioning practices
- Over-categorization in early stages

Mitigation:
- Enforce naming standards in future canonical documentation
- Update glossary if conventions evolve

---

## 8. Revisit Conditions

This decision should be revisited if:

- AnythingLLM introduces true hierarchical document storage
- Ross Brain expands to multiple workspaces
- Corpus size exceeds manageable limits within a flat structure
- A migration to an external document system (e.g., Git-backed knowledge base) occurs

---

## 9. Architectural Impact

This decision formalizes a structural constraint of AnythingLLM:

Workspace document storage is flat and does not support enforced hierarchy.

Ross Brain v1.0 will operate under this constraint using naming conventions as a structural abstraction layer.

---

# End of Decision Log DL-2026-03-09-01
