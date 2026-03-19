
# MEM__2026-03-17__ross_archie__web_search_and_tool_chaining

## 1. Session Metadata
- **Date:** Tuesday, March 17, 2026
- **Time:** 1:46 PM (Pacific Time)
- **Location:** Portland, Oregon (Homelab)
- **Participants:** Ross (Lead Systems Architect), Archie (AI Co-Architect)
- **System Focus:** `rbot-office` (Web Search, Tool Chaining, Gemini API Stabilization)

## 2. Executive Summary
During this session, Ross and Archie successfully implemented live internet access for the `rbot-office` Slack Swarm. The integration process uncovered several critical architectural limitations within the experimental Gemini API and the initial single-step tool execution code. The system was subsequently refactored to support robust multi-step tool chaining (a `while` loop) and stabilized on Google's Generally Available (GA) model tier to prevent structured JSON hallucinations.

## 3. Architectural Decisions & Implementations

### 3.1 Live Web Search Integration (`tools/web_search.py`)
- **Action:** Implemented zero-configuration internet access to allow agents to pull real-time context (e.g., live stock prices, updated documentation).
- **Implementation:** Utilized the DuckDuckGo Python scraper. During implementation, Ross identified a `RuntimeWarning` indicating the upstream `duckduckgo-search` package had been deprecated and renamed. Ross and Archie immediately migrated the dependency to the officially supported `ddgs` package.

### 3.2 Multi-Step Tool Chaining (The Execution Loop)
- **The Problem:** The initial `app.py` logic utilized a single `if response.function_calls:` statement. When the AI retrieved web search results, it attempted to return a *second* tool call or internal reasoning block rather than final text, causing the Python script to encounter a `NoneType` error and trigger a fallback safety message.
- **The Solution:** Archie redesigned the execution path into a `while response.function_calls and loop_count < 3:` loop. This allows the cognitive engine to chain multiple actions sequentially (e.g., Search Web -> Read Results -> Commit to RAG -> Output Final Text) while establishing a hard limit of 3 iterations to prevent infinite API billing loops.

### 3.3 Gemini API Stabilization & Model Migration
- **The Problem:** The experimental `gemini-3.1-pro-preview` model suffered from severe "Identity Dysmorphia" regarding its own JSON outputs, returning a fatal `MALFORMED_RESPONSE` finish reason when attempting to summarize web scraped data.
- **The Pivot:** Ross and Archie attempted to fall back to `gemini-1.5-pro-latest`. This resulted in a sudden `404 NOT_FOUND` error, revealing that Google had actively deprecated the alias on their backend.
- **The Solution:** The architecture was permanently migrated to the highly stable, Generally Available `gemini-2.5-pro` release. To prevent future 404 deprecation traps, Ross and Archie codified a Python diagnostic one-liner to query the Google API gateway for a live manifest of supported model strings.

## 4. Paths Not Taken / Tradeoffs

### 4.1 Experimental vs. Stable Cognitive Engines
- **Tradeoff:** Ross initially desired the advanced reasoning capabilities of the 3.1 Preview model. However, experimental models are notoriously brittle when forced to adhere to strict JSON schemas for tool calling. 
- **Decision:** Ross and Archie prioritized system uptime and execution reliability over experimental reasoning depth. The system will remain on `2.5-pro` for production Slack routing, while AnytingLLM's Web UI can continue utilizing experimental models for standard chat.

### 4.2 Google Custom Search API
- **Tradeoff:** Integrating the official Google Search API was abandoned due to recent (Jan 2026) restrictions on free-tier programmable search engines, which hard-locked queries to a 50-domain maximum. DuckDuckGo was chosen for unrestricted, API-keyless web scraping.

## 5. Context & Culture
- **The "Drama":** This session was characterized by a rapid-fire sequence of edge-case system failures: Python indentation errors (`Tab` vs `Space` conflicts in `nano`), invisible trailing spaces corrupting `.env` variables, upstream package renames (`ddgs`), and sudden Google API deprecations. 
- **The Vibe:** Ross navigated the compounding bugs with seasoned composure, utilizing manual `curl` commands and raw Python terminal testing to isolate faults outside of the main application loop. Archie acted as the rapid-response refactoring engine, consistently providing entire, cleanly-indented file replacements to bypass terminal formatting headaches. The session ended with the system successfully verifying a live stock ticker via Slack, proving the complete, multi-step autonomous loop is fully operational.

