# ghostshield.py
# A one-shot cybersecurity hardening script for Linux/Kali.

import os
import subprocess
import sys
import argparse
import platform

def run(cmd):
    print(f"[+] Running: {cmd}")
    subprocess.run(cmd, shell=True, check=False)

def require_sudo():
    if os.geteuid() != 0:
        print("[-] This script must be run as root. Use sudo.")
        sys.exit(1)

def disable_bash_history():
    print("[+] Disabling bash history...")
    run("unset HISTFILE")
    run("echo 'unset HISTFILE' >> /etc/profile")
    run("chmod 000 ~/.bash_history 2>/dev/null")

def randomize_mac():
    print("[+] Randomizing MAC address...")
    interfaces = os.listdir('/sys/class/net/')
    for iface in interfaces:
        if iface != 'lo':
            run(f"ip link set {iface} down")
            run(f"macchanger -r {iface}")
            run(f"ip link set {iface} up")

def configure_ufw():
    print("[+] Configuring UFW firewall...")
    run("apt-get install -y ufw")
    run("ufw default deny incoming")
    run("ufw default allow outgoing")
    run("ufw allow out 53,80,443/tcp")
    run("ufw allow out 53,80,443/udp")
    run("ufw enable")

def set_dns_cloudflare():
    print("[+] Setting DNS to Cloudflare...")
    resolv_conf = "nameserver 1.1.1.1\nnameserver 1.0.0.1\n"
    with open("/etc/resolv.conf", "w") as f:
        f.write(resolv_conf)
    run("chattr +i /etc/resolv.conf")

def warn_if_not_encrypted():
    print("[+] Checking for disk encryption...")
    result = subprocess.run("lsblk -o NAME,TYPE,MOUNTPOINT", shell=True, capture_output=True, text=True)
    if 'crypt' not in result.stdout:
        print("[!] WARNING: Full-disk encryption not detected!")

def disable_usb_autorun():
    print("[+] Disabling USB autorun...")
    run("echo 'usb-storage' >> /etc/modprobe.d/blacklist.conf")
    run("modprobe -r usb-storage")

def enable_unattended_upgrades():
    print("[+] Enabling unattended security upgrades...")
    run("apt-get install -y unattended-upgrades")
    run("dpkg-reconfigure -f noninteractive unattended-upgrades")

def detect_vm():
    print("[+] Detecting virtual environment...")
    vm_indicators = ["hypervisor", "vbox", "vmware", "kvm"]
    result = subprocess.run("lscpu", shell=True, capture_output=True, text=True)
    if any(ind in result.stdout.lower() for ind in vm_indicators):
        print("[!] WARNING: VM environment detected!")

def harden_system():
    disable_bash_history()
    randomize_mac()
    configure_ufw()
    set_dns_cloudflare()
    warn_if_not_encrypted()
    disable_usb_autorun()
    enable_unattended_upgrades()
    detect_vm()

if __name__ == "__main__":
    require_sudo()

    parser = argparse.ArgumentParser(description="GhostShield - Harden your Kali/Ubuntu rig.")
    parser.add_argument("--mode", choices=["default", "stealth", "paranoid"], default="default", help="Select hardening mode")
    args = parser.parse_args()

    print(f"[*] GhostShield Starting in {args.mode.upper()} mode...")

    if args.mode in ["default", "stealth", "paranoid"]:
        harden_system()

    if args.mode in ["stealth", "paranoid"]:
        print("[+] Applying stealth mode adjustments...")
        run("ufw logging off")
        run("echo 1 > /proc/sys/net/ipv4/icmp_echo_ignore_all")

    if args.mode == "paranoid":
        print("[+] Applying paranoid mode adjustments...")
        run("systemctl stop bluetooth 2>/dev/null")
        run("systemctl disable bluetooth 2>/dev/null")
        run("systemctl stop avahi-daemon 2>/dev/null")
        run("systemctl disable avahi-daemon 2>/dev/null")
        run("ufw deny out to any port 22")

    print("[+] GhostShield hardening complete.")
