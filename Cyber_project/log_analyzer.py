import re
from collections import Counter
import os

# Threshold for suspicious activity
FAILED_ATTEMPT_THRESHOLD = 3  

def analyze_log(file_path):
    if not os.path.exists(file_path): 
        print(f"Log file not found: {file_path}") 
        return

    failed_ips = []
    pattern = re.compile(r'Failed password for .* from (\d+\.\d+\.\d+\.\d+)')
    
    with open(file_path, 'r') as file:
        for line in file:
            match = pattern.search(line) # Look for failed login attempts
            if match:
                failed_ips.append(match.group(1))  # Extract IP

    if not failed_ips:
        print("No failed login attempts found in the log.") 
        return

    ip_counts = Counter(failed_ips)
    
    print("\nTop 5 IPs with failed login attempts:") 
    for ip, count in ip_counts.most_common(5):
        print(f"{ip}: {count} failed attempts") 
 
    print("\nSuspicious IPs (failed attempts >= threshold):") 
    suspicious_ips = {ip: count for ip, count in ip_counts.items() if count >= FAILED_ATTEMPT_THRESHOLD} 
    if suspicious_ips:
        for ip, count in suspicious_ips.items():
            print(f"{ip}: {count} failed attempts 🚨") 
    else:
        print("No suspicious IPs detected.")

if __name__ == "__main__":
    log_file_path = r'auth.log'  # Replace with full path if needed
    analyze_log(log_file_path) 

# Example usage:
# File: log_analyzer.py
# To analyze a log file: python log_analyzer.py
# Ensure you have a log file named 'auth.log' in the same directory or provide the full path. 
# The script will print the top 5 IPs with failed login attempts and flag any IPs exceeding the threshold. 
# Example log line to match:
# "Jul 10 10:00:00 server sshd[12345]: Failed password for invalid user admin
# "Jul 10 10:00:00 server sshd[12345]: Failed password for root
# "Jul 10 10:00:00 server sshd[12345]: Failed password for user1 
# "Jul 10 10:00:00 server sshd[12345]: Failed password for user2
