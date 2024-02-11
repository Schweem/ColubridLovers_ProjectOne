document.addEventListener('DOMContentLoaded', function() {
    let interval;
    let isRunning = false;
    const display = document.querySelector('#timer-display');
    const durations = {
        pomodoro: 25 * 60,
        shortBreak: 5 * 60,
        longBreak: 10 * 60
    };
    let currentDuration = durations.pomodoro; // Default to Pomodoro

    function startTimer(duration) {
        if (isRunning) return; // Prevent multiple intervals
        let timer = duration, minutes, seconds;
        isRunning = true;
        interval = setInterval(function () {
            minutes = parseInt(timer / 60, 10);
            seconds = parseInt(timer % 60, 10);

            minutes = minutes < 10 ? "0" + minutes : minutes;
            seconds = seconds < 10 ? "0" + seconds : seconds;

            display.textContent = minutes + ":" + seconds;

            if (--timer < 0) {
                clearInterval(interval);
                alert("Time's up!");
                isRunning = false;
            }
        }, 1000);
    }

    document.querySelector('#start-button').addEventListener('click', function () {
        startTimer(currentDuration);
    });

    document.querySelector('#stop-button').addEventListener('click', function () {
        clearInterval(interval);
        isRunning = false;
    });

    document.querySelector('#reset-button').addEventListener('click', function () {
        clearInterval(interval);
        display.textContent = "25:00";
        isRunning = false;
        currentDuration = durations.pomodoro; // Reset to default Pomodoro time
    });

    document.querySelector('#pomodoro').addEventListener('click', function () {
        currentDuration = durations.pomodoro;
        display.textContent = "25:00";
    });

    document.querySelector('#short-break').addEventListener('click', function () {
        currentDuration = durations.shortBreak;
        display.textContent = "05:00";
    });

    document.querySelector('#long-break').addEventListener('click', function () {
        currentDuration = durations.longBreak;
        display.textContent = "10:00";
    });
});
