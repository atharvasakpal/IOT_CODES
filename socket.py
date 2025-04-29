# hostname -I

# server.py
import socket
import threading

HOST = '0.0.0.0'
PORT = 12345

def receive_messages(conn):
    while True:
        try:
            msg = conn.recv(1024).decode()
            if not msg:
                break
            print(f"\nFriend: {msg}\nYou: ", end="")
        except:
            break

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    print("Waiting for connection...")

    conn, addr = s.accept()
    print(f"Connected by {addr}")

    threading.Thread(target=receive_messages, args=(conn,), daemon=True).start()

    while True:
        msg = input("You: ")
        conn.sendall(msg.encode())

if __name__ == "__main__":
    main()




# client.py
import socket
import threading

SERVER_IP = '192.168.x.x'  # Replace with your server Pi's IP
PORT = 12345

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if not msg:
                break
            print(f"\nFriend: {msg}\nYou: ", end="")
        except:
            break

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, PORT))
    print(f"Connected to {SERVER_IP}:{PORT}")

    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

    while True:
        msg = input("You: ")
        sock.sendall(msg.encode())

if __name__ == "__main__":
    main()
