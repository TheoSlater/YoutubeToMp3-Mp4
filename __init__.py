import tkinter as tk
from tkinter import StringVar
from pytube import YouTube
from moviepy.editor import VideoFileClip
import threading
import os
import customtkinter

mp3_conversion_triggered = False  # Flag to track MP3 conversion
customtkinter.set_appearance_mode("dark")

def download_mp4(url_entry):
    url = url_entry.get()
    output_path = '.'  # Set your desired output path

    try:
        yt = YouTube(url)
        mp4_stream = yt.streams.filter(file_extension='mp4').first()

        if mp4_stream:
            mp4_file_path = mp4_stream.download(output_path)
        else:
            print("Mp4 stream not found")

    except Exception as e:
        print(f'Error Downloading mp4: {e}')
        

def download_and_convert(url_entry):
    url = url_entry.get()
    output_path = '.'  # Set your desired output path

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


        # Delete the original MP4 file
        os.remove(video_file_path)
        print('succesfully downloaded.')


    except Exception as e:
        print(f'Error converting to MP3: {e}')

def main():

    root = customtkinter.CTk()
    root.title("YouTube Downloader")

    # Set window size and position
    window_width = 345
    window_height = 90
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = int((screen_width - window_width) / 2)
    y_coordinate = int((screen_height - window_height) / 2)
    root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    # Entry for URL
    url_var = StringVar()
    url_entry = customtkinter.CTkEntry(root, textvariable=url_var, width=400, bg_color="black", fg_color="white")  
    url_entry.insert(0, "Paste YouTube URL here")  
    url_entry.bind("<FocusIn>", lambda event: url_entry.delete("0", "end") if url_entry.get() == "Paste YouTube URL here" else None)
    url_entry.grid(row=0, column=0, padx=10, pady=10, sticky="we")  # Use sticky="we" to expand horizontally

    # Buttons
    download_mp4_button = customtkinter.CTkButton(root, text="Download MP4", command=lambda: download_mp4(url_entry))
    download_mp4_button.grid(row=1, column=0, padx=5, pady=(0, 5), sticky="w")

    download_and_convert_button = customtkinter.CTkButton(root, text="Download and Convert to MP3", command=lambda: download_and_convert(url_entry))
    download_and_convert_button.grid(row=1, column=0, padx=(0, 5), pady=(0, 5), sticky="e")

    # Configure rows and columns to expand
    root.grid_rowconfigure(0, weight=0)  # URL entry row
    root.grid_rowconfigure(1, weight=0)  # Button row
    root.grid_columnconfigure(0, weight=1)  # Allow widgets to expand horizontally

    root.mainloop()

if __name__ == "__main__":
    main()
