from flask import Flask, render_template, request, send_file
from moviepy.editor import VideoFileClip
from pytube import YouTube
import os
from tempfile import NamedTemporaryFile

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_link = request.form['video_link']

        # Download YouTube video
        youtube_video = YouTube(video_link)
        video_stream = youtube_video.streams.filter(file_extension="mp4").first()
        video_stream.download(filename="temp_video.mp4")

        # Convert the downloaded video to audio
        video_clip = VideoFileClip("temp_video.mp4")
        temp_audio = NamedTemporaryFile(suffix=".mp3", delete=False)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(temp_audio.name)

        # Close resources
        audio_clip.close()
        video_clip.close()

        # Provide a download link for the user
        return render_template('index.html', download_link=temp_audio.name)

    return render_template('index.html', download_link=None)

@app.route('/download/<path:filename>')
def download(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
