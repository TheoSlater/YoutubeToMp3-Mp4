# Created by Theo Slater
# This is an open source project. Do whatever you want with it.


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
        self.text_area = ctk.CTkTextbox(self.root, height=100, width=400)
        self.text_area.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        self.text_area.grid_remove()

        self.entry = ctk.CTkEntry(self.root, width=400)
        self.entry.grid(row=4, column=0, padx=10, pady=10, sticky="we")
        self.entry.grid_remove()
        self.entry.bind('<Return>', self.process_command)
        self.entry.bind('<Up>', self.show_previous_command)
        self.entry.bind('<Down>', self.show_next_command)

        self.console_output = ConsoleOutput(self.text_area)

    def redirect_output(self):
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        self.console_output = ConsoleOutput(self.text_area)
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
        return "Usage: console output [on/off]"

    def show_previous_command(self, event):
        if self.command_history and self.history_index > 0:
            self.history_index -= 1
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.command_history[self.history_index])

    def show_next_command(self, event):
        if self.command_history and self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.command_history[self.history_index])
        elif self.history_index == len(self.command_history) - 1:
            self.history_index += 1
            self.entry.delete(0, tk.END)

    def open_dev_console(self):
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
    try:
        file_ext = format.lower()
        output_template = f"%(title)s.{file_ext}"

        command = [
            'python', '-m', 'yt_dlp', url,
            '-x', '--audio-format', file_ext,
            '--audio-quality', '0',
            '--embed-metadata',
            '-o', output_template
        ]

        if file_ext in ['mp3', 'm4a', 'mkv', 'mp4', 'ogg', 'opus', 'flac', 'mka', 'm4v', 'mov']:
            command.append('--embed-thumbnail')

        subprocess.run(command, check=True)
        print(f"Downloaded and converted audio: {output_template}")
    except subprocess.CalledProcessError as e:
        print(f'Error Downloading Audio: {e}')
    except Exception as e:
        print(f'Error: {e}')

def toggle_console_visibility(console_app, root):
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
    window_height = 200
    expanded_window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = int((screen_width - window_width) / 2)
    y_coordinate = int((screen_height - window_height) / 2)
    root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    # Configure grid to make UI responsive
    root.grid_columnconfigure(0, weight=1)  # Allows column 0 to expand
    root.grid_rowconfigure(2, weight=0)     # Ensure row 2 (button) has proper height
    root.grid_rowconfigure(3, weight=1)     # Allows row 3 (console) to expand

    url_var = StringVar()
    url_entry = ctk.CTkEntry(root, textvariable=url_var, width=400)
    url_entry.insert(0, "Paste YouTube URL here")
    url_entry.bind("<FocusIn>", lambda event: url_entry.delete("0", "end") if url_entry.get() == "Paste YouTube URL here" else None)
    url_entry.grid(row=0, column=0, padx=10, pady=10, sticky="we") 

    format_var = StringVar(value="mp3")
    format_menu = ctk.CTkOptionMenu(root, variable=format_var, values=["mp3", "wav", "m4a"])
    format_menu.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="we")  #

    # Create frame for button and ensure it expands properly
    button_frame = ctk.CTkFrame(root, fg_color=root.cget("bg"))  # Match frame color to root background
    button_frame.grid(row=2, column=0, padx=10, pady=(0, 5), sticky="we")

    download_audio_button = ctk.CTkButton(button_frame, text="Download and Convert Audio", command=lambda: threading.Thread(target=download_audio, args=(url_var.get(), format_var.get())).start())
    download_audio_button.grid(row=0, column=0, padx=5, pady=(0, 5), sticky="we")  # Make button take full width

    # Configure button_frame to ensure it does not collapse
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_rowconfigure(0, weight=1)

    console_app = ConsoleApp(root)
    root.grid_rowconfigure(3, weight=1)

    root.bind("<Control-d>", lambda event: toggle_console_visibility(console_app, root))

    root.mainloop()

if __name__ == "__main__":
    main()


