from flask import render_template, request
import os
import yt_dlp as youtube_dl 

songs = []

def dlsong(url, name):
    os.makedirs('./songs', exist_ok=True)

    # Remove a extensão no caso do usuario adicionar
    base_filename = os.path.splitext(name)[0]

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'static/songs/{base_filename}.%(ext)s',
        'ffmpeg_location': 'C:/ProgramData/chocolatey/lib/ffmpeg/tools/ffmpeg/bin',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return f'static/songs/{base_filename}.mp3'

def init_app(app):
    # Rota principal do site
    @app.route("/")
    # View function - Explicita o que vai ser renderizado na rota
    def home():
        return render_template("index.html", songs=songs)
    
    @app.route("/addsong", methods=["POST"])
    def addsong():
        if request.method == "POST":
            if request.form.get("url") and request.form.get("name"):
                out = dlsong(request.form.get("url"), request.form.get("name"))
                songs.append({"name": request.form.get("name"), "uri": out})