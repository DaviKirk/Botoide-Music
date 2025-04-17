
const player = document.getElementById('player');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const playBtn = document.getElementById('playBtn');
const spanTotalTime = document.getElementById('duration');
const spanCurrentTime = document.getElementById('currentTime');
const progressBar = document.getElementById('progress');

let songs = [];
let currentSongsIndex = 0;

function loadJson() {
    fetch('/static/songs.json')
        .then(response => response.json())
        .then(dados => {
            songs = dados;
            loadSong(currentSongsIndex);
        })
        .catch(function(error) {
            console.error('Erro ao carregar o JSON:', error);
        });
};

function loadSong(index){
    const song = songs[index];
    player.src = song.uri;
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

nextBtn.addEventListener('click', function(){
    currentSongsIndex = (currentSongsIndex + 1) % songs.length;
    loadSong(currentSongsIndex);
    player.play();
    playBtn.innerHTML = '<i class="fa-solid fa-pause"></i>';
});
prevBtn.addEventListener('click', function(){
    currentSongsIndex = (currentSongsIndex - 1 + songs.length) % songs.length;
    loadSong(currentSongsIndex);
    player.play();
    playBtn.innerHTML = '<i class="fa-solid fa-pause"></i>';
});

document.addEventListener('DOMContentLoaded', loadJson);