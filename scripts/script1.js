function activateIRSensor() {
    const car = document.getElementById("car");
    const alarm = document.getElementById("alarm");
    const sadFace = document.getElementById("sad-face");

    // Car movement
    car.style.transform = "translateX(-100px)";
    // Alarm pulse
    alarm.style.transform = "scale(1.2)";
    setTimeout(() => alarm.style.transform = "scale(1)", 500);

    // Show Sad Face
    sadFace.style.opacity = "1";

    // Play sound
    const beepSound = document.getElementById("beepSound");
    beepSound.play();

    alert("Obstacle detected! The car has stopped, the alarm is beeping, and a sad face is displayed.");
}

function resetSystem() {
    const car = document.getElementById("car");
    const alarm = document.getElementById("alarm");
    const sadFace = document.getElementById("sad-face");

    // Reset visuals
    car.style.transform = "translateX(0px)";
    alarm.style.transform = "scale(1)";
    sadFace.style.opacity = "0";

    // Stop beep
    const beepSound = document.getElementById("beepSound");
    beepSound.pause();
    beepSound.currentTime = 0;

    alert("System reset! The car is back to normal.");
}
