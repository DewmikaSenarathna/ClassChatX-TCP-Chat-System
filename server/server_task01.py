import socket
from datetime import datetime

#Server Configuration
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000
BUFFER_SIZE = 1024

#Logs
def log(message):
    time_stamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{time_stamp}] {message}")

#Create TCP Server
def start_server():
    #create TCP Socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Bind Socket
    server_socket.bind((SERVER_HOST, SERVER_PORT))

    #Listen for connections
    server_socket.listen(1)
    log(f"ClassChatX server started on {SERVER_HOST}:{SERVER_PORT}")
    log("Waiting for cleant connection ...")

    #Accept client connections
    client_socket, client_address = server_socket.accept()
    log(f"Client connected from {client_address}")

    #Sent introdution message to client
    intro_message = (
        "Welcome to ClassChatX.\n"
        "I am the ClassChatX server. I manage client connections and forward messages between users.\n"
    )
    client_socket.sendall(intro_message.encode())

    #Receive messages from client
    client_message = client_socket.recv(BUFFER_SIZE).decode()
    log(f"Message received from client: {client_message}")

    #Send acknowledgement
    response = "Server received your message successfully."
    client_socket.sendall(response.encode())

    #Close connection
    client_socket.close()
    server_socket.close()
    log("Connection closed. Server shutting down.")

if __name__ == "__main__":
    start_server()


