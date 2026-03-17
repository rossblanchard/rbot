# PROJECT__job_application_orchestrator__System_Architecture_v1

## 1. Overview

### 1.1 Purpose
The Job Application Orchestrator (JAO) is a human-in-the-loop workflow system designed to semi-automate the process of preparing and tracking job applications.

The system assists with:
- Tailoring a structured resume (JSON-based) to a specific job description
- Generating a role-specific cover letter draft
- Rendering resume artifacts (HTML → PDF)
- Producing formatted cover letter documents (PDF or DOCX)
- Creating draft Jira work items for tracking
- Persisting application artifacts in cloud storage (e.g., OneDrive or Google Drive)

The system does not autonomously apply to jobs. All modifications and actions require explicit user approval.

---

## 2. Design Principles

1. Human-in-the-Loop Control  
   No resume edits, file writes, or Jira actions occur without user confirmation.

2. Deterministic Execution Layer  
   LLMs propose structured outputs. The system applies changes deterministically.

3. Structured Data First  
   Resume data remains canonical in JSON format.

4. Idempotent Operations  
   Re-running a workflow step should not corrupt artifacts or duplicate Jira records.

5. Local-First Architecture  
   The system runs locally (initially on macOS), with optional later deployment to Raspberry Pi.

6. Explicit Tool Boundaries  
   LLM agents do not directly access filesystem or external APIs.

---

## 3. High-Level Architecture

```
User (CLI or Minimal Web UI)
        ↓
Workflow Orchestrator
        ↓
ATS Optimization Agent (LLM)
        ↓
Structured Output (validated schema)
        ↓
User Approval Gate
        ↓
Tool Execution Layer
    - Resume JSON patch application
    - Resume rendering (HTML → PDF)
    - Cover letter document generation
    - Cloud storage upload
    - Jira draft ticket creation
        ↓
Application Log + Artifact Registry
```

---

## 4. Core Components

### 4.1 Workflow Orchestrator

Responsibilities:
- Manage application lifecycle state
- Invoke LLM agent
- Validate structured output
- Present diffs to user
- Trigger tool execution upon approval

State model (initial version):
- INIT
- JOB_ANALYZED
- PROPOSED_CHANGES_READY
- APPROVED
- ARTIFACTS_GENERATED
- JIRA_DRAFT_CREATED
- COMPLETED

Persistence: SQLite or structured JSON log.

---

### 4.2 ATS Optimization Agent

Role:
Simulates an HR professional with Applicant Tracking System (ATS) knowledge.

Inputs:
- Job description text
- Canonical resume JSON

Outputs (strict schema):
- resume_patch (structured JSON diff)
- suggested_keywords
- cover_letter_draft (markdown or plain text)
- rationale_summary

Constraints:
- Must not rewrite entire resume blindly
- Must return structured, schema-valid output

---

### 4.3 Resume Patch Engine

Responsibilities:
- Validate resume_patch against schema
- Apply patch deterministically
- Preserve unchanged resume sections
- Prevent destructive overwrites

Failure Modes:
- Invalid schema
- Field mismatch
- Excessive deletion attempts

Mitigation:
- Strict JSON schema validation
- User preview before commit

---

### 4.4 Rendering Layer

Inputs:
- Updated resume JSON
- Existing HTML renderer (prebuilt system)

Outputs:
- Resume HTML
- Resume PDF

Cover Letter:
- Convert draft to PDF or DOCX
- Apply consistent formatting template

---

### 4.5 Jira Integration Layer

Responsibilities:
- Create draft Jira issue
- Populate fields:
  - Company name
  - Job title
  - Job description
  - Resume artifact path
  - Cover letter artifact path

Constraints:
- Draft state only
- Prevent duplicate ticket creation

Integration Method:
- Jira REST API
- Token-based authentication

---

### 4.6 Cloud Storage Integration

Target Providers:
- OneDrive (preferred if primary storage)
- Google Drive (alternative)

Responsibilities:
- Upload artifacts
- Maintain structured folder hierarchy

Example hierarchy:
```
Job Applications/
    2026/
        Company_Name/
            resume.pdf
            cover_letter.pdf
            job_description.txt
```

---

## 5. Technology Stack (Initial)

Language: Python  
Interface: CLI (v1)  
LLM Provider: OpenAI API  
State Persistence: SQLite  
Resume Renderer: Existing JSON → HTML system  
PDF Generation: WeasyPrint or wkhtmltopdf  
Cloud APIs: Microsoft Graph API or Google Drive API  
Jira Integration: Jira REST API

---

## 6. Security and Privacy Considerations

- API keys stored in environment variables
- No plaintext secrets in codebase
- Local logs must not expose sensitive tokens
- Resume data treated as confidential
- No autonomous submission of applications

---

## 7. Failure Modes and Mitigations

| Failure Mode | Mitigation |
|--------------|------------|
| LLM produces invalid JSON | Strict schema validation + retry |
| Resume corruption | Patch preview + user approval |
| Duplicate Jira tickets | Idempotency check via application ID |
| Cloud upload failure | Retry with exponential backoff |
| Partial workflow completion | Persist state after each step |

---

## 8. Non-Goals (v1)

- Autonomous job discovery
- Auto-submitting applications
- Multi-agent internal debates
- Continuous background monitoring
- SaaS-hosted orchestration

---

## 9. Milestones

### Milestone 1
CLI tool that:
- Accepts job description
- Generates resume_patch + cover letter
- Displays structured diff

### Milestone 2
Patch application + artifact rendering

### Milestone 3
Jira draft creation

### Milestone 4
Cloud storage integration

---

## 10. Future Extensions

- Multiple persona evaluators (ATS + Hiring Manager)
- Ranking job fit score
- Analytics dashboard for application pipeline
- Web UI
- Deployment to Raspberry Pi for centralized access

---

## 11. Architectural Status

Status: Conceptual Architecture Approved  
Date: 2026-03-09  
Owner: Ross Blanchard  
System Architect: Archie

This document defines the canonical v1 architecture for the Job Application Orchestrator and is intended to serve as the authoritative reference for future implementation and iteration.
