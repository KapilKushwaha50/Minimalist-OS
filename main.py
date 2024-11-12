import tkinter as tk
from tkinter import simpledialog
from tkinter import font as tkFont
from datetime import datetime
import subprocess
import json
import os
import signal  # for killing background process
from PIL import Image, ImageTk  # Importing PIL modules

# Define default apps
default_apps = {
    "Google Chrome": "/Applications/Google Chrome.app",
    "Safari": "/Applications/Safari.app",
    "Firefox": "/Applications/Firefox.app",
    "TextEdit": "/Applications/TextEdit.app"
}

# Define password (hardcoded for simplicity)
PASSWORD = "Kapil"

def update_time():
    """Updates the time and date labels every second."""
    current_time = datetime.now().strftime('%H:%M')
    seconds = datetime.now().strftime('%S')
    current_date = datetime.now().strftime('%A, %d %B %Y')

    time_label.config(text=current_time)
    seconds_label.config(text=seconds)
    date_label.config(text=current_date)

    root.after(1000, update_time)

def quit_with_password():
    """Prompt user for password before quitting."""
    user_input = simpledialog.askstring("Password", "Enter password to quit:", show='*')
    if user_input == PASSWORD:
        root.quit()
    else:
        tk.messagebox.showerror("Error", "Incorrect password!")

def create_launcher(apps, data_collector_process):
    """Creates the Tkinter GUI for the application launcher."""
    global time_label, seconds_label, date_label, root

    root = tk.Tk()
    root.title("Minimalist Launcher")
    root.geometry("400x500")  # Set initial size (will be adjusted by the background image)
    root.configure(bg="black")

    # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Load background image using Pillow
    image = Image.open("BGGGG.jpg")  # Make sure to use the correct path to your image
    image = image.resize((screen_width, screen_height), Image.ANTIALIAS)  # Resize image to fit screen
    background_image = ImageTk.PhotoImage(image)

    # Create a label to hold the image
    background_label = tk.Label(root, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Fill the whole window

    # Navigation bar frame
    nav_bar = tk.Frame(root, bg="#999999", height=30)
    nav_bar.pack(side="top", fill="x")

    # Add navigation items
    nav_items = {
        "System Settings": lambda: print("System Settings Clicked"),
        "Quit": quit_with_password
    }

    for text, command in nav_items.items():
        label = tk.Label(nav_bar, text=text,bg="#999999", fg="black", font=("Helvetica", 12, "bold"))
        label.pack(side="left", padx=10)
        label.bind("<Button-1>", lambda e, cmd=command: cmd())

    # Frame for time display
    time_frame = tk.Frame(root, bg="black")
    time_frame.pack(side="top", pady=30)

    time_label = tk.Label(time_frame, bg="black", fg="white", font=("Helvetica", 34, "bold"))
    time_label.pack(side="left")

    seconds_label = tk.Label(time_frame, text="", bg="black", fg="white", font=("Helvetica", 14, "bold"))
    seconds_label.pack(side="left", padx=(5, 0))

    date_label = tk.Label(root, text="", bg="black", fg="white", font=("Helvetica", 14, "bold"))
    date_label.pack(side="top")

    # Create a frame to hold the labels for apps
    frame = tk.Frame(root, bg="black", pady=20)
    frame.pack(side="left", padx=20, pady=20)

    helvetica_font = ("Helvetica", 10, "bold")

    for app_name, app_path in apps.items():
        app_data = {"name": app_name, "path": app_path}
        label = tk.Label(frame, text=app_name, bg="black", fg="white", font=helvetica_font, pady=5, padx=10, anchor="w")
        label.pack(fill=tk.X, pady=5)

        # Hover effect
        def on_enter(event, label=label):
            label.config(bg="gray")

        def on_leave(event, label=label):
            label.config(bg="black")

        label.bind("<Enter>", on_enter)
        label.bind("<Leave>", on_leave)

    # Initialize time update
    update_time()

    # Set up quit handler
    def on_quit():
        """Handle clean-up when app is closed."""
        if data_collector_process:
            os.kill(data_collector_process.pid, signal.SIGTERM)  # Kill data collector process
        root.quit()

    root.protocol("WM_DELETE_WINDOW", on_quit)  # Close app and stop data collector

    root.mainloop()


if __name__ == "__main__": # Load selected apps from JSON before creating the launcher

    # Start data collection script in the background
    data_collector_process = subprocess.Popen(["python3", "data_collector.py"])

    create_launcher(default_apps, data_collector_process)
