let car = document.getElementById('car');
let gameContainer = document.getElementById('game-container');
let speed = 10;

document.addEventListener('keydown', (event) => {
    let carPosition = car.getBoundingClientRect();
    let containerPosition = gameContainer.getBoundingClientRect();
    
    switch(event.key) {
        case 'ArrowUp':
            if (carPosition.top > containerPosition.top) {
                car.style.top = carPosition.top - containerPosition.top - speed + 'px';
            }
            break;
        case 'ArrowDown':
            if (carPosition.bottom < containerPosition.bottom) {
                car.style.top = carPosition.top - containerPosition.top + speed + 'px';
            }
            break;
        case 'ArrowLeft':
            if (carPosition.left > containerPosition.left) {
                car.style.left = carPosition.left - containerPosition.left - speed + 'px';
            }
            break;
        case 'ArrowRight':
            if (carPosition.right < containerPosition.right) {
                car.style.left = carPosition.left - containerPosition.left + speed + 'px';
            }
            break;
    }
});
