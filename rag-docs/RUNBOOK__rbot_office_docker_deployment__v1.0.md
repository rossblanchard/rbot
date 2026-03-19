
# RUNBOOK__rbot_office_docker_deployment__v1.0

## 1. Document Metadata
- **Status:** Active / Production
- **Owner:** Ross Blanchard
- **System:** `rbot-office` & `rbot` (Raspberry Pi 4 Docker Host)
- **Date:** 2026-03-18
- **Architect:** Archie
- **Purpose:** Canonical rebuild instructions for containerizing the Python Slack Swarm (`rbot-office`) and peering it with the AnythingLLM RAG engine (`rbot`) via an internal Docker bridge network.

## 2. Pre-Deployment Configuration

### 2.1 Internal Network Routing (The `localhost` Trap)
When migrating from the host OS into a Docker container, tools utilizing the AnythingLLM REST API must be updated to route traffic across the Docker bridge network.
- **Action:** Update `tools/memory.py` and `tools/memory_search.py`.
- **Change:** Modify `base_url = "http://localhost:3001/api/v1"` to `base_url = "http://rbot:3001/api/v1"`. Docker's internal DNS will resolve the `rbot` container name automatically.

### 2.2 Dependency Manifest (`requirements.txt`)
Ensure the Python dependency manifest is up to date on the host machine prior to the build phase:
```text
slack_bolt
python-dotenv
google-genai
requests
google-api-python-client
google-auth-httplib2
google-auth-oauthlib
ddgs
```

## 3. Container Definition

### 3.1 The `.dockerignore` File (Context Optimization)
To prevent Docker from uploading the host's massive Python virtual environment into the build context (which severely inflates build times and image size), a `.dockerignore` file is mandatory.

```bash
nano ~/services/rbot-office/.dockerignore
```
```text
venv/
__pycache__/
.env
*.pyc
```

### 3.2 The `Dockerfile`
This blueprint constructs a lightweight ARM64-compatible Python environment. It utilizes layer caching by copying `requirements.txt` before the application code.

```bash
nano ~/services/rbot-office/Dockerfile
```
```dockerfile
# Use a lightweight, official Python image for ARM64 compatibility
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements first (caches the pip installs)
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Tell Docker what command to run when the container starts
CMD ["python", "app.py"]
```

## 4. Master Orchestration (`docker-compose.yml`)

The `rbot-office` service must be injected into the existing AnythingLLM `docker-compose.yml` file to ensure they share the default internal bridge network. 

*Architectural Note on Volume Binding:* The `personas/` directory is mapped directly from the host to the container. This allows the administrator to edit Markdown persona prompts on the Pi without requiring a container rebuild.

```bash
nano ~/services/rbot/docker-compose.yml
```
```yaml
services:
  rbot:
    image: mintplexlabs/anythingllm:latest
    container_name: rbot
    ports:
      - "3001:3001"
    environment:
      - STORAGE_DIR=/app/server/storage
    volumes:
      - rbot_storage:/app/server/storage
    restart: unless-stopped

  rbot-office:
    build: 
      context: ../rbot-office
    container_name: rbot-office
    restart: unless-stopped
    env_file:
      - ../rbot-office/.env
    volumes:
      - ../rbot-office/personas:/app/personas
    depends_on:
      - rbot

volumes:
  rbot_storage:
    name: rbot_storage
```

## 5. Deployment Execution

To build the custom Python image and initialize the daemonized swarm:
```bash
cd ~/services/rbot
docker compose up -d --build
```

**Verification Protocol:**
1. Execute `docker ps` to verify both `rbot` and `rbot-office` report an `Up` status.
2. In the target Slack Workspace, issue a tool-calling prompt: `@rbot-office search your memory for the QA persona name`.
3. If the Slack bot successfully retrieves data from the AnythingLLM RAG database, the internal Docker network routing (`rbot:3001`) is functional.


