import socket
import threading
import json


class NetworkClient:
    def __init__(self, host, port, message_callback):
        self.host = host
        self.port = port
        self.socket = None
        self.buffer = ""
        self.message_callback = message_callback
        self.connected = False

    # Connect to server
    def connect(self, username):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.socket.sendall(username.encode())
        self.connected = True

        threading.Thread(target=self.receive_loop, daemon=True).start()

    # Send message
    def send_message(self, receiver, text):
        if not self.connected:
            return

        message_data = {
            "receiver": receiver,
            "text": text
        }

        self.socket.sendall((json.dumps(message_data) + "\n").encode())

    # Receive messages
    def receive_loop(self):
        while self.connected:
            try:
                data = self.socket.recv(1024)
                if not data:
                    break

                self.buffer += data.decode()

                while "\n" in self.buffer:
                    message, self.buffer = self.buffer.split("\n", 1)
                    try:
                        json_data = json.loads(message)
                        self.message_callback(json_data)
                    except:
                        continue
            except:
                break

    def disconnect(self):
        self.connected = False
        if self.socket:
            self.socket.close()