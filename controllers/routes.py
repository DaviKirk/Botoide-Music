#BAIXAR DEPENDENCIAS PELO POWER SHELL EXECUTADO COMO ADM:

#Set-ExecutionPolicy AllSigned

#Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

#choco install ffmpeg

from flask import redirect, render_template, request, url_for
import os
import yt_dlp as youtube_dl 
import json

songs = []
authors = []
genres = []

def save_songs_to_json():
    with open('static/songs.json', 'w', encoding='utf-8') as f:
        json.dump(songs, f, ensure_ascii=False, indent=4)

def dlsong(url, name):
    os.makedirs('./songs', exist_ok=True)

    # Remove a extensão no caso do usuario adicionar
    base_filename = os.path.splitext(name)[0]

    # First extract info to get thumbnail URL
    with youtube_dl.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(url, download=False)
        url_thumb = info.get('thumbnail', '')

    # Then download and process the audio
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
    
    return f'static/songs/{base_filename}.mp3', url_thumb

def init_app(app):
    # Rota principal do site
    @app.route("/")
    # View function - Explicita o que vai ser renderizado na rota
    def home():
        return render_template("index.html", songs=songs)
    
    @app.route("/getauthors", methods=["GET"])
    def getauthors():
        return render_template("artists.html", authors=authors)
    
    @app.route("/getgenres", methods=["GET"])
    def getgenres():
        return render_template("genres.html", genres=genres)
    
    @app.route("/addsong", methods=["POST"])
    def addsong():
        if request.method == "POST":
            if request.form.get("url") and request.form.get("name"):
                out, url_thumb = dlsong(request.form.get("url"), request.form.get("name"))

                songs.append({"name": request.form.get("name"), "author": request.form.get("author"), "uri": out, "url_thumb": url_thumb})
                save_songs_to_json()
        return home()
            
    @app.route("/addauthor", methods=["POST"])
    def addauthor():
        if request.method == "POST":
            if request.form.get("name") and request.form.get("genre") and request.form.get("age"):
                authors.append({"name": request.form.get("name"), "genre": request.form.get("genre"), "age": request.form.get("age")})
                return getauthors()
            
    @app.route("/addgenre", methods=["POST"])
    def addgenre():
        if request.method == "POST":
            if request.form.get("name"):
                genres.append(request.form.get("name"))
                return getgenres()
    @app.route("/formPage")
    def formPage():
         return render_template("formPage.html")
        
            