import subprocess
import sys
import os
import platform
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import shutil

# -------------------------------
# 1. AUTO-INSTALL SCAPY IF MISSING
# -------------------------------
def ensure_scapy():
    try:
        import scapy.all as scapy
        return scapy
    except ImportError:
        print("[INFO] Scapy not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "scapy"])
        import scapy.all as scapy
        return scapy

scapy = ensure_scapy()

# -------------------------------
# 2. AUTO-INSTALL NPCAP (Windows only)
# -------------------------------
def ensure_npcap():
    if platform.system() != "Windows":
        return
    npcap_path = r"C:\Program Files\Npcap"
    if os.path.exists(npcap_path):
        print("[INFO] Npcap already installed.")
        return
    print("[INFO] Npcap not found. Installing silently...")
    # Download npcap installer if not present
    installer = "npcap_installer.exe"
    url = "https://npcap.com/dist/npcap-1.79.exe"  # Example version (update as needed)
    if not os.path.exists(installer):
        subprocess.check_call(["powershell", "-Command",
                               f"Invoke-WebRequest -Uri {url} -OutFile {installer}"])
    # Silent install
    subprocess.check_call([installer, "/S"])
    print("[INFO] Npcap installation complete.")

ensure_npcap()

# -------------------------------
# 3. REAL WI-FI SECURITY DETECTION
# -------------------------------
def detect_wifi_security():
    os_type = platform.system()
    security_info = []
    try:
        if os_type == "Windows":
            result = subprocess.check_output("netsh wlan show interfaces", shell=True).decode(errors="ignore")
            for line in result.splitlines():
                if "Authentication" in line or "Cipher" in line:
                    security_info.append(line.strip())
        else:
            # Linux / macOS
            interfaces = subprocess.check_output("iwconfig", shell=True).decode(errors="ignore")
            for iface in interfaces.split("\n\n"):
                if "no wireless extensions" in iface or iface.strip() == "":
                    continue
                if "WEP" in iface or "WPA" in iface:
                    security_info.append(iface.strip())
    except Exception as e:
        security_info.append(f"[ERROR] Detection failed: {e}")
    return security_info if security_info else ["No Wi-Fi security info found"]

# -------------------------------
# 4. MAIN SECURITY ASSESSMENT LOGIC
# -------------------------------
def run_assessment():
    print("\n[+] Running Wi-Fi Security Assessment...\n")
    info = detect_wifi_security()
    for line in info:
        print(line)
    return "\n".join(info)

# -------------------------------
# 5. GUI WITH SCHEDULER
# -------------------------------
def start_gui():
    def run_now():
        output = run_assessment()
        messagebox.showinfo("Wi-Fi Security Assessment", output)

    def schedule_task():
        try:
            minutes = int(interval_var.get())
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number for minutes.")
            return

        def task_loop():
            while True:
                output = run_assessment()
                print(f"[INFO] Next run in {minutes} minutes...")
                time.sleep(minutes * 60)

        threading.Thread(target=task_loop, daemon=True).start()
        messagebox.showinfo("Scheduler", f"Task scheduled every {minutes} minutes.")

    root = tk.Tk()
    root.title("Wi-Fi Security Assessment Tool")
    root.geometry("400x200")

    ttk.Label(root, text="Scheduler Interval (minutes):").pack(pady=10)
    interval_var = tk.StringVar(value="10")
    ttk.Entry(root, textvariable=interval_var, width=10).pack(pady=5)

    ttk.Button(root, text="Run Now", command=run_now).pack(pady=5)
    ttk.Button(root, text="Start Scheduler", command=schedule_task).pack(pady=5)
    ttk.Button(root, text="Exit", command=root.quit).pack(pady=10)

    root.mainloop()

# -------------------------------
# 6. ENTRY POINT
# -------------------------------
if __name__ == "__main__":
    start_gui()
# Wi-Fi Security Assessment Tool v1.000 by OpenAI GPT4
# GitHub:   
# Twitter:   
# Discord:  
# Telegram:   
# Email:    
# License: MIT License
# Disclaimer: Use at your own risk. The author is not responsible for any misuse or damage caused by this tool. 
# Always ensure you have permission to test the security of any network. Unauthorized access to networks is illegal and unethical. 
# This tool is for educational purposes only. 
# Please respect privacy and legal boundaries when using this tool.
# Always follow best practices for network security and ethical hacking. Stay safe and responsible!
# -----------------------------------------------------------------------------------------------