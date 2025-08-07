import socket
import threading
import os
import time
from datetime import datetime
from collections import defaultdict

LOG_FILE = 'logs/honeylogs.log'
MAX_LOGINS_PER_SECOND = 3

login_attempts = defaultdict(list)  # key: IP, value: list of timestamps

BANNER = "220 (vsFTPd 3.0.3)\r\n"

RESPONSE_LOGIN_FAILED = "530 Login incorrect.\r\n"
RESPONSE_USER_OK = "331 Please specify the password.\r\n"
RESPONSE_LOGIN_SUCCESS = "230 Login successful.\r\n"
RESPONSE_UNKNOWN_COMMAND = "500 Unknown command.\r\n"

def log_event(event_type, ip, detail=""):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"[{timestamp}] [{event_type}] From {ip} {detail}"
    print(log_line)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, 'a') as f:
        f.write(log_line + '\n')

def is_bruteforce(ip):
    now = time.time()
    login_attempts[ip] = [t for t in login_attempts[ip] if now - t <= 1]  # only keep timestamps in the last 1 second
    if len(login_attempts[ip]) >= MAX_LOGINS_PER_SECOND:
        return True
    return False

def handle_client(conn, addr):
    ip = addr[0]
    conn.sendall(BANNER.encode())

    try:
        username = ""
        while True:
            data = conn.recv(1024).decode().strip()
            if not data:
                break

            cmd = data.upper()

            if cmd.startswith("USER"):
                username = data.split(" ", 1)[1] if " " in data else "unknown"
                login_attempts[ip].append(time.time())

                if is_bruteforce(ip):
                    log_event("BRUTEFORCE", ip, f"Excessive login attempts (user: {username})")
                log_event("LOGIN_ATTEMPT", ip, f"USER: {username}")
                conn.sendall(RESPONSE_USER_OK.encode())

            elif cmd.startswith("PASS"):
                password = data.split(" ", 1)[1] if " " in data else "unknown"
                log_event("LOGIN_FAIL", ip, f"USER: {username} PASS: {password}")
                conn.sendall(RESPONSE_LOGIN_FAILED.encode())

            else:
                log_event("CMD", ip, f"Unknown: {data}")
                conn.sendall(RESPONSE_UNKNOWN_COMMAND.encode())

    except Exception as e:
        log_event("ERROR", ip, str(e))
    finally:
        conn.close()

def start_honeypot(host='0.0.0.0', port=21):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind((host, port))
    except OSError as e:
        log_event("ERROR", host, f"Port {port} bind failed: {e}")
        exit(1)

    server.listen(5)
    log_event("INFO", host, f"HoneyFTP running on port {port}...")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_honeypot()
