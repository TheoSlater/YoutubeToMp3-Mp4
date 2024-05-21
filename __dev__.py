# Created by Theo Slater
# This is open source. Please give me credit.

# DEV
import tkinter as tk
from tkinter import StringVar, scrolledtext
from pytube import YouTube
from moviepy.editor import VideoFileClip
import threading
import os
import customtkinter as ctk
import sys

mp3_conversion_triggered = False
ctk.set_appearance_mode("dark")


class ConsoleOutput:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.default_color = "white"  # Default text color


    def write(self, message):
        self.text_widget.configure(state='normal')
        self.text_widget.insert(tk.END, message)
        self.text_widget.configure(state='disabled')
        self.text_widget.yview(tk.END)

    def flush(self):
        pass


class ConsoleApp:
    def __init__(self, root):
        self.root = root
        self.console_enabled = True

        self.text_area = ctk.CTkTextbox(root, height=100, width=400)
        self.text_area.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        self.entry = ctk.CTkEntry(root, width=400)
        self.entry.grid(row=4, column=0, padx=10, pady=10, sticky="we")
        self.entry.bind('<Return>', self.process_command)

        self.console_output = ConsoleOutput(self.text_area)
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        sys.stdout = self.console_output
        sys.stderr = self.console_output

    def process_command(self, event):
        command = self.entry.get()
        if command:
            self.entry.delete(0, ctk.END)
            self.display_command(command)
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
            if len(parts) > 1:
                if parts[1].lower() == "on":
                    self.console_enabled = True
                    sys.stdout = self.console_output
                    sys.stderr = self.console_output
                    return "Console output enabled."
                elif parts[1].lower() == "off":
                    self.console_enabled = False
                    sys.stdout = self.original_stdout
                    sys.stderr = self.original_stderr
                    return "Console output disabled."
                
            return "Usage: console output [on/off]"
        
        else:
            return f"Unknown command: {command}"

def download_mp4(url_entry):
    url = url_entry.get()
    output_path = '.' 

    try:
        yt = YouTube(url)
        mp4_stream = yt.streams.filter(file_extension='mp4').first()

        if mp4_stream:
            mp4_file_path = mp4_stream.download(output_path)
            print(f"Downloaded MP4: {mp4_file_path}")
        else:
            print("Mp4 stream not found")

    except Exception as e:
        print(f'Error Downloading mp4: {e}')

def download_and_convert(url_entry):
    url = url_entry.get()
    output_path = '.' 

    try:
        yt = YouTube(url)
        mp4_stream = yt.streams.filter(file_extension='mp4').first()

        if mp4_stream:
            mp4_file_path = mp4_stream.download(output_path)
            threading.Thread(target=convert_to_mp3, args=(mp4_file_path,)).start()
        else:
            print("MP4 stream not found.")

    except Exception as e:
        print(f'Error downloading MP4: {e}')

def convert_to_mp3(video_file_path):
    try:
        video = VideoFileClip(video_file_path)
        audio = video.audio
        audio.write_audiofile(video_file_path.replace('.mp4', '_converted.mp3'), codec='mp3', fps=44100)
        video.close()

        os.remove(video_file_path)
        print('Successfully downloaded and converted to MP3.')

    except Exception as e:
        print(f'Error converting to MP3: {e}')

def main():
    root = ctk.CTk()
    root.title("YouTube To Mp3 (DEV)")

    window_width = 600
    window_height = 600
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

    button_frame = ctk.CTkFrame(root)
    button_frame.grid(row=1, column=0, padx=10, pady=(0, 5), sticky="we")

    download_mp4_button = ctk.CTkButton(button_frame, text="Download MP4", command=lambda: download_mp4(url_entry))
    download_mp4_button.grid(row=0, column=0, padx=5, pady=(0, 5))

    download_and_convert_button = ctk.CTkButton(button_frame, text="Download and Convert to MP3", command=lambda: download_and_convert(url_entry))
    download_and_convert_button.grid(row=0, column=1, padx=5, pady=(0, 5))

    root.grid_rowconfigure(0, weight=0)  
    root.grid_rowconfigure(1, weight=0) 
    root.grid_columnconfigure(0, weight=1) 

    console_app = ConsoleApp(root)
    root.grid_rowconfigure(3, weight=1)  
    root.grid_rowconfigure(4, weight=0)  

    root.mainloop()

if __name__ == "__main__":
    main()
