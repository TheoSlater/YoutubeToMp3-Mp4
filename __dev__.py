import tkinter as tk
from tkinter import StringVar
from pytube import YouTube
from moviepy.editor import VideoFileClip
import threading
import os
import customtkinter as ctk
from customtkinter import CTkToplevel
import sys

mp3_conversion_triggered = False
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
        self.root.after(100, self.update_dev_console)  # Update every 100 milliseconds

def download_mp4(url):
    try:
        yt = YouTube(url)
        mp4_stream = yt.streams.filter(file_extension='mp4').first()
        if mp4_stream:
            mp4_file_path = mp4_stream.download('.')
            print(f"Downloaded MP4: {mp4_file_path}")
        else:
            print("MP4 stream not found")
    except Exception as e:
        print(f'Error Downloading MP4: {e}')

def download_and_convert(url, desired_format):
    try:
        yt = YouTube(url)
        mp4_stream = yt.streams.filter(file_extension='mp4').first()
        if mp4_stream:
            mp4_file_path = mp4_stream.download('.')
            threading.Thread(target=convert_to_audio, args=(mp4_file_path, desired_format)).start()
        else:
            print("MP4 stream not found.")
    except Exception as e:
        print(f'Error downloading MP4: {e}')

def convert_to_audio(video_file_path, format):
    try:
        video = VideoFileClip(video_file_path)
        audio = video.audio
        audio_file_path = video_file_path.replace('.mp4', f'_converted.{format.lower()}')
        audio.write_audiofile(audio_file_path, codec='mp3' if format == 'MP3' else 'pcm_s16le', fps=44100)
        video.close()
        os.remove(video_file_path)
        print(f'Successfully downloaded and converted to {format}.')
    except Exception as e:
        print(f'Error converting to {format}: {e}')

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
    root.title("YouTube To Audio (DEV)")

    window_width = 600
    window_height = 200
    expanded_window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = int((screen_width - window_width) / 2)
    y_coordinate = int((screen_height - window_height) / 2)
    root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    url_var = StringVar()
    url_entry = ctk.CTkEntry(root, textvariable=url_var, width=400)
    url_entry.insert(0, "Paste YouTube URL here")
    url_entry.bind("<FocusIn>", lambda event: url_entry.delete("0", "end") if url_entry.get() == "Paste YouTube URL here" else None)
    url_entry.grid(row=0, column=0, padx=10, pady=10, sticky="we")

    format_var = StringVar(value="MP3")
    format_menu = ctk.CTkOptionMenu(root, variable=format_var, values=["MP3", "WAV"])
    format_menu.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="we")

    button_frame = ctk.CTkFrame(root)
    button_frame.grid(row=2, column=0, padx=10, pady=(0, 5), sticky="we")

    download_mp4_button = ctk.CTkButton(button_frame, text="Download MP4", command=lambda: download_mp4(url_var.get()))
    download_mp4_button.grid(row=0, column=0, padx=5, pady=(0, 5))

    download_and_convert_button = ctk.CTkButton(button_frame, text="Download and Convert to Audio", command=lambda: download_and_convert(url_var.get(), format_var.get()))
    download_and_convert_button.grid(row=0, column=1, padx=5, pady=(0, 5))

    root.grid_rowconfigure(0, weight=0)
    root.grid_rowconfigure(1, weight=0)
    root.grid_rowconfigure(2, weight=0)
    root.grid_columnconfigure(0, weight=1)

    console_app = ConsoleApp(root)
    root.grid_rowconfigure(3, weight=1)
    root.grid_rowconfigure(4, weight=0)

    root.bind("`", lambda event: toggle_console_visibility(console_app, root))

    root.mainloop()

if __name__ == "__main__":
    main()
