
const player = document.getElementById('player');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const playBtn = document.getElementById('playBtn');
const currentSongName = document.getElementById('currentSongName');
const currentThumb = document.getElementById('currentThumb');
const spanTotalTime = document.getElementById('duration');
const spanCurrentTime = document.getElementById('currentTime');
const progressBar = document.querySelector('.progress');
const progressContainer = document.getElementById('progressBar');

player.addEventListener('timeupdate', function () {

    const duration = player.duration
    const currentTime = player.currentTime

    if (!isNaN(duration) && duration > 0) {

        const percent = (currentTime / duration) * 100;
        progressBar.style.width = percent + '%';

        spanTotalTime.textContent = formatTime(duration)
        spanCurrentTime.textContent = formatTime(currentTime)

    }
});

progressContainer.addEventListener('click', function(event){

    const barWidth = progressContainer.clientWidth;
    const clickX = event.offsetX;
    const clickPercent = clickX / barWidth;
    const newTime = clickPercent * player.duration;

    player.currentTime = newTime;

});

function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${minutes}:${secs < 10 ? '0' : ''}${secs}`;
}

let songs = [];
let currentSongsIndex = 0;

function loadJson() {
    fetch('/static/songs.json')
        .then(response => response.json())
        .then(dados => {
            songs = dados;
            loadSong(currentSongsIndex);
        })
        .catch(function (error) {
            console.error('Erro ao carregar o JSON:', error);
        });
};

function loadSong(index) {
    const song = songs[index];
    player.src = song.uri;
    currentSongName.textContent = song.name;
    currentThumb.src = song.url_thumb;
    currentSongAuthor.textContent = song.author;
}

playBtn.addEventListener('click', () => {
    if (player.paused) {
        player.play();
        playBtn.innerHTML = '<i class="fa-solid fa-pause"></i>';
    } else {
        player.pause();
        playBtn.innerHTML = '<i class="fa-solid fa-play"></i>';
    }
});

nextBtn.addEventListener('click', function () {
    currentSongsIndex = (currentSongsIndex + 1) % songs.length;
    loadSong(currentSongsIndex);
    player.play();
    playBtn.innerHTML = '<i class="fa-solid fa-pause"></i>';
});
prevBtn.addEventListener('click', function () {
    currentSongsIndex = (currentSongsIndex - 1 + songs.length) % songs.length;
    loadSong(currentSongsIndex);
    player.play();
    playBtn.innerHTML = '<i class="fa-solid fa-pause"></i>';
});
player.addEventListener('ended', function () {
    currentSongsIndex = (currentSongsIndex + 1) % songs.length;
    loadSong(currentSongsIndex);
    player.play();
    playBtn.innerHTML = '<i class="fa-solid fa-pause"></i>';
});

document.addEventListener('DOMContentLoaded', loadJson);