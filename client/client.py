import socket
import threading
import json

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000
BUFFER_SIZE = 1024


def receive_messages(client_socket):
    buffer = ""

    while True:
        try:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break

            buffer += data.decode()

            while "\n" in buffer:
                message, buffer = buffer.split("\n", 1)

                try:
                    json_data = json.loads(message)
                except:
                    continue

                msg_type = json_data.get("type")

                if msg_type == "system":
                    print(f"\n[SYSTEM] {json_data.get('message')}")
                elif msg_type == "chat":
                    print(f"\n[{json_data.get('sender')}] {json_data.get('text')}")
                elif msg_type == "error":
                    print(f"\n[ERROR] {json_data.get('message')}")

                print("> ", end="", flush=True)

        except:
            break


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    username = input("Enter your username: ").strip()
    client_socket.sendall(username.encode())

    print("\nType messages in format: receiver:message")
    print("Example: Alice:Hello")
    print("Type /exit to quit.\n")

    # Start receiving thread AFTER instructions
    threading.Thread(
        target=receive_messages,
        args=(client_socket,),
        daemon=True
    ).start()

    print("> ", end="", flush=True)

    while True:
        user_input = input().strip()

        if user_input.lower() == "/exit":
            break

        if ":" not in user_input:
            print("Invalid format. Use receiver:message")
            print("> ", end="", flush=True)
            continue

        receiver, text = user_input.split(":", 1)

        if not receiver.strip() or not text.strip():
            print("Receiver and message cannot be empty.")
            print("> ", end="", flush=True)
            continue

        message_data = {
            "receiver": receiver.strip(),
            "text": text.strip()
        }

        client_socket.sendall((json.dumps(message_data) + "\n").encode())

    client_socket.close()
    print("Disconnected from server.")


if __name__ == "__main__":
    start_client()