import tkinter as tk
from tkinter import filedialog
import json
import os
import subprocess

# Define default apps
default_apps = {
    "Google Chrome": "/Applications/Google Chrome.app",
    "Safari": "/Applications/Safari.app",
    "Firefox": "/Applications/Firefox.app",
    "TextEdit": "/Applications/TextEdit.app"
}

def on_submit():
    """Handle the submit action."""
    try:
        selected_indices = app_listbox.curselection()
        selected_apps = {app_listbox.get(i): apps[app_listbox.get(i)] for i in selected_indices}

        # Save selected apps to JSON file
        with open("selected_apps.json", "w") as f:
            json.dump(selected_apps, f, indent=4)

        # Run the main.py script
        subprocess.Popen(["python3", "main.py"])

        root.destroy()  # Close the app selector window
    except Exception as e:
        print(f"Error during submission: {e}")

def browse_app_folder():
    """Open a file dialog to browse for application folder."""
    folder_path = filedialog.askdirectory(title="Select Applications Folder")
    if folder_path:
        detect_apps_in_folder(folder_path)
        update_app_list()

def update_app_list():
    """Update the listbox with application names."""
    app_listbox.delete(0, tk.END)
    for app in apps:
        if apps[app] not in default_apps.values():  # Exclude default apps
            app_listbox.insert(tk.END, app)

def detect_apps_in_folder(folder_path):
    """Detect apps in a folder and add to the app list."""
    for app_name in os.listdir(folder_path):
        if app_name.endswith('.app'):  # MacOS application extension
            app_path = os.path.join(folder_path, app_name)
            app_name_only = app_name.replace('.app', '')  # Remove the .app suffix for display
            apps[app_name_only] = app_path  # Store path as string

root = tk.Tk()
root.title("App Selector")
root.geometry("300x400")

# Browse button to select app folder
browse_button = tk.Button(root, text="Browse Applications", command=browse_app_folder)
browse_button.pack(pady=10)

# Listbox to show applications
app_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
app_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

# Initialize apps dictionary and detect apps in /Applications directory
apps = {}
detect_apps_in_folder("/Applications")

# Update the listbox with detected apps
update_app_list()

# Submit button
submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.pack(pady=10)

root.mainloop()