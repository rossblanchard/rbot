
# INFRA__anythingllm_volume_backup_procedure__v1.0

Status: Active  
Owner: Ross Blanchard  
System: AnythingLLM (rbot)  
Host: Raspberry Pi 4 (8GB)  
Location: /home/ross/services/rbot  

---

# 1. Purpose

This document defines the procedure for creating a backup of the AnythingLLM persistent storage volume used by the `rbot` container.

The backup captures the entire application state including:

- user accounts
- authentication data
- workspaces
- documents
- embeddings
- application metadata

Backups are stored on the Raspberry Pi host filesystem for later restoration if required.

---

# 2. System Architecture Reference

Container Name

rbot

Docker Volume

rbot_rbot_storage

Volume Host Location

/var/lib/docker/volumes/rbot_rbot_storage/_data

Container Mount

/app/server/storage

AnythingLLM stores all persistent state inside this directory.

Backing up this volume captures the full system state.

---

# 3. Backup Location

Backups are written to:

/home/ross/backups

Backup file naming format:

rbot_rbot_storage_YYYY-MM-DD_HHMM.tar.gz

Example:

rbot_rbot_storage_2026-03-10_2130.tar.gz

---

# 4. Backup Procedure

## Step 1 — Create Backup Directory (if not already present)

mkdir -p /home/ross/backups

---

## Step 2 — Execute Backup

Run the following command from the Raspberry Pi:

docker run --rm -v rbot_rbot_storage:/data -v /home/ross/backups:/backup alpine tar czf /backup/rbot_rbot_storage_$(date +%F_%H%M).tar.gz /data

Explanation:

- A temporary Alpine Linux container is launched
- The AnythingLLM volume is mounted as `/data`
- A host directory is mounted as `/backup`
- The `tar` utility compresses the entire volume into a timestamped archive

The container is automatically removed when the process finishes.

---

# 5. Verify Backup

Confirm the archive exists:

ls -lh /home/ross/backups

Expected output example:

rbot_rbot_storage_2026-03-10_2130.tar.gz

File size will vary depending on stored documents and embeddings.

---

# 6. Recommended Operational Practice

Before performing any of the following operations:

- modifying docker-compose.yml
- upgrading AnythingLLM
- restarting containers after configuration changes
- modifying storage configuration
- modifying external integrations

Execute a backup using the procedure above.

This provides a fast recovery point in the event of application corruption or configuration errors.

---

# 7. Backup Scope

This procedure backs up:

- AnythingLLM persistent storage
- user database
- workspace configuration
- document index and embeddings

This procedure does NOT back up:

- docker-compose.yml
- system configuration
- rclone configuration
- Google Drive mount configuration
- other containers

Those artifacts must be managed separately.

---

# 8. Backup Frequency Recommendation

Minimum recommended cadence:

- before infrastructure changes
- before application upgrades
- before configuration changes

Optional improvement:

Daily automated backup via cron.

---

# 9. Failure Considerations

Potential failure conditions include:

- insufficient disk space
- incorrect volume name
- incorrect backup directory permissions

Verification in Section 5 must always be performed to confirm successful backup creation.

---

# End of Document
:::