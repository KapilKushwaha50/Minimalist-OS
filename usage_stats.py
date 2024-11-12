import tkinter as tk
from tkinter import ttk
import json
from datetime import datetime

def display_usage_stats(root):
    # Load usage data from JSON file
    try:
        with open("usage_stats.json", "r") as f:
            usage_data = json.load(f)
    except FileNotFoundError:
        usage_data = {}

    # Create a new window to display usage stats
    stats_window = tk.Toplevel(root)
    stats_window.title("Usage Statistics")
    stats_window.geometry("400x400")
    stats_window.configure(bg="black")

    # Date label (created only once)
    date_label = tk.Label(stats_window, text=f"Usage on {datetime.now().strftime('%Y-%m-%d')}", bg="black", fg="white", font=("Helvetica", 14))
    date_label.pack(pady=10)

    for app_name, time_spent in usage_data.items():
        time_in_minutes = time_spent // 60  # Convert seconds to minutes
        time_in_seconds = time_spent - time_in_minutes
        app_label = tk.Label(stats_window, text=f"{app_name}: {time_in_minutes} min {time_in_seconds} sec", bg="black", fg="white", font=("Helvetica", 12))
        app_label.pack(pady=5)

    # Create the Treeview for displaying the data (initially empty)
    tree = ttk.Treeview(stats_window, columns=("App Name", "Time Spent (Minutes)"), show="headings")
    tree.heading("App Name", text="App Name")
    tree.heading("Time Spent (Minutes)", text="Time Spent (Minutes)")
    tree.pack(fill=tk.BOTH, expand=True)

    # Button to show usage data in the table
    def show_table():
        # Clear any previous rows
        for row in tree.get_children():
            tree.delete(row)

        # Populate the Treeview with data
        for app_name, time_spent in usage_data.items():
            time_in_minutes = time_spent // 60  # Convert seconds to minutes
            tree.insert("", "end", values=(app_name, time_in_minutes))

    # Add the button to show the table
    table_button = tk.Button(stats_window, text="Show Usage Data", command=show_table)
    table_button.pack(pady=10)