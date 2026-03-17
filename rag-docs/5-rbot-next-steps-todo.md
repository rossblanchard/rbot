# rbot – Next Steps Roadmap

Owner: Ross
Environment: Raspberry Pi (Docker) + Cloudflare Tunnel + Zero Trust
Date: 2026-03-06

---

# 1. Security Enhancements (High Priority)

## 1.1 Restrict by Country (US Only)
**Why:** Reduces automated global probing traffic at the edge.
**Where:** Cloudflare → Access → Applications → rbot → Policies
**Action:** Add rule → Country → Equals → United States

---

## 1.2 SSH Hardening with fail2ban
**Why:** Protects SSH from brute force attempts.

Install:
```
sudo apt install fail2ban -y
```

Enable & start:
```
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

---

## 1.3 Docker Log Limits
**Why:** Prevents logs from filling SD/SSD storage.

Edit docker-compose.yml and add:

```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

Then restart:
```
docker compose up -d
```

---

# 2. Reliability & Backup (Very Important)

## 2.1 Backup rbot Docker Volume
Volume name:
```
rbot_storage
```

Backup command example:
```
docker run --rm \
  -v rbot_storage:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/rbot-backup.tar.gz /data
```

Store backup on:
- Mac
- External drive
- Cloud storage

---

## 2.2 Automated Backups (Future)
- Create weekly cron job
- Sync backup to Mac via rsync

---

# 3. Observability (Operational Visibility)

## 3.1 Install Uptime Kuma (Behind Tunnel)
**Why:** Monitor rbot and other internal services.

Future structure:
```
services/
  rbot/
  uptime-kuma/
```

Expose via:
```
kuma.rossblanchard.com
```

Protect with Cloudflare Access.

---

## 3.2 Resource Monitoring
Monitor:
- CPU
- Memory
- Disk usage

Command:
```
htop
```

Consider:
- Netdata
- Prometheus (advanced)

---

# 4. Performance & Hardware Planning

## 4.1 Storage Consideration
If using SD card:
- Consider migrating to SSD
- Improves durability + performance

Check disk usage:
```
df -h
```

---

## 4.2 Model Strategy
Current: OpenAI API

Future considerations:
- Cost monitoring
- Model selection per workspace
- Evaluate local LLM only if needed (Pi is limited)

---

# 5. AI Workflow Improvements

## 5.1 Structured Document Ingestion
- Create dedicated workspace for documentation
- Keep personal vs technical separated

---

## 5.2 Naming Strategy
Example:
- rbot-core
- homelab-docs
- personal-notes

Clear separation improves retrieval quality.

---

# 6. Future Expansion Ideas

- Add additional internal services behind Cloudflare Tunnel
- Add private API endpoints
- Add webhook automation
- Add CI/CD for container updates

---

# Priority Order Recommendation

1. ✅ Docker log limits
2. ✅ Backup strategy
3. ✅ fail2ban
4. ✅ US-only rule
5. Observability stack
6. Performance tuning

---

# Current System Status

✅ Raspberry Pi hardened
✅ Docker installed
✅ AnythingLLM (rbot) deployed
✅ Persistent storage configured
✅ Cloudflare Tunnel active
✅ Zero Trust email OTP enabled

You are running a secure, identity-protected AI node from home infrastructure.

---

End of document.
