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

'''Function to display dataset in the Treeview'''
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
        data["Average_Score"] = data[["Math", "Science", "English","Tamil","Social Science"]].mean(axis=1)

        # Top 3 students by average score
        top_students = data.nlargest(3, "Average_Score")
        class_avg = data[["Math", "Science", "English","Tamil","Social Science"]].mean()

        # Update insights text
        insights_text.set(
            f"Top 3 Students by Average Score:\n{top_students[['Student', 'Average_Score']].to_string(index=False)}\n\n"
            f"Class Average (Math, Science, English,Tamil,Social Science):\n{class_avg.to_string()}\n\n"
            f"Highest Scoring Student: {top_students.iloc[0]['Student']} ({top_students.iloc[0]['Average_Score']})\n"
            f"Lowest Scoring Student: {data.loc[data['Average_Score'].idxmin(), 'Student']} ({data.loc[data['Average_Score'].idxmin(), 'Average_Score']})"
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
root.title("Educational Performance Analytics")

# Variables
data = pd.DataFrame()


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

tree = ttk.Treeview(tree_frame, columns=("Student", "Math", "Science", "English","Tamil","Social Science"), show="headings", height=10)
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
