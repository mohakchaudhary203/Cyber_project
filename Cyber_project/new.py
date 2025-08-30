import os

print("[*] Removing old Npcap installation...")

# Kill Wireshark or any process using Npcap
os.system('taskkill /F /IM Wireshark.exe')

# Run Npcap uninstaller if it exists
os.chdir(r"C:\Program Files\Npcap")
if os.path.exists("npcap-uninstall.exe"):
    os.system('npcap-uninstall.exe /S')

# Delete leftover files and folders
os.system('rmdir /S /Q "C:\\Program Files\\Npcap"')
os.system('del /F /Q "C:\\Windows\\System32\\Npcap*"')
os.system('del /F /Q "C:\\Windows\\SysWOW64\\Npcap*"')

# Clean registry entry
os.system('reg delete HKLM\\SYSTEM\\CurrentControlSet\\Services\\npcap /f')

print("[+] Old Npcap installation removed successfully.")
