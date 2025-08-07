# HoneyFTP   
*A simple honeypot for FTP brute-force detection.*

HoneyFTP is a fake FTP service written in Python that mimics a real FTP server, designed to detect suspicious login attempts, including brute-force attacks and common exploit patterns.  
This project is intended for **educational** and **research** purposes in a controlled environment only.

---

##  Features

- Fake FTP server listening on port 21
- Realistic banner to trick scanners and bots
- Logs:
  - Successful and failed login attempts
  - Brute-force detection (more than 4 login attempts per IP per second)
- Threaded connection handling
- Easy to configure and extend

---

##  How It Works

HoneyFTP listens on port `21` and accepts any incoming connection.  
It simulates responses like a real FTP server but never gives real access.  
If an IP attempts to login repeatedly (e.g. >4 times per second), it is flagged as a brute-force attempt.

Logs are saved in `logs/honeylogs.log` in a structured format with timestamps.

---

##  Directory Structure

```bash
HoneyFTP/
├── main.py              # Main honeypot server
├── logs/
│   └── honeylogs.log    # Log file (auto-created)
└── README.md            
````

---

##  Requirements

* Python 3.x
* Works out of the box (no 3rd-party dependencies)

---

##  Usage

### Run the FTP honeypot:

```bash
sudo python3 main.py
```

> Make sure port 21 is not in use by a real FTP service (like vsftpd, proftpd, etc.)

---

## Brute-force Simulation Tool

A simple script is included to simulate brute-force login attempts.

```bash
python3 bruteforce.py
```

It sends multiple random `USER`/`PASS` attempts to `127.0.0.1:21` using 4 threads.

---

## 📋 Sample Log Output

```
┌──(root㉿opslinuxsec)-[~/HoneyFTP]
└─# python3 main.py
[2025-08-07 17:53:54] [INFO] From 0.0.0.0 HoneyFTP running on port 21...
[2025-08-07 17:53:58] [LOGIN_ATTEMPT] From 127.0.0.1 USER: GxE23F
[2025-08-07 17:53:58] [LOGIN_ATTEMPT] From 127.0.0.1 USER: 0DPfCj
[2025-08-07 17:53:58] [LOGIN_FAIL] From 127.0.0.1 USER: 0DPfCj PASS: B6Ka1j
[2025-08-07 17:53:58] [BRUTEFORCE] From 127.0.0.1 Excessive login attempts (user: 1cjn7E)
[2025-08-07 17:53:58] [LOGIN_FAIL] From 127.0.0.1 USER: GxE23F PASS: fvj3OZ
[2025-08-07 17:53:58] [BRUTEFORCE] From 127.0.0.1 Excessive login attempts (user: VEYeV2)
[2025-08-07 17:53:58] [LOGIN_ATTEMPT] From 127.0.0.1 USER: 1cjn7E
[2025-08-07 17:53:58] [LOGIN_ATTEMPT] From 127.0.0.1 USER: VEYeV2
[2025-08-07 17:53:58] [LOGIN_FAIL] From 127.0.0.1 USER: 1cjn7E PASS: cBESn4
[2025-08-07 17:53:58] [LOGIN_FAIL] From 127.0.0.1 USER: VEYeV2 PASS: DWB4z5
[2025-08-07 17:53:58] [BRUTEFORCE] From 127.0.0.1 Excessive login attempts (user: tqTpOl)
[2025-08-07 17:53:58] [BRUTEFORCE] From 127.0.0.1 Excessive login attempts (user: mdTU6A)
[2025-08-07 17:53:58] [LOGIN_ATTEMPT] From 127.0.0.1 USER: mdTU6A
[2025-08-07 17:53:58] [LOGIN_FAIL] From 127.0.0.1 USER: mdTU6A PASS: aQ16EG
[2025-08-07 17:53:58] [BRUTEFORCE] From 127.0.0.1 Excessive login attempts (user: DqqBOZ)
[2025-08-07 17:53:58] [LOGIN_ATTEMPT] From 127.0.0.1 USER: DqqBOZ
[2025-08-07 17:53:58] [BRUTEFORCE] From 127.0.0.1 Excessive login attempts (user: FbK90m)
[2025-08-07 17:53:58] [LOGIN_ATTEMPT] From 127.0.0.1 USER: tqTpOl
[2025-08-07 17:53:58] [LOGIN_ATTEMPT] From 127.0.0.1 USER: FbK90m


```

---

## ⚠️ Disclaimer

This tool is for **educational and research purposes** only.
Do **not** deploy it on production systems or use it for malicious activities.
You are responsible for any misuse.

---

## Author

Created with by [OpsLinuxSec Team](https://opslinuxsec.com)


