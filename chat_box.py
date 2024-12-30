import tkinter as tk
import pandas as pd
from datetime import datetime

# Initialize chat history
chat_data = pd.DataFrame(columns=["Timestamp", "User", "Message"])

# Function to handle sending messages
def send_message():
    global chat_data

    user_message = user_input.get()
    if user_message.strip():  # Only proceed if message isn't empty
        # Log the user's message
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_row = pd.DataFrame([{"Timestamp": timestamp, "User": "User", "Message": user_message}])
        chat_data = pd.concat([chat_data, new_row], ignore_index=True)

        # Display user message
        chat_history.config(state=tk.NORMAL)
        chat_history.insert(tk.END, f"User: {user_message}\n")
        chat_history.config(state=tk.DISABLED)
        user_input.delete(0, tk.END)

        # Generate system response
        generate_response(user_message)

def generate_response(user_message):
    global chat_data

    # Example response logic
    if "hello" in user_message.lower():
        response = "Hi there! How can I help you?"
    elif "how are you?" in user_message.lower():
        response = "I'm fine! What about you?"
    elif "how is today" in user_message.lower():
        response = "Good"
    elif "i want movie" in user_message.lower():
        response = "Go to Chrome"
    elif "i want song" in user_message.lower():
        response = "Go to Chrome"
    elif "bye" in user_message.lower():
        response = "Goodbye! Have a great day!"
    else:
        response = "I'm sorry, I didn't understand that."

    # Log the system response
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_row = pd.DataFrame([{"Timestamp": timestamp, "User": "System", "Message": response}])
    chat_data = pd.concat([chat_data, new_row], ignore_index=True)

    # Display system response
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, f"System: {response}\n")
    chat_history.config(state=tk.DISABLED)

def save_chat():
    global chat_data
    chat_data.to_csv("chat_history.csv", index=False)
    print("Chat history saved to chat_history.csv!")

# Tkinter GUI setup
root = tk.Tk()
root.title("Chat Box")

# Make the window full-screen
root.attributes('-fullscreen', True)

# Chat history display with larger font
chat_history = tk.Text(root, height=20, width=70, state=tk.DISABLED, font=("Arial", 20))
chat_history.pack(expand=True, fill="both", padx=20, pady=20)

# Input and buttons frame
input_frame = tk.Frame(root)
input_frame.pack(pady=20)

# User input field with larger font
user_input = tk.Entry(input_frame, width=50, font=("Arial", 20))
user_input.grid(row=0, column=0, padx=10)

# Send button with larger font
send_button = tk.Button(input_frame, text="Send", command=send_message, font=("Arial", 14))
send_button.grid(row=0, column=1, padx=10)

# Save chat button with larger font
save_button = tk.Button(input_frame, text="Save Chat", command=save_chat, font=("Arial", 14))
save_button.grid(row=0, column=2, padx=10)

# Escape key to exit full screen
def exit_fullscreen(event):
    root.attributes('-fullscreen', False)

root.bind('<Escape>', exit_fullscreen)

root.mainloop()
