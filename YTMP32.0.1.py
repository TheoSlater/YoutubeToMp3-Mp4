# Created by Theo Slater
# This is an open-source project. Do whatever you want with it.

import tkinter as tk
from tkinter import StringVar
import threading
import os
import customtkinter as ctk
from customtkinter import CTkToplevel
import sys
import yt_dlp as ytdlp
import subprocess

ctk.set_appearance_mode("dark")

class ConsoleOutput:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.output_buffer = []

    def write(self, message):
        self.output_buffer.append(message)
        self.update_output()

    def update_output(self):
        output_text = ''.join(self.output_buffer)
        self.text_widget.configure(state='normal')
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, output_text)
        self.text_widget.configure(state='disabled')
        self.text_widget.yview(tk.END)

    def flush(self):
        pass

class ConsoleApp:
    def __init__(self, root):
        self.root = root
        self.console_visible = False
        self.command_history = []
        self.history_index = -1

        self.setup_widgets()
        self.redirect_output()

    def setup_widgets(self):
        """Set up the text console and input fields."""
        self.text_area = ctk.CTkTextbox(self.root)
        self.text_area.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")  # Full width and height

        self.entry = ctk.CTkEntry(self.root, placeholder_text="Enter command here...")
        self.entry.grid(row=2, column=0, padx=10, pady=10, sticky="we")  # Full width

        self.entry.bind('<Return>', self.process_command)
        self.entry.bind('<Up>', self.show_previous_command)
        self.entry.bind('<Down>', self.show_next_command)

        self.console_output = ConsoleOutput(self.text_area)



    def redirect_output(self):
        """Redirect console output to the custom text area."""
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        sys.stdout = self.console_output
        sys.stderr = self.console_output

    def process_command(self, event):
        command = self.entry.get().strip()
        if command:
            self.entry.delete(0, tk.END)
            self.display_command(command)
            self.command_history.append(command)
            self.history_index = len(self.command_history)
            result = self.execute_command(command)
            if result:
                self.display_output(result)

    def display_command(self, command):
        self.text_area.configure(state='normal')
        self.text_area.insert(tk.END, f"> {command}\n")
        self.text_area.configure(state='disabled')
        self.text_area.yview(tk.END)

    def display_output(self, output):
        self.text_area.configure(state='normal')
        self.text_area.insert(tk.END, f"{output}\n")
        self.text_area.configure(state='disabled')
        self.text_area.yview(tk.END)

    def execute_command(self, command):
        """Execute basic shell-like commands."""
        parts = command.split()
        if not parts:
            return "No command entered."

        cmd = parts[0].lower()

        if cmd == "hello":
            return "Hello, World!"
        elif cmd == "console":
            return self.toggle_console(parts)
        elif cmd == "dev" and len(parts) > 1 and parts[1].lower() == "console":
            self.open_dev_console()
            return "Developer console opened."
        else:
            return f"Unknown command: {command}"

    def toggle_console(self, parts):
        """Enable or disable the console output based on user input."""
        if len(parts) > 1:
            if parts[1].lower() == "on":
                self.console_visible = True
                sys.stdout = self.console_output
                sys.stderr = self.console_output
                return "Console output enabled."
            elif parts[1].lower() == "off":
                self.console_visible = False
                sys.stdout = self.original_stdout
                sys.stderr = self.original_stderr
                return "Console output disabled."
        return "Usage: console [on/off]"

    def show_previous_command(self, event):
        """Handle browsing through command history."""
        if self.command_history and self.history_index > 0:
            self.history_index -= 1
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.command_history[self.history_index])

    def show_next_command(self, event):
        """Handle forward navigation through command history."""
        if self.command_history and self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.command_history[self.history_index])
        elif self.history_index == len(self.command_history) - 1:
            self.history_index += 1
            self.entry.delete(0, tk.END)

    def open_dev_console(self):
        """Open a new developer console window."""
        dev_console_window = CTkToplevel(self.root)
        dev_console_window.title("Developer Console")
        dev_console_window.geometry("600x400")

        self.dev_console_text = ctk.CTkTextbox(dev_console_window)
        self.dev_console_text.pack(expand=True, fill='both', padx=10, pady=10)

        self.update_dev_console()

    def update_dev_console(self):
        self.dev_console_text.configure(state='normal')
        self.dev_console_text.delete(1.0, tk.END)
        self.dev_console_text.insert(tk.END, ''.join(self.console_output.output_buffer))
        self.dev_console_text.configure(state='disabled')
        self.dev_console_text.yview(tk.END)
        self.root.after(100, self.update_dev_console)

def download_audio(url, format):
    """Download audio or video from YouTube using yt-dlp."""
    try:
        file_ext = format.lower()
        output_template = f"%(title)s.{file_ext}"

        command = ['python', '-m', 'yt_dlp', url]

        if file_ext == "mp4":
            # Download video in mp4 format only
            command += ['-f', 'bestvideo[ext=mp4]+bestaudio[ext=mp4]/mp4', '-o', output_template]
        else:
            # Download audio
            command += ['-x', '--audio-format', file_ext, '--audio-quality', '0', '--embed-metadata', '-o', output_template]

            if file_ext in ['mp3', 'wav', 'mkv', 'ogg', 'opus', 'flac', 'mka', 'm4v', 'mov']:
                command.append('--embed-thumbnail')

        subprocess.run(command, check=True)
        print(f"Downloaded and converted to {file_ext}: {output_template}")
    except subprocess.CalledProcessError as e:
        print(f'Error Downloading: {e}')
    except Exception as e:
        print(f'Error: {e}')


def toggle_console_visibility(console_app, root):
    """Toggle visibility of the console area."""
    if console_app.console_visible:
        console_app.text_area.grid_remove()
        console_app.entry.grid_remove()
        root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
    else:
        console_app.text_area.grid()
        console_app.entry.grid()
        root.geometry(f"{window_width}x{expanded_window_height}+{x_coordinate}+{y_coordinate}")
    console_app.console_visible = not console_app.console_visible


def main():
    global window_width, window_height, expanded_window_height, x_coordinate, y_coordinate

    root = ctk.CTk()
    root.title("YouTube To Audio")

    window_width = 600
    window_height = 50
    expanded_window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = int((screen_width - window_width) / 2)
    y_coordinate = int((screen_height - window_height) / 2)
    root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    # Disable window resizing
    root.resizable(False, False)

    # Set column and row configurations to ensure full window expansion
    root.grid_columnconfigure(0, weight=1)  # Make column fill width
    root.grid_rowconfigure(1, weight=1)     # Make console area fill height
    root.grid_rowconfigure(2, weight=0)     # Fixed row for input

    # Create URL entry field
    url_var = StringVar()
    url_entry = ctk.CTkEntry(root, textvariable=url_var, placeholder_text="Paste YouTube URL here")
    url_entry.grid(row=0, column=0, padx=10, pady=10, sticky="we")  # Full width

    # Create format selection dropdown
    format_var = StringVar(value="mp3")  # Default value set to mp3
    format_menu = ctk.CTkOptionMenu(root, variable=format_var, values=["mp3", "wav", "mp4"])  # Added "mp4" here
    format_menu.grid(row=0, column=1, padx=10, pady=10, sticky="we")  # Full width

    # Create download button
    download_audio_button = ctk.CTkButton(root, text="Download", 
                                          command=lambda: threading.Thread(target=download_audio, args=(url_var.get(), format_var.get())).start())
    download_audio_button.grid(row=0, column=2, padx=10, pady=10, sticky="we")  # Full width

    # Create console app
    console_app = ConsoleApp(root)

    # Bind Ctrl+D to toggle the console
    root.bind('<Control-d>', lambda event: toggle_console_visibility(console_app, root))

    root.mainloop()



if __name__ == "__main__":
    main()
