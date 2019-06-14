import socket
import threading
from colorama import Fore, Style

HOST = '10.13.40.113'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
messages = []


def send(client_ip, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((client_ip, PORT))
        s.sendall(message.encode(encoding="utf-8"))
        data = s.recv(1024)

    print(Fore.RED + 'Received', repr(data))
    print(Style.RESET_ALL)


def listen():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        while True:
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024).decode()
                    if not data:
                        break
                    else:
                        messages.append(data)
                    print(Fore.GREEN + data)
                    print(Style.RESET_ALL)
                    conn.sendall(data.encode(encoding="utf-8"))


if __name__ == "__main__":
    th = threading.Thread(target=listen)
    th.start()
    while True:
        a = input()
        print()
        if a == "exit":
            break
        send("10.13.40.110", a)
