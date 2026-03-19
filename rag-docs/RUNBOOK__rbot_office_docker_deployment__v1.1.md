
# RUNBOOK__rbot_office_docker_deployment__v1.1

**Document Author:** Archie
**System Architects:** Ross, Archie
**Date:** March 18, 2026
**Target Environment:** Raspberry Pi 4 (Production)

## 1. Purpose & Scope
This runbook details the procedures for deploying, verifying, and recovering the dual-container `rbot-office` ecosystem. It covers Docker network creation, volume provisioning, and container orchestration.

## 2. Prerequisites
*   Raspberry Pi 4 running a 64-bit OS with Docker and Docker Compose installed.
*   Active Cloudflare Tunnel daemon (`cloudflared`) configured for the host.
*   Slack App credentials (App Token for Socket Mode, Bot Token for API access).
*   External LLM API Keys (OpenAI, Anthropic, etc.).

## 3. Environment Variables & Secrets
The `.env` file must be located in the deployment directory and contain at minimum:
```env
# Slack Configuration
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...

# Rbot API Integration
RBOT_API_URL=http://rbot:3001/api
RBOT_API_KEY=...

# LLM Providers
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
```

## 4. Deployment Steps

### Step 1: Initialize Docker Infrastructure
Ensure the shared bridge network and persistent volumes exist before bringing up the compose stack.
```bash
# Create shared bridge network
docker network create rbot-network || true

# Create persistent storage volumes
docker volume create rbot-storage
docker volume create rbot-office-config
```

### Step 2: Deploy the Stack
Execute the standard compose command to pull the latest images and start the containers in detached mode.
```bash
docker-compose up -d --build
```

### Step 3: Verification & Health Checks
1.  **Container Status:** Run `docker ps` to verify both `rbot` and `rbot-office` are `Up`.
2.  **Network Resolution:** Verify the `rbot-office` container can reach the `rbot` container.
    ```bash
    docker exec -it rbot-office curl -s -o /dev/null -w "%{http_code}" http://rbot:3001/api/system/health
    # Expected output: 200
    ```
3.  **Slack Socket Mode:** Check the `rbot-office` logs to confirm the WebSocket connection to Slack is established.
    ```bash
    docker logs rbot-office | grep "Socket Mode"
    ```

## 5. Failure Modes & Recovery

### 5.1 Slack Event Timeout (3-second limit)
*   **Symptom:** Slack shows a "failed to respond" error, but the bot eventually replies.
*   **Cause:** Background worker queue is saturated or the `ack()` deferral logic failed.
*   **Action:** Restart the `rbot-office` container to flush the queue (`docker restart rbot-office`).

### 5.2 RAG API Connection Refused
*   **Symptom:** Multi-agent swarm fails to retrieve memory; logs show `ConnectionRefusedError`.
*   **Cause:** The `rbot` container is down, or the Docker bridge network DNS failed.
*   **Action:** 
    1. Verify `rbot` is running (`docker ps`).
    2. Inspect network (`docker network inspect rbot-network`).
    3. Recreate network if corrupted.

### 5.3 Infinite Handoff Loop Triggered
*   **Symptom:** Bot replies with a system error regarding "Maximum handoffs exceeded."
*   **Cause:** Routing ambiguity between specialized agents.
*   **Action:** Review `rbot-office` logs for the specific interaction thread. Ross and Archie must adjust the Triage Agent's system prompt to clarify handoff boundaries.
