

const startStopBtn = document.querySelector('#startStopBtn');
const resetBtn = document.querySelector('#resetBtn');

let seconds = 0;
let minutes = 0;
let hours = 0;


let leadingSeconds = 0;
let leadingMinutes = 0;
let leadingHours = 0;


let timeInterval = null;
let timeStatus = "Stopped"



function stopWatch() {
    seconds ++;

    if (seconds / 60 === 1) {
        seconds = 0;
        minutes++;

        if (minutes / 60 === 1) {
            minutes = 0;
            hours++;
        }
    }

    if (seconds < 10)
        leadingSeconds = "0" + seconds.toString();
    else
        leadingSeconds = seconds

    if (minutes < 10)
        leadingMinutes = "0" + minutes.toString();
    else
        leadingMinutes = minutes

    if (hours < 10)
        leadingHours = "0" + hours.toString();
    else
        leadingHours = hours

    let displayTimer = document.getElementById('timer').innerText = leadingHours + ":" + leadingMinutes + ":" + leadingSeconds

}

startStopBtn.addEventListener('click', function() {

    if (timeStatus === "Stopped") {
        timeInterval = window.setInterval(stopWatch, 1000);
        document.getElementById('startStopBtn').innerHTML = `<i class="fa-solid fa-play" id="play"><img class="img-btn" src="Image/pause-btn.svg" alt="play"></i>`;
        timeStatus = 'Started';
    } else {
        window.clearInterval(timeInterval);
        document.getElementById('startStopBtn').innerHTML = `<i class="fa-solid fa-play" id="play"><img class="img-btn" src="Image/play-btn.svg" alt="play"></i>`;
        timeStatus = 'Stopped';
    }

});

resetBtn.addEventListener('click', function() {

    document.getElementById('timer').innerText = '00:00:00'
    window.clearInterval(timeInterval);
    document.getElementById('startStopBtn').innerHTML = `<i class="fa-solid fa-play" id="play"><img class="img-btn" src="Image/play-btn.svg" alt="play"></i>`;
    timeStatus = 'Stopped';
    seconds = 0;
    minutes = 0;
    hours = 0;

});