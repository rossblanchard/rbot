# Cloudflare Tunnel + Zero Trust Setup for rbot

## Overview
This document describes the complete setup of a secure Cloudflare Tunnel for the self-hosted AnythingLLM instance (`rbot`) running on a Raspberry Pi in Portland, Oregon.

Architecture:

Internet
  ↓
Cloudflare Edge (TLS + Identity)
  ↓
Cloudflare Tunnel (Outbound Only)
  ↓
Raspberry Pi (No Open Ports)
  ↓
Docker
  ↓
rbot (AnythingLLM on port 3001)

---

# 1. Prerequisites

- Cloudflare account created
- Domain (rossblanchard.com) moved to Cloudflare DNS
- Nameservers updated and active
- rbot running locally at http://localhost:3001

---

# 2. Install cloudflared (Binary Method)

Removed failed apt repo method and installed standalone binary.

```bash
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64
mv cloudflared-linux-arm64 cloudflared
chmod +x cloudflared
sudo mv cloudflared /usr/local/bin/
```

Verify:

```bash
cloudflared --version
```

---

# 3. Authenticate Tunnel

```bash
cloudflared tunnel login
```

- Open provided URL in browser
- Select rossblanchard.com
- Approve

This creates:

```
~/.cloudflared/cert.pem
```

---

# 4. Create Tunnel

```bash
cloudflared tunnel create rbot-tunnel
```

Tunnel ID:

```
REDACTED
```

Credentials file created at:

```
/home/ross/.cloudflared/REDACTED.json
```

---

# 5. Create Tunnel Configuration

Create directory:

```bash
sudo mkdir -p /etc/cloudflared
```

Create config:

```bash
sudo nano /etc/cloudflared/config.yml
```

Contents:

```yaml
tunnel: REDACTED
credentials-file: /home/ross/.cloudflared/REDACTED.json

ingress:
  - hostname: rbot.rossblanchard.com
    service: http://localhost:3001
  - service: http_status:404
```

---

# 6. Create DNS Route

```bash
cloudflared tunnel route dns rbot-tunnel rbot.rossblanchard.com
```

This automatically creates the DNS record in Cloudflare.

---

# 7. Install Tunnel as System Service

```bash
sudo cloudflared service install
sudo systemctl start cloudflared
```

Verify:

```bash
sudo systemctl status cloudflared
```

Ensure:

- active (running)
- enabled

---

# 8. Configure Zero Trust Access

## Create Application

Cloudflare Dashboard → Zero Trust → Access → Applications → Add Application

Type: Self-hosted

Name: rbot
Domain: rbot.rossblanchard.com

---

## Create Access Policy

Policy Name: Allow Ross
Action: Allow
Rule Type: Emails
Condition: Equals
Value: Your email address

---

## Enable Authentication Method

Zero Trust → Settings → Authentication

Enabled:

- ✅ One-time PIN (Email OTP)

---

# 9. Verification

Open in private browser:

```
https://rbot.rossblanchard.com
```

Expected behavior:

1. Cloudflare Access login page appears
2. Email OTP required
3. After authentication → rbot loads

If rbot loads directly without login, configuration is incorrect.

---

# Security Properties Achieved

- No router port forwarding
- No inbound connections to home network
- Outbound-only encrypted tunnel
- TLS at Cloudflare edge
- Identity-aware access control
- Docker container isolated
- Persistent systemd service

---

# Operational Commands

Check tunnel:

```bash
sudo systemctl status cloudflared
```

Restart tunnel:

```bash
sudo systemctl restart cloudflared
```

Check rbot:

```bash
docker ps
```

View rbot logs:

```bash
docker logs -f rbot
```

---

# Current System State (March 2026)

- Raspberry Pi hardened
- Static IP configured
- Docker running
- AnythingLLM deployed as rbot
- Persistent storage configured
- Cloudflare Tunnel active
- Zero Trust email OTP enabled

Status: Secure, private AI endpoint operational.
