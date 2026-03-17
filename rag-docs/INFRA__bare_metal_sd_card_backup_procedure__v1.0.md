


### The Tradeoff to Know Before You Start
A bit-for-bit clone copies *everything*, including empty space. If you have a 64GB SD card, it will create a 64GB file on your Mac, even if you are only using 8GB of data. To fix this, we will compress the image immediately after creating it.

---

### Step 1: Safely Shutdown the Pi
Don't just pull the power. SSH into the Pi and gracefully spin it down to prevent database corruption in AnythingLLM or SQLite.
```bash
sudo shutdown -h now
```
Wait for the green light on the Pi to stop blinking, pull the power, remove the Micro SD card, and insert it into your Mac using an adapter.

### Step 2: Identify the SD Card on your Mac
Open the **Terminal** app on your Mac and list your drives:
```bash
diskutil list
```
Look through the output for your SD card. It will likely be labeled something like `DOS_FAT_32 bootfs` and `Linux`. 
**Crucial:** Note the disk number (e.g., `/dev/disk2`, `/dev/disk3`, `/dev/disk4`). 
*Do not proceed until you are 100% sure which disk is the SD card, or you could overwrite your Mac's hard drive.*

### Step 3: Unmount the SD Card
Your Mac automatically mounts the boot partition. We need to unmount it so we can read the raw data. (Replace `N` with your disk number, e.g., `disk4`):
```bash
diskutil unmountDisk /dev/diskN
```
*(Expected output: `Unmount of all volumes on diskN was successful`)*

### Step 4: Create the Clone (The `dd` command)
Now we execute the clone. We are going to use `/dev/rdiskN` instead of `/dev/diskN` (adding the "r" stands for "raw" disk access, which makes the backup happen about 5x faster on macOS).

Run this command, replacing `N` with your disk number, and `YYYYMMDD` with today's date:
```bash
sudo dd if=/dev/rdiskN of=~/Desktop/rbot_baremetal_backup_YYYYMMDD.img bs=1m
```
*   `if` = input file (the SD card)
*   `of` = output file (your Mac's desktop)
*   `bs=1m` = reads 1 megabyte at a time for speed.

**Note on observability:** The `dd` command is completely silent. It won't show a progress bar. If you want to check its progress, press `CTRL + T` while it's running, and your Mac will print out how much data has been copied so far. 

### Step 5: Eject the SD Card
Once the terminal prompt returns, the clone is finished. You can safely eject the physical card and put it back in your Raspberry Pi.
```bash
diskutil eject /dev/diskN
```

### Step 6: Compress the Backup (Highly Recommended)
Right now, you have a massive `.img` file on your Desktop. Let's shrink it down by zipping the empty space. Run:
```bash
gzip ~/Desktop/rbot_baremetal_backup_YYYYMMDD.img
```
This will take a few minutes, but it will convert the file into `rbot_baremetal_backup_YYYYMMDD.img.gz`, shrinking it from its full capacity down to just the actual data size (usually 4-8GB). 

---

### How to Restore It Later
If your Pi's SD card ever dies:
1. Open the **Raspberry Pi Imager** or **BalenaEtcher** app on your Mac.
2. Select your new, blank SD card.
3. For the OS, choose "Use Custom" and select your `.img.gz` file. 
4. Click Flash. 

