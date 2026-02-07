import socket
import threading
HOST = '127.0.0.1'
PORT = 12345
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(2)
clients = []
def handle_client(client):
    while True:
        try:
            message = client.recv(1024).decode()
            if not message:
                break
            broadcast(message, client)
        except:
            break
    clients.remove(client)
    client.close()
def broadcast(message, sender):
    for client in clients:
        if client != sender:
            client.send(message.encode())
print("Server started. Waiting for clients...")
while True:
    client, address = server.accept()
    print(f"Connected with {address}")
    clients.append(client)
    thread = threading.Thread(target=handle_client, args=(client,))
    thread.start()
