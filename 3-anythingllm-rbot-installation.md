# AnythingLLM (rbot) Installation Guide

## Environment
- Device: Raspberry Pi 4 (8GB RAM)
- OS: Raspberry Pi OS 64-bit (aarch64)
- Docker Engine installed and running
- Static DHCP reservation configured on router
- SSH hardened (key-based auth, password disabled)

---

# 1️⃣ Install Docker (If Not Already Installed)

```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
```

Log out and back in.

Verify:

```bash
docker version
```

Install Docker Compose plugin:

```bash
sudo apt install docker-compose-plugin -y
```

Verify:

```bash
docker compose version
```

Ensure Docker starts on boot:

```bash
sudo systemctl enable docker
sudo systemctl start docker
```

---

# 2️⃣ Create Project Directory

```bash
mkdir -p ~/services/rbot
cd ~/services/rbot
```

This directory contains all configuration for the rbot service.

---

# 3️⃣ Create docker-compose.yml

```bash
nano docker-compose.yml
```

Paste the following configuration:

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

volumes:
  rbot_storage:
```

### Important
The `STORAGE_DIR` environment variable is required in recent versions of AnythingLLM.
Without it, the container will fail to start and may risk data loss.

---

# 4️⃣ Start rbot

From inside `~/services/rbot`:

```bash
docker compose up -d
```

Verify container is running:

```bash
docker ps
```

View logs:

```bash
docker compose logs -f
```

---

# 5️⃣ Access AnythingLLM Locally

From a browser on the LAN:

```
http://<pi-local-ip>:3001
```

Initial setup:
- Create admin account
- Add OpenAI API key
- Select default model
- Create initial workspace

---

# 6️⃣ Verify Persistent Storage

1. Upload a small document.
2. Restart container:

```bash
docker compose restart
```

3. Confirm document still exists.

If it does, the Docker volume is functioning correctly.

---

# 7️⃣ Common Administration Commands

Start:
```bash
docker compose up -d
```

Stop:
```bash
docker compose down
```

Restart:
```bash
docker compose restart
```

View logs:
```bash
docker compose logs -f
```

Update to latest image:
```bash
docker compose pull
docker compose up -d
```

---

# ✅ Current State

- Docker installed and running
- rbot container operational
- Persistent storage configured
- Local access confirmed
- System ready for Cloudflare Tunnel setup
