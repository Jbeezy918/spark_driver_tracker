import tkinter as tk
from tkinter import scrolledtext
import datetime
import subprocess
import sys

# Attempt to import pyttsx3 or install if not available
try:
    import pyttsx3
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyttsx3"])
    import pyttsx3

# Log conversation to file
def log_conversation(user_input, response):
    with open("chat_log.txt", "a") as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] You: {user_input}\n")
        log_file.write(f"[{timestamp}] Spark: {response}\n\n")

# Placeholder logic for Spark
def get_bot_response(user_input):
    if "commands" in user_input.lower():
        return "Here's what I can do: Tell jokes, answer questions, toggle voice, be your favorite assistant 😉"
    return f"You said: {user_input}"

class SparkGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Spark Driver Tracker")

        # Voice toggle (default: ON)
        self.voice_enabled = tk.BooleanVar(value=True)
        self.voice_toggle = tk.Checkbutton(root, text="Voice Output", variable=self.voice_enabled)
        self.voice_toggle.pack(pady=5)

        # Conversation display
        self.chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=15, state='disabled')
        self.chat_display.pack(padx=10, pady=5)

        # User input
        self.entry = tk.Entry(root, width=40)
        self.entry.pack(padx=10, pady=5)
        self.entry.bind("<Return>", self.send_message)

        # Send button
        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)

    def send_message(self, event=None):
        user_input = self.entry.get().strip()
        if not user_input:
            return

        self.display_message(f"You: {user_input}")
        self.entry.delete(0, tk.END)

        response = get_bot_response(user_input)
        self.display_message(f"Spark: {response}")

        log_conversation(user_input, response)

        if self.voice_enabled.get():
            self.speak(response)

    def speak(self, text):
        try:
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            self.display_message(f"Spark: (Voice error — {e})")

    def display_message(self, msg):
        self.chat_display.configure(state='normal')
        self.chat_display.insert(tk.END, msg + "\n")
        self.chat_display.configure(state='disabled')
        self.chat_display.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = SparkGUI(root)
    root.mainloop()
