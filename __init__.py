import tkinter as tk
from tkinter import Entry, Label, Button, StringVar, Text, Scrollbar
from pytube import YouTube
from moviepy.editor import VideoFileClip
import threading
import os

def download_mp4():
    global url_entry, console_text
    url = url_entry.get()
    output_path = '.'  # Set your desired output path

    try:
        yt = YouTube(url)
        mp4_stream = yt.streams.filter(file_extension='mp4').first()

        if mp4_stream:
            console_text.insert(tk.END, f'Downloading MP4: {yt.title}\n')
            mp4_file_path = mp4_stream.download(output_path)
            console_text.insert(tk.END, 'MP4 Download completed!\n')
        else:
            console_text.insert(tk.END, "MP4 stream not found.\n")

    except Exception as e:
        console_text.insert(tk.END, f'Error: {e}\n')

def download_and_convert():
    global url_entry, console_text
    url = url_entry.get()
    output_path = '.'  # Set your desired output path

    try:
        yt = YouTube(url)
        mp4_stream = yt.streams.filter(file_extension='mp4').first()

        if mp4_stream:
            console_text.insert(tk.END, f'Downloading MP4: {yt.title}\n')
            mp4_file_path = mp4_stream.download(output_path)
            console_text.insert(tk.END, 'MP4 Download completed!\n')
            threading.Thread(target=convert_to_mp3, args=(mp4_file_path,)).start()
        else:
            console_text.insert(tk.END, "MP4 stream not found.\n")

    except Exception as e:
        console_text.insert(tk.END, f'Error: {e}\n')

def convert_to_mp3(video_file_path):
    global console_text
    try:
        video = VideoFileClip(video_file_path)
        audio = video.audio
        audio.write_audiofile(video_file_path.replace('.mp4', '_converted.mp3'), codec='mp3', fps=44100)
        video.close()
        console_text.insert(tk.END, 'Conversion to MP3 completed!\n')

        # Delete the original MP4 file
        os.remove(video_file_path)
        console_text.insert(tk.END, 'Original MP4 file deleted.\n')

    except Exception as e:
        console_text.insert(tk.END, f'Error converting to MP3: {e}\n')

def main():
    global url_entry, console_text
    root = tk.Tk()
    root.title("YouTube Downloader")

    # Center the window
    root.geometry("800x300+400+200")

    # Set the weight of columns and rows to allow them to resize
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=0)
    root.rowconfigure(2, weight=1)
    root.columnconfigure(0, weight=0)
    root.columnconfigure(1, weight=1)
    root.columnconfigure(2, weight=1)

    url_label = Label(root, text="Enter YouTube video URL:")
    url_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

    url_var = StringVar()
    url_entry = Entry(root, textvariable=url_var, width=40)
    url_entry.insert(0, "Paste YouTube URL here")  # Set placeholder text
    url_entry.bind("<FocusIn>", lambda event: url_entry.delete("0", "end") if url_entry.get() == "Paste YouTube URL here" else None)
    url_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    button_frame = tk.Frame(root)
    button_frame.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    download_mp4_button = Button(button_frame, text="Download MP4", command=download_mp4)
    download_mp4_button.grid(row=0, column=0, padx=5)

    download_and_convert_button = Button(button_frame, text="Download and Convert to MP3", command=download_and_convert)
    download_and_convert_button.grid(row=0, column=1, padx=5)

    # Console box
    console_frame = tk.Frame(root, bg="black")
    console_frame.grid(row=0, column=2, rowspan=2, padx=10, pady=10, sticky="nsew")

    console_text = Text(console_frame, bg="black", fg="white", wrap="word", height=15, width=30)
    console_text.pack(side="left", fill="both", expand=True)

    # Add a scrollbar to the console
    scrollbar = Scrollbar(console_frame, command=console_text.yview)
    scrollbar.pack(side="right", fill="y")
    console_text.config(yscrollcommand=scrollbar.set)

    root.mainloop()

if __name__ == "__main__":
    main()
