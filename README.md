# GhostShield

**GhostShield** is a one-command cybersecurity hardening tool for Kali Linux and Ubuntu systems. Designed for hackers, privacy enthusiasts, and cybersecurity professionals, it quickly fortifies your system against surveillance, network leaks, weak defaults, and forensic residue. There may be better and more custom ways, but this is a quick and easy script to run to make it to a lot of heavy lifting for you.

---

## 🔒 What It Does

- **Disables Bash History**  
  Prevents command logging to protect your operational security.

- **Randomizes MAC Address**  
  Changes your MAC address on all interfaces (except `lo`) to mask identity and location.

- **Firewall Hardening (UFW)**  
  Blocks all incoming traffic, only allows essential outgoing (DNS, HTTPS).

- **DNS Hardening**  
  Forces system DNS to Cloudflare's `1.1.1.1` and `1.0.0.1`. You can customize this and add a vpn etc later.

- **Detects Full-Disk Encryption**  
  Warns if system disks aren't encrypted, a major risk on portable devices.

- **Disables USB Autorun**  
  Prevents USB-based attacks by disabling automatic mounting.

- **Enables Unattended Security Upgrades**  
  Automatically installs security patches to keep you safe from CVEs.

- **Detects Virtual Machines**  
  Warns if you're in a VM (could be a honeypot, sandbox, etc.).

---

## 🔧 Usage

```bash
sudo python3 ghostshield.py --mode [default | stealth | paranoid]
```

### Modes:
- `default` - General hardening, safest baseline.
- `stealth` - Blocks all pings, disables logging, randomizes MAC.
- `paranoid` - All of the above + disables Bluetooth, Avahi, and SSH egress.

---

## 📦 Requirements
- Python 3
- Kali or Ubuntu
- Root privileges (`sudo`)
- Packages auto-installed: `ufw`, `macchanger`, `unattended-upgrades`

---

## 💡 Why Use GhostShield?
You can run and trust without configuring every file manually. With one command, you can take a raw Kali or Ubuntu machine and ghost it out for some extra privacy. 

---

## 🧪 Future Additions
- GUI/Terminal-based menu
- Full DNS-over-HTTPS proxy setup
- Encrypted bash logging (optional)
- Remote hardening over SSH
- Automated VM detection evasion

---

## ⚠️ Disclaimer
Use responsibly and legally. GhostShield modifies core system files and network settings. Do not run on production systems without review.


