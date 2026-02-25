import socket

#Client 
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000
BUFFER_SIZE = 1024

#Create TCP Client
def start_client():
    #Create TCP Socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Connect to server
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    #Receive server
    intro_message = client_socket.recv(BUFFER_SIZE).decode()
    print("\n ... Server Meassge ...")
    print(intro_message)

    #Take user input 
    user_message = input("Enter your message: ")

    #Send message to server
    client_socket.sendall(user_message.encode())

    #Receve server response
    server_response = client_socket.recv(BUFFER_SIZE).decode()
    print("\n[SERVER RESPONSE]")
    print(server_response)

    #Close connection
    client_socket.close()
    print("\nConnection closed.")


if __name__ == "__main__":
    start_client()