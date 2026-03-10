# NFRA__anythingllm_backup_procedure__v1.1

Status: Active
Owner: Ross Blanchard
System: AnythingLLM (container: rbot)
Host: Raspberry Pi 4 (8GB)
Date: 2026-03-10
Supersedes: INFRA__anythingllm_volume_backup_procedure__v1.0

## 1. Purpose

This document defines the procedure for creating a complete operational backup of the AnythingLLM system running in the `rbot` Docker container. The procedure captures both application state and the minimal infrastructure configuration required to restore the system after failure.

The objective is to allow full restoration of the system onto a new host with minimal reconstruction.

## 2. System Components Requiring Backup

The AnythingLLM deployment depends on three critical artifacts:

1. Docker volume containing application state
2. Container configuration (docker-compose)
3. rclone configuration used for Google Drive integration

Loss of any of these artifacts complicates recovery.

### 2.1 Docker Volume

Volume Name:

rbot_rbot_storage

Host Path:

/var/lib/docker/volumes/rbot_rbot_storage/_data

Mounted in container as:

/app/server/storage

This volume contains:

- user accounts
- password hashes
- workspaces
- documents
- embeddings
- application metadata
- configuration stored by AnythingLLM

This is the primary stateful component of the system.

### 2.2 Container Configuration

File:

/home/ross/services/rbot/docker-compose.yml

This file defines the container image, port mapping, restart policy, and volume attachment.

### 2.3 Google Drive Integration Configuration

File:

/home/ross/.config/rclone/rclone.conf

This file contains OAuth credentials and configuration for Google Drive mounting.

## 3. Backup Storage Location

Backups are written to:

/home/ross/backups

File naming convention:

rbot_full_backup_YYYY-MM-DD_HHMM.tar.gz

Example:

rbot_full_backup_2026-03-10_2145.tar.gz

## 4. Backup Procedure

### Step 1 — Ensure Backup Directory Exists

mkdir -p /home/ross/backups

### Step 2 — Execute Backup

Run the following command on the Raspberry Pi host:

```
docker run --rm -v rbot_rbot_storage:/volume -v /home/ross:/hosthome -v /home/ross/backups:/backup alpine tar czf /backup/rbot_full_backup_$(date +%F_%H%M).tar.gz /volume /hosthome/services/rbot/docker-compose.yml /hosthome/.config/rclone/rclone.conf
```

Operational description:

- A temporary Alpine container is started
- The AnythingLLM volume is mounted as `/volume`
- The host home directory is mounted as `/hosthome`
- The backup directory is mounted as `/backup`
- `tar` compresses the required artifacts into a timestamped archive
- The container automatically deletes itself after completion

## 5. Backup Verification

Confirm the archive exists:

```
ls -lh /home/ross/backups
```

Expected output example:

rbot_full_backup_2026-03-10_2145.tar.gz

File size varies depending on documents and embeddings stored in AnythingLLM.

Verification must always be performed after creating a backup.

## 6. Recommended Operational Practice

A backup should be created before any of the following operations:

- modifying docker-compose.yml
- upgrading AnythingLLM
- modifying storage configuration
- modifying Google Drive integration
- restarting containers after configuration changes

The backup process takes only a few seconds and significantly reduces operational risk.

## 7. Backup Scope

### Included

- AnythingLLM persistent storage
- user database
- workspaces
- documents
- embeddings
- container configuration
- Google Drive authentication configuration

### Not Included

- Raspberry Pi OS
- Docker installation
- other containers
- unrelated host files

These components must be rebuilt during disaster recovery but are standard installations.

## 8. Disaster Recovery Overview

In the event of catastrophic failure (hardware replacement or OS rebuild):

1. Install Raspberry Pi OS
2. Install Docker and Docker Compose
3. Restore `/home/ross/services/rbot/docker-compose.yml`
4. Restore `/home/ross/.config/rclone/rclone.conf`
5. Restore Docker volume contents from the backup archive
6. Start the container using `docker compose up -d`

After restoration, AnythingLLM should return to its previous operational state.

## 9. Failure Considerations

Possible failure conditions include:

- insufficient disk space
- incorrect Docker volume name
- incorrect backup directory permissions
- interrupted backup process

Backup verification (Section 5) mitigates these risks.

## End of Document
