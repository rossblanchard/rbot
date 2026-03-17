


# INFRA__rclone_google_drive_removal_procedure__v1.0

## 1. Document Metadata
- **Status:** Active (Execution Pending)
- **Owner:** Ross Blanchard
- **System:** Raspberry Pi 4 (rbot host)
- **Date:** 2026-03-13
- **Architect:** Archie
- **Supersedes:** `INFRA__google_drive_sync_integration__v1.0` (Deprecated)

## 2. Purpose and Scope
This document defines the procedure for safely removing the `rclone` Google Drive integration from the `rbot` Docker environment. 

The `rclone` FUSE mount architecture has been deprecated due to severe I/O lockup vulnerabilities when utilized alongside SQLite databases inside Docker containers. This procedure will decouple the network drive, terminate the background processes, and restore the AnythingLLM container to a stable, localized state in preparation for the API-driven MCP integration.

## 3. Prerequisites
- **Mandatory:** A verified Docker volume backup must exist prior to execution (See `NFRA__anythingllm_backup_procedure__v1.1`).
- SSH access to the Raspberry Pi host.
- Administrative (`sudo`) privileges.

---

## 4. Execution Procedure

### Step 4.1: Verify Pre-Surgery Backup
Confirm the existence of the backup archive generated prior to this operation:
```bash
ls -lh /home/ross/backups/rbot_pre_rclone_removal_*.tar.gz
```
*Do not proceed if this archive is missing or 0 bytes.*

### Step 4.2: Spin Down the Container
Gracefully halt the AnythingLLM container to release file locks on the database.
```bash
cd ~/services/rbot
docker compose down
```
*Wait for the terminal to confirm the `rbot` container has been removed.*

### Step 4.3: Terminate `rclone` Processes
Identify and kill any running `rclone` daemon processes holding the FUSE mount open.
```bash
sudo killall rclone
```
*Note: If the terminal returns `rclone: no process found`, the daemon has already crashed or was not running. This is acceptable; proceed to the next step.*

### Step 4.4: Force Unmount the Network Drive
Ensure the host operating system completely detaches from the Google Drive FUSE mount.
```bash
sudo umount -f /home/ross/GoogleDrive
```
*Note: If the terminal returns `not mounted`, proceed to the next step.*

### Step 4.5: Remove the Volume Mapping from Docker Compose
Edit the configuration file to decouple the host mount from the container.
```bash
nano ~/services/rbot/docker-compose.yml
```

Locate the `volumes:` array under the `rbot` service block.
**Delete** the line mapping the external drive. The block should change:

**FROM:**
```yaml
    volumes:
      - rbot_storage:/app/server/storage
      - /home/ross/GoogleDrive:/gdrive
```

**TO:**
```yaml
    volumes:
      - rbot_storage:/app/server/storage
```

Save and exit the editor (`CTRL+O`, `Enter`, `CTRL+X`).

### Step 4.6: Restart the Stabilized Container
Bring the `rbot` container back online utilizing only its native Docker volume.
```bash
docker compose up -d
```

Monitor the startup sequence for 30 seconds to ensure the SQLite database initializes without I/O hangs:
```bash
docker compose logs -f
```
*(Press `CTRL+C` to exit the log view once the web server reports it is listening on port 3001).*

---

## 5. Verification and Validation

1. Navigate to `https://rbot.rossblanchard.com` via a web browser.
2. Authenticate using existing administrator credentials.
3. Verify that previous workspaces and documents are present and accessible.

If authentication is successful, the `rclone` hazard has been successfully excised without data loss.

## 6. Cleanup (Post-Verification)
Once system stability is confirmed, the orphaned host directory may be safely deleted to prevent future confusion:
```bash
rmdir /home/ross/GoogleDrive
```
*(Use `rmdir` to ensure the directory is completely empty before deletion; if it contains files, it will safely reject the command).*

---

## 7. Failure Modes & Rollback

| Failure Mode | Indicator | Rollback Action |
| :--- | :--- | :--- |
| **Database Corruption** | Login fails or workspaces are missing. | Spin down container (`docker compose down`). Delete corrupted volume (`docker volume rm rbot_rbot_storage`). Restore volume from the Step 4.1 backup archive. |
| **Stale File Handle** | `umount` returns "device is busy". | Force unmount using lazy detach: `sudo umount -l /home/ross/GoogleDrive`. |

--- END OF FILE ---
