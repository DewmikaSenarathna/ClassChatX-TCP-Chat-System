import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
from PIL import Image, ImageTk
from client.network_client import NetworkClient

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000


class ClassChatXUI:

    def __init__(self, root):
        self.root = root
        self.root.title("ClassChatX")
        self.root.geometry("750x600")
        self.root.configure(bg="#1e1e1e")

        self.network = NetworkClient(
            SERVER_HOST,
            SERVER_PORT,
            self.handle_incoming_message
        )

        self.logo_image = None
        self.username = None

        self.load_logo()
        self.create_login_screen()

    # Load logo (preserve shape)
    def load_logo(self):
        try:
            image = Image.open("classchatx-logo.png")
            image.thumbnail((220, 220), Image.LANCZOS)
            self.logo_image = ImageTk.PhotoImage(image)
        except:
            self.logo_image = None

    # LOGIN SCREEN
    def create_login_screen(self):
        self.clear_window()

        container = tk.Frame(self.root, bg="#1e1e1e")
        container.pack(expand=True)

        if self.logo_image:
            tk.Label(container,
                     image=self.logo_image,
                     bg="#1e1e1e").pack(pady=20)

        tk.Label(container,
                 text="ClassChatX",
                 font=("Segoe UI", 30, "bold"),
                 fg="#4da6ff",
                 bg="#1e1e1e").pack(pady=10)

        tk.Label(container,
                 text="Academic Communication Platform",
                 font=("Segoe UI", 13),
                 fg="#bbbbbb",
                 bg="#1e1e1e").pack(pady=5)

        tk.Label(container,
                 text="Enter Username",
                 font=("Segoe UI", 12),
                 fg="white",
                 bg="#1e1e1e").pack(pady=20)

        self.username_entry = tk.Entry(container,
                                       font=("Segoe UI", 13),
                                       width=30,
                                       justify="center")
        self.username_entry.pack(pady=10)

        tk.Button(container,
                  text="Connect",
                  font=("Segoe UI", 12, "bold"),
                  bg="#4da6ff",
                  fg="white",
                  width=20,
                  command=self.connect).pack(pady=25)

    # CHAT SCREEN
    def create_chat_screen(self):
        self.clear_window()

        header = tk.Frame(self.root, bg="#2d2d2d", height=60)
        header.pack(fill=tk.X)

        tk.Label(header,
                 text="ClassChatX",
                 font=("Segoe UI", 18, "bold"),
                 fg="#4da6ff",
                 bg="#2d2d2d").pack(side=tk.LEFT, padx=20)

        tk.Label(header,
                 text=f"Logged in as {self.username}",
                 font=("Segoe UI", 11),
                 fg="white",
                 bg="#2d2d2d").pack(side=tk.RIGHT, padx=20)

        receiver_frame = tk.Frame(self.root, bg="#1e1e1e")
        receiver_frame.pack(pady=15)

        tk.Label(receiver_frame,
                 text="Chat with:",
                 fg="white",
                 bg="#1e1e1e").pack(side=tk.LEFT)

        self.receiver_entry = tk.Entry(receiver_frame)
        self.receiver_entry.pack(side=tk.LEFT, padx=10)

        self.chat_area = scrolledtext.ScrolledText(
            self.root,
            bg="#252526",
            fg="white",
            state='disabled'
        )
        self.chat_area.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        message_frame = tk.Frame(self.root, bg="#1e1e1e")
        message_frame.pack(fill=tk.X, padx=20, pady=15)

        self.message_entry = tk.Entry(message_frame)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        tk.Button(message_frame,
                  text="Send",
                  bg="#4da6ff",
                  fg="white",
                  width=10,
                  command=self.send_message).pack(side=tk.RIGHT)

    # CONNECT
    def connect(self):
        self.username = self.username_entry.get().strip()
        if not self.username:
            return

        self.network.connect(self.username)
        self.create_chat_screen()

    # SEND
    def send_message(self):
        receiver = self.receiver_entry.get().strip()
        message = self.message_entry.get().strip()

        if not receiver or not message:
            return

        self.network.send_message(receiver, message)
        self.message_entry.delete(0, tk.END)

    # HANDLE INCOMING MESSAGE
    def handle_incoming_message(self, data):
        timestamp = datetime.now().strftime("%H:%M:%S")

        self.chat_area.config(state='normal')

        msg_type = data.get("type")

        if msg_type == "system":
            self.chat_area.insert(tk.END,
                                  f"[{timestamp}] [SYSTEM] {data.get('message')}\n")
        elif msg_type == "chat":
            self.chat_area.insert(tk.END,
                                  f"[{timestamp}] {data.get('sender')}: {data.get('text')}\n")
        elif msg_type == "error":
            self.chat_area.insert(tk.END,
                                  f"[{timestamp}] [ERROR] {data.get('message')}\n")

        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ClassChatXUI(root)
    root.mainloop()
