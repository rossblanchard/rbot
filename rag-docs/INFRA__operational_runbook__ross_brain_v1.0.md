# Ross Brain – Operational Runbook

Document Name: INFRA__operational_runbook__ross_brain_v1.0.md  
Version: 1.0  
Date: 2026-03-09 UTC  
Owner: Ross Blanchard  
Status: Active

---

## 1. Purpose

This document defines the operational procedures for maintaining, recovering, and evolving the Ross Brain local LLM environment running on a Raspberry Pi 4 (8GB).

It provides step-by-step guidance for:

- Service restarts
- Container management
- Backup and recovery
- Embedding reindexing
- Upgrades
- Failure response

This runbook assumes:

- Raspberry Pi 4 (8GB)
- Linux-based OS (e.g., Raspberry Pi OS)
- Docker runtime
- AnythingLLM running in a Docker container
- OpenAI API used for LLM and embeddings

---

## 2. System Components

### 2.1 Hardware Layer
- Raspberry Pi 4 (8GB RAM)
- SD card or SSD storage
- Stable power supply

### 2.2 Software Layer
- Linux OS
- Docker
- AnythingLLM container
- Cloudflare Tunnel (if externally exposed)

---

## 3. Service Restart Procedures

### 3.1 Restart AnythingLLM Container

```bash
docker ps
```
Identify container name or ID.

```bash
docker restart <container_name>
```

Verify logs:

```bash
docker logs -f <container_name>
```

Success Criteria:
- No fatal errors in logs
- Web UI accessible
- Embedding provider initializes correctly

---

### 3.2 Restart Docker Service

```bash
sudo systemctl restart docker
```

Verify:

```bash
docker ps
```

---

### 3.3 Reboot Raspberry Pi

```bash
sudo reboot
```

After reboot:

- Confirm Docker auto-started
- Confirm AnythingLLM container is running

---

## 4. Backup Strategy

### 4.1 What Must Be Backed Up

- AnythingLLM persistent volume
- Workspace documents
- Vector database storage
- Configuration files
- System prompt configuration

### 4.2 Backup Method

Recommended:

```bash
docker stop <container_name>
```

Copy volume directory:

```bash
rsync -av /path/to/anythingllm/data /backup/location
```

Restart container:

```bash
docker start <container_name>
```

Frequency Recommendation:
- After major documentation additions
- Before upgrades
- Monthly baseline backup

---

## 5. Restore Procedure

1. Stop container
2. Replace data directory with backup
3. Restart container
4. Validate:
   - Documents visible
   - Retrieval working
   - Embeddings intact

---

## 6. Embedding Reindex Procedure

Reindex required when:

- Embedding model changes
- Vector store corruption occurs
- Major document restructuring happens

Procedure:

1. Remove affected documents
2. Re-upload canonical versions
3. Confirm embeddings regenerate
4. Test retrieval via new chat session

---

## 7. Upgrade Procedure

### 7.1 Upgrade AnythingLLM Container

```bash
docker pull mintplexlabs/anythingllm
```

Stop existing container:

```bash
docker stop <container_name>
```

Remove container (not volume):

```bash
docker rm <container_name>
```

Re-run container using existing volume.

Post-Upgrade Validation:
- UI loads
- Documents present
- Retrieval functional
- No embedding errors

---

## 8. Failure Modes

### 8.1 Container Fails to Start

Check:

```bash
docker logs <container_name>
```

Common causes:
- Corrupted volume
- Invalid environment variables
- Port conflict

---

### 8.2 Retrieval Fails

Symptoms:
- Generic answers
- No document references

Check:
- Embeddings present
- Vector database intact
- No provider errors

---

### 8.3 High Memory Usage

Raspberry Pi constraints:
- 8GB RAM limit
- No heavy concurrent workloads

Mitigation:
- Limit background services
- Restart container
- Monitor via:

```bash
htop
```

---

## 9. Security Operations

- Rotate OpenAI API keys periodically
- Store keys outside repository
- Validate Cloudflare Zero Trust rules
- Limit SSH exposure
- Maintain OS updates

---

## 10. Observability

Monitoring Methods:

- Docker logs
- System resource monitoring (htop)
- Periodic retrieval validation queries

Recommended Validation Query:

"What naming convention does Ross Brain use?"

If incorrect, investigate embeddings.

---

## 11. Evolution Path

Future Enhancements:

- Scheduled automated backups
- External NAS backup target
- Migration to SSD if on SD card
- Centralized log aggregation
- Multi-workspace separation if scaling

---

## 12. Operational Discipline

After any of the following events, documentation must be updated:

- Infrastructure change
- Deployment method change
- Upgrade process change
- Security posture modification

When operational changes stabilize, update:

- INFRA specification
- This runbook
- Relevant decision logs

---

# End of Document
