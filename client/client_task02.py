import socket

# Client configuration
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000
BUFFER_SIZE = 1024

# Create TCP client
def start_client():

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((SERVER_HOST, SERVER_PORT))

    # Receive introduction message
    intro_message = client_socket.recv(BUFFER_SIZE).decode()
    print("\n... Server Message ...")
    print(intro_message)

    try:
        while True:

            user_message = input("Enter your message (type 'exit' to quit): ")

            if user_message.lower() == "exit":
                break

            client_socket.sendall(user_message.encode())

            server_response = client_socket.recv(BUFFER_SIZE).decode()

            print("\n[SERVER RESPONSE]")
            print(server_response)

    except Exception as e:
        print("Error:", e)

    finally:
        client_socket.close()
        print("\nConnection closed.")

if __name__ == "__main__":
    start_client()
