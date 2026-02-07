import socket
import threading
HOST = '127.0.0.1'
PORT = 12345
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
name = input("Enter your name: ")
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode()
            print(message)
        except:
            print("Disconnected from server")
            client.close()
            break
def send_messages():
    while True:
        message = input()
        full_message = f"{name}: {message}"
        client.send(full_message.encode())
receive_thread = threading.Thread(target=receive_messages)
send_thread = threading.Thread(target=send_messages)
receive_thread.start()
send_thread.start()
