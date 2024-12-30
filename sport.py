import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import numpy as np

# Function to load dataset
def load_file():
    global data
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            data = pd.read_csv(file_path)
            messagebox.showinfo("File Loaded", "Dataset loaded successfully!")
            display_data(data)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")

# Function to display dataset in the Treeview
def display_data(df):
    for col in tree["columns"]:
        tree.heading(col, text=col)
    tree.delete(*tree.get_children())  # Clear the treeview
    for _, row in df.iterrows():
        tree.insert("", tk.END, values=list(row))

# Function to process data and display insights
def process_data():
    if data.empty:
        messagebox.showwarning("No Data", "Please load a dataset first.")
        return

    try:
        # Add derived metrics
        data["Goals_per_Match"] = data["Goals"] / data["Matches"]
        data["Minutes_per_Goal"] = np.where(data["Goals"] > 0, data["Minutes_Played"] / data["Goals"], 0)

        # Top players by goals
        top_players = data.nlargest(3, "Goals")
        team_goals = data.groupby("Team")["Goals"].sum().sort_values(ascending=False)
        team_avg_goals = data.groupby("Team")["Goals_per_Match"].mean().sort_values(ascending=False)

        # Update insights text
        insights_text.set(
            f"Top 3 Players by Goals:\n{top_players[['Player', 'Goals']].to_string(index=False)}\n\n"
            f"Team Goals:\n{team_goals.to_string()}\n\n"
            f"Team Avg Goals per Match:\n{team_avg_goals.to_string()}\n\n"
            f"Best Goals per Match: {data.loc[data['Goals_per_Match'].idxmax(), 'Player']}\n"
            f"Highest Scoring Team: {team_goals.idxmax()} ({team_goals.max()} goals)"
        )
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process data: {e}")

# Function to save processed data
def save_file():
    if data.empty:
        messagebox.showwarning("No Data", "Please process the data before saving.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            data.to_csv(file_path, index=False)
            messagebox.showinfo("File Saved", "Processed data saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")

# GUI Setup
root = tk.Tk()
root.title("Sports Analytics")

# Variables
data = pd.DataFrame()  # To hold the dataset
insights_text = tk.StringVar()

# File Buttons
file_frame = tk.Frame(root)
file_frame.pack(pady=10)

load_button = tk.Button(file_frame, text="Load Dataset", command=load_file, width=15)
load_button.pack(side=tk.LEFT, padx=5)

process_button = tk.Button(file_frame, text="Process Data", command=process_data, width=15)
process_button.pack(side=tk.LEFT, padx=5)

save_button = tk.Button(file_frame, text="Save Processed Data", command=save_file, width=20)
save_button.pack(side=tk.LEFT, padx=5)

# Treeview for displaying dataset
tree_frame = tk.Frame(root)
tree_frame.pack(pady=10)

tree = ttk.Treeview(tree_frame, columns=("Player", "Team", "Goals", "Assists", "Matches", "Minutes_Played"), show="headings", height=10)
tree.pack(side=tk.LEFT)

scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tree.configure(yscroll=scrollbar.set)

# Insights Section
insights_label = tk.Label(root, text="Insights", font=("Arial", 14, "bold"))
insights_label.pack(pady=10)

insights_frame = tk.Frame(root)
insights_frame.pack(pady=5)

insights_box = tk.Label(insights_frame, textvariable=insights_text, anchor="w", justify="left", bg="white", width=80, height=15, relief="solid", padx=5, pady=5)
insights_box.pack()

# Run the GUI
root.mainloop()
