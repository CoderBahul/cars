let car = document.getElementById('car');
let gameContainer = document.getElementById('game-container');
let speed = 10;

function moveCar(direction) {
    let carPosition = car.getBoundingClientRect();
    let containerPosition = gameContainer.getBoundingClientRect();

    switch(direction) {
        case 'up':
            if (carPosition.top > containerPosition.top) {
                car.style.top = carPosition.top - containerPosition.top - speed + 'px';
            }
            break;
        case 'down':
            if (carPosition.bottom < containerPosition.bottom) {
                car.style.top = carPosition.top - containerPosition.top + speed + 'px';
            }
            break;
        case 'left':
            if (carPosition.left > containerPosition.left) {
                car.style.left = carPosition.left - containerPosition.left - speed + 'px';
            }
            break;
        case 'right':
            if (carPosition.right < containerPosition.right) {
                car.style.left = carPosition.left - containerPosition.left + speed + 'px';
            }
            break;
    }
}

// Event listeners for mobile control buttons
document.getElementById('up').addEventListener('click', () => moveCar('up'));
document.getElementById('down').addEventListener('click', () => moveCar('down'));
document.getElementById('left').addEventListener('click', () => moveCar('left'));
document.getElementById('right').addEventListener('click', () => moveCar('right'));
