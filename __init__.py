from pytube import YouTube
from moviepy.editor import VideoFileClip
import os

def download_and_convert(url, output_path='.'):
    try:
        yt = YouTube(url)

        # Always download the video as mp4
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
        # Load the video and extract audio
        video = VideoFileClip(video_file_path)
        audio = video.audio

        # Write the audio to an mp3 file
        audio.write_audiofile(video_file_path.replace('.mp4', '_converted.mp3'), codec='mp3', fps=44100)

        video.close()

        print('Conversion to MP3 completed!')

    except Exception as e:
        print(f'Error converting to MP3: {e}')

if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")
    download_and_convert(video_url)
