import tkinter as tk
from tkinter import Entry, Label, Button, StringVar
from pytube import YouTube
from moviepy.editor import VideoFileClip
import os
from PIL import Image, ImageTk  # PIL is used to convert the icon to a Tkinter-compatible format

def download_and_convert():
    url = url_entry.get()

    try:
        yt = YouTube(url)

        mp4_stream = yt.streams.filter(file_extension='mp4').first()
        if mp4_stream:
            print(f'Downloading MP4: {yt.title}')
            mp4_file_path = mp4_stream.download(output_path)
            print('MP4 Download completed!')

            # Convert the mp4 to mp3
            convert_to_mp3(mp4_file_path)
            print('MP3 Conversion completed!')

    except Exception as e:
        print(f'Error: {e}')

def convert_to_mp3(video_file_path):
    try:
        video = VideoFileClip(video_file_path)
        audio = video.audio
        audio.write_audiofile(video_file_path.replace('.mp4', '_converted.mp3'), codec='mp3', fps=44100)
        video.close()
        print('Conversion to MP3 completed!')

    except Exception as e:
        print(f'Error converting to MP3: {e}')

output_path = '.'  # Set your desired output path

# GUI setup
root = tk.Tk()
root.title("YouTube Downloader")

# Set the window icon using a bitmap file
icon_path = os.path.abspath("youtube.bmp")
icon_image = Image.open(icon_path)
icon_bitmap = ImageTk.PhotoImage(icon_image)
root.tk.call('wm', 'iconphoto', root._w, icon_bitmap)

url_label = Label(root, text="Enter YouTube video URL:")
url_label.pack()

url_var = StringVar()
url_entry = Entry(root, textvariable=url_var, width=40)
url_entry.pack()

download_button = Button(root, text="Download and Convert", command=download_and_convert)
download_button.pack()

root.mainloop()
