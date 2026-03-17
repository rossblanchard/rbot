# HomeLab Setup Guide
## Ross Blanchard – Personal AI Endpoint
### Project: rbot.rossblanchard.com

---

# Overview

This guide documents the complete setup for hosting AnythingLLM on a Raspberry Pi at home and securely exposing it to the public internet using Cloudflare Tunnel.

Architecture Goal:

Internet
  → Cloudflare (DNS + SSL + Security)
  → Encrypted Tunnel
  → Raspberry Pi
  → Docker
  → AnythingLLM

No open router ports.
Home IP remains hidden.
Free SSL via Cloudflare.

---

# Phase 1 — Cloudflare DNS Migration

## Goal

- Move DNS from GoDaddy to Cloudflare
- Enable free SSL for main domain
- Prepare rbot subdomain

---

## Step 1 — Add Domain to Cloudflare

1. Log into Cloudflare
2. Click Add a Site
3. Enter rossblanchard.com
4. Choose Free Plan
5. Review imported DNS records carefully

Verify:

- A record for rossblanchard.com
- A record or CNAME for www
- No missing records

---

## Step 2 — Change Nameservers in GoDaddy

Cloudflare will provide two nameservers similar to:

    lucy.ns.cloudflare.com
    mark.ns.cloudflare.com

In GoDaddy:

1. Domain Settings
2. Nameservers → Custom
3. Replace with Cloudflare nameservers
4. Save

Wait for propagation (5–60 minutes typical).

---

## Step 3 — Enable Free SSL

In Cloudflare Dashboard:

SSL/TLS → Overview
Set mode to:

    Full

Then:

SSL/TLS → Edge Certificates
Enable:

- Always Use HTTPS
- Automatic HTTPS Rewrites

Your main site should now load via HTTPS.

---

## Step 4 — Prepare rbot Subdomain

In Cloudflare → DNS → Records
Add:

    Type: CNAME
    Name: rbot
    Target: placeholder.example.com
    Proxy Status: Proxied (Orange Cloud ON)

This placeholder will later be replaced by your Cloudflare Tunnel target.

Do NOT point to home IP.
Do NOT open router ports.

---

# Phase 2 — Raspberry Pi Setup

## Recommended Hardware

- Raspberry Pi 4 or 5
- 4GB RAM minimum (8GB preferred)
- 64-bit Raspberry Pi OS
- Wired Ethernet recommended

---

## Step 1 — Update System

    sudo apt update && sudo apt upgrade -y
    sudo reboot

---

## Step 2 — Install Docker

    curl -fsSL https://get.docker.com | sh
    sudo usermod -aG docker $USER

Log out and back in.

Verify:

    docker version

---

## Step 3 — Install Docker Compose Plugin

    sudo apt install docker-compose-plugin -y

Verify:

    docker compose version

---

## Step 4 — Deploy AnythingLLM

Create directory:

    mkdir ~/anythingllm
    cd ~/anythingllm

Create docker-compose.yml with:

services:
  anythingllm:
    image: mintplexlabs/anythingllm:latest
    container_name: anythingllm
    ports:
      - "3001:3001"
    volumes:
      - anythingllm_storage:/app/server/storage
    restart: unless-stopped

volumes:
  anythingllm_storage:

Start:

    docker compose up -d

---

## Step 5 — Test Locally

On Pi:

    http://localhost:3001

On LAN device:

    http://<pi-local-ip>:3001

Do not expose externally yet.

---

## Security Baseline

- Set strong AnythingLLM password
- Assign static IP to Pi
- No router port forwarding
- Keep OS updated regularly

---

# Phase 3 — Cloudflare Tunnel Setup

## Goal

Expose AnythingLLM securely without opening ports.

---

## Step 1 — Install cloudflared

    sudo apt install cloudflared

If unavailable, install using Cloudflare’s official repository instructions.

---

## Step 2 — Authenticate

    cloudflared tunnel login

Authorize your domain via browser.

---

## Step 3 — Create Tunnel

    cloudflared tunnel create rbot

This generates a tunnel ID and credentials file.

---

## Step 4 — Route DNS

    cloudflared tunnel route dns rbot rbot.rossblanchard.com

Cloudflare automatically creates the correct CNAME record.

---

## Step 5 — Create Config File

Create:

    ~/.cloudflared/config.yml

Contents:

    tunnel: <tunnel-id>
    credentials-file: /home/pi/.cloudflared/<tunnel-id>.json

    ingress:
      - hostname: rbot.rossblanchard.com
        service: http://localhost:3001
      - service: http_status:404

---

## Step 6 — Run Tunnel

    cloudflared tunnel run rbot

Visit:

    https://rbot.rossblanchard.com

---

## Step 7 — Enable Access Protection (Strongly Recommended)

Cloudflare Dashboard → Zero Trust → Access

Protect:

    rbot.rossblanchard.com

Require:

- Google login OR
- One-time email login

---

# Final Architecture Summary

Internet
  → Cloudflare (DNS + SSL + WAF)
  → Encrypted Tunnel
  → Raspberry Pi
  → Docker
  → AnythingLLM

Security Characteristics:

- No open inbound ports
- Home IP hidden
- Free SSL certificates
- Optional Zero Trust authentication

---

# Optional Future Enhancements

- Enable cloudflared as a system service
- Configure automatic Docker updates (Watchtower)
- Add UFW firewall on Pi
- Add monitoring (Grafana / Prometheus)
- Create rbot-dev subdomain for testing

---

End of HomeLab Setup Guide
