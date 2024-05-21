# Created by Theo Slater
# This is open source. Please give me credit.


# RELEASE
import tkinter as tk
from tkinter import StringVar, messagebox
from pytube import YouTube
from moviepy.editor import VideoFileClip
import threading
import os

import customtkinter as ctk

ctk.set_appearance_mode("dark")

def download_mp4(url_entry):
    url = url_entry.get()
    output_path = '.'

    try:
        yt = YouTube(url)
        mp4_stream = yt.streams.filter(file_extension='mp4').first()

        if mp4_stream:
            mp4_file_path = mp4_stream.download(output_path)
            messagebox.showinfo("Download Complete", "MP4 downloaded successfully.")
        else:
            messagebox.showerror("Error", "MP4 stream not found.")

    except Exception as e:
        messagebox.showerror("Error", f'Error Downloading MP4: {e}')

def download_and_convert(url_entry):
    url = url_entry.get()
    output_path = '.'

    try:
        yt = YouTube(url)
        mp4_stream = yt.streams.filter(file_extension='mp4').first()

        if mp4_stream:
            mp4_file_path = mp4_stream.download(output_path)
            threading.Thread(target=convert_to_mp3, args=(mp4_file_path,)).start()
            messagebox.showinfo("Download Complete", "MP4 downloaded. Conversion to MP3 started.")
        else:
            messagebox.showerror("Error", "MP4 stream not found.")

    except Exception as e:
        messagebox.showerror("Error", f'Error Downloading MP4: {e}')

def convert_to_mp3(video_file_path):

    try:
        video = VideoFileClip(video_file_path)
        audio = video.audio
        audio.write_audiofile(video_file_path.replace('.mp4', '_converted.mp3'), codec='mp3', fps=44100)
        video.close()

        os.remove(video_file_path)
        messagebox.showinfo("Conversion Complete", "MP3 conversion completed successfully.")

    except Exception as e:
        messagebox.showerror("Error", f'Error converting to MP3: {e}')

def main():

    root = ctk.CTk()
    root.title("YouTube To Mp3")

    window_width = 345
    window_height = 90
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

    download_mp4_button = ctk.CTkButton(root, text="Download MP4", command=lambda: threading.Thread(target=download_mp4, args=(url_entry,)).start())
    download_mp4_button.grid(row=1, column=0, padx=5, pady=(0, 5), sticky="w")

    download_and_convert_button = ctk.CTkButton(root, text="Download and Convert to MP3", command=lambda: threading.Thread(target=download_and_convert, args=(url_entry,)).start())
    download_and_convert_button.grid(row=1, column=0, padx=(0, 5), pady=(0, 5), sticky="e")

    root.grid_rowconfigure(0, weight=0)
    root.grid_rowconfigure(1, weight=0)
    root.grid_columnconfigure(0, weight=1)

    root.mainloop()

if __name__ == "__main__":
    main()
