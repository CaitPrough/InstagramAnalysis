import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext  

from messagesInARow import process_messages_in_folder, get_consecutive_stats

root_folder = 'C:\\Users\\caitp\\OneDrive\\Desktop\\Insta\\inbox'

def set_new_directory():
    selected_folder = combobox.get()
    if selected_folder:
        new_directory = os.path.join(root_folder, selected_folder)
        process_messages_in_folder(new_directory)
        stats_output = get_consecutive_stats()
        show_stats_window(stats_output)

def show_stats_window(stats_output):
    stats_window = tk.Toplevel(root)
    stats_window.title("Consecutive Message Statistics")

    text_area = scrolledtext.ScrolledText(stats_window, width=80, height=30)
    text_area.insert(tk.END, stats_output)
    text_area.pack(padx=10, pady=10)

    stats_window.mainloop()

root = tk.Tk()
root.title("Select User Folder")

folders = [folder for folder in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder, folder))]

combobox = ttk.Combobox(root, values=folders, state="readonly", width=30)
combobox.pack(pady=10)

label = ttk.Label(root, text="Select a Username:")
label.pack(pady=10)

next_button = ttk.Button(root, text="Next", command=set_new_directory)
next_button.pack(pady=10)

root.mainloop()
