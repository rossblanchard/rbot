# Raspberry Pi Setup Steps

## Device
- Raspberry Pi 4 (8GB RAM)
- Raspberry Pi OS (64-bit)
- Hostname configured
- Connected via Ethernet

---

## 1. Enabled SSH

Executed:

    sudo raspi-config

Navigated to:

    Interface Options → SSH → Enable

Verified SSH service:

    sudo systemctl status ssh

Result:
- SSH service active and running

---

## 2. Verified Remote SSH Access

From Mac:

    ssh <username>@<pi-ip>

Accepted host fingerprint.
Confirmed successful remote login.

---

## 3. Configured Static IP (Router-Level DHCP Reservation)

On TP-Link BE24000 router:

    Advanced → Network → DHCP Server → Address Reservation

Added reservation:
- Bound Pi MAC address (eth0) to current LAN IP
- Device label: rbot

Rebooted Pi:

    sudo reboot

Verified IP remained consistent:

    hostname -I

Result:
- Stable LAN IP assigned via DHCP reservation

---

## 4. Created SSH Key (On Mac)

Generated key:

    ssh-keygen -t ed25519 -C "ross-mac"

Created:
- id_ed25519
- id_ed25519.pub

---

## 5. Installed Public Key on Pi

Executed:

    ssh-copy-id <username>@<pi-ip>

Tested login in new terminal session.

Result:
- SSH login successful without password prompt
- Key-based authentication confirmed

---

## 6. Disabled Password Authentication (SSH Hardening)

Edited SSH configuration:

    sudo nano /etc/ssh/sshd_config

Changed:

    PasswordAuthentication yes

To:

    PasswordAuthentication no

Restarted SSH service:

    sudo systemctl restart ssh

Result:
- Password-based SSH disabled
- Key-based SSH only

---

## Current State

✅ Headless operation enabled  
✅ Stable LAN IP assigned  
✅ SSH secured with key-based authentication only  
✅ System ready for Docker installation  

---

Next Phase:
Docker installation and AnythingLLM deployment.
