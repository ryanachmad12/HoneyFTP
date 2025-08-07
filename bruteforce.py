import threading
import random
import string
import ftplib
import time

TARGET_IP = '127.0.0.1'
TARGET_PORT = 21
THREAD_COUNT = 4
ATTEMPTS_PER_THREAD = 50

def generate_random_string(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def try_login(thread_id):
    for _ in range(ATTEMPTS_PER_THREAD):
        username = generate_random_string()
        password = generate_random_string()
        try:
            ftp = ftplib.FTP()
            ftp.connect(TARGET_IP, TARGET_PORT, timeout=3)
            ftp.login(username, password)
            print(f"[+] Thread-{thread_id}: SUCCESS - {username}:{password}")
            ftp.quit()
        except ftplib.error_perm:
            print(f"[-] Thread-{thread_id}: Failed - {username}:{password}")
        except Exception as e:
            print(f"[!] Thread-{thread_id}: Error - {e}")
        time.sleep(0.1)

def main():
    threads = []
    for i in range(THREAD_COUNT):
        t = threading.Thread(target=try_login, args=(i+1,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == '__main__':
    main()
