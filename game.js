const canvas = document.getElementById("gameCanvas");
const screen = canvas.getContext("2d");
const keyState = {};
let DIFFICULTY = 1;
let SCORE = 0;
let SPEED = 10;
let gameover = false;


// Start screen class
class StartScreen {
    constructor(canvas) {
        this.font = "60px Arial";
        this.titleText = "SPACE FIGHTER";
        this.startText = "Press ENTER to start";
        this.titleX = canvas.width / 2;
        this.titleY = canvas.height / 2 - 50;
        this.startX = canvas.width / 2;
        this.startY = canvas.height / 2 + 50;
    }

    draw(screen) {
        screen.fillStyle = "#00FFFF";
        screen.font = this.font;
        screen.textAlign = "center";
        screen.fillText(this.titleText, this.titleX, this.titleY);
        screen.fillStyle = "#FFFFFF";
        screen.fillText(this.startText, this.startX, this.startY);
    }
}

// Game over screen class
class GameOverScreen {
    constructor(canvas) {
        this.font = "60px Arial";
        this.gameOverText = "Game Over";
        this.restartText = "Press ENTER to exit";
        this.gameOverX = canvas.width / 2;
        this.gameOverY = canvas.height / 2 - 50;
        this.restartX = canvas.width / 2;
        this.restartY = canvas.height / 2 + 50;
    }

    draw(screen) {
        screen.fillStyle = "#FF00FF";
        screen.font = this.font;
        screen.textAlign = "center";
        screen.fillText(this.gameOverText, this.gameOverX, this.gameOverY);
        screen.fillStyle = "#FFFFFF";
        screen.fillText(this.restartText, this.restartX, this.restartY);
    }
}

// Velocity class
class Velocity {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }
}

// Position class
class Position {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }
}

// Bullet class
class Bullet {
    constructor(position, velocity, canvas) {
        this.position = position;
        this.velocity = velocity;
        this.height = canvas.height;
        this.width = 2;
    }

    draw(screen) {
        screen.fillStyle = "#00FFFF";
        screen.fillRect(this.position.x, this.position.y - this.height, this.width, this.height);
    }

    move() {
        this.position.y += this.velocity.y;
    }
}

// Ship class
class Ship {
    constructor(position, velocity, canvas) {
        this.position = position;
        this.velocity = velocity;
        this.width = 40;
        this.height = 60;
        this.bullet = new Bullet(new Position((this.position.x + this.width / 2), this.position.y), new Velocity(20, 20), canvas);
        this.image = new Image();
        this.image.src = "/home/zoso/Desktop/invader/assets/ship.png"; // Update the path to your ship image
    }

    draw(screen) {
        screen.drawImage(this.image, this.position.x, this.position.y);
    }

    move(canvas) {
        const SPEED = 10;
        this.velocity.x = 0;
        this.velocity.y = 0;

        if (keyState["ArrowUp"]) {
            this.velocity.y = -SPEED;
        }
        if (keyState["ArrowDown"]) {
            this.velocity.y = SPEED;
        }
        if (keyState["ArrowLeft"]) {
            this.velocity.x = -SPEED;
        }
        if (keyState["ArrowRight"]) {
            this.velocity.x = SPEED;
        }

        if ((this.position.x + this.velocity.x >= 0) && ((this.position.x + this.width + this.velocity.x) <= canvas.width)) {
            this.position.x += this.velocity.x;
        }
        if ((this.position.y + this.velocity.y >= 0) && ((this.position.y + this.height + this.velocity.y) <= canvas.height)) {
            this.position.y += this.velocity.y;
        }
    }

    fireWeapon(screen, canvas) {
        if (keyState["Space"]) {
            this.bullet.position.x = this.position.x + this.width / 2;
            this.bullet.position.y = this.position.y;
            this.bullet.move();
            this.bullet.draw(screen);
            return true;
        }
    }
}

// Alien class
class Alien {
    constructor(canvas) {
        this.width = 40;
        this.height = 40;
        this.position = new Position(randomInt(0 + this.width, canvas.width - this.width), -100);
        this.image = new Image();
        this.image.src = "/home/zoso/Desktop/invader/assets/alien.png"; // Update the path to your alien image
    }

    draw(screen) {
        screen.drawImage(this.image, this.position.x, this.position.y);
    }

    move(speed) {
        this.position.y += speed;
    }
}

// Star class
class Star {
    constructor(canvas) {
        this.position = new Position(randomInt(0, canvas.width), -100);
    }

    draw(screen) {
        screen.fillStyle = "#FFFFFF";
        screen.fillRect(this.position.x, this.position.y, 2, 2);
    }

    move(speed) {
        this.position.y += speed;
    }
}



// Game functions
function detectCollision(ship, alien) {
    return (
        ship.position.x < alien.position.x + alien.width &&
        ship.position.x + ship.width > alien.position.x &&
        ship.position.y < alien.position.y + alien.height &&
        ship.position.y + ship.height > alien.position.y
    );
}

function detectHit(ship, alien) {
    return (
        ship.bullet.position.x < alien.position.x + alien.width &&
        ship.bullet.position.x + ship.bullet.width > alien.position.x &&
        ship.position.y > alien.position.y + alien.height
    );
}

// Helper function to generate a random integer
function randomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1) + min);
}




// Initialize game objects
const startScreen = new StartScreen(canvas);
const gameOverScreen = new GameOverScreen(canvas);
const ship = new Ship(new Position(canvas.width / 2, canvas.height - 100), new Velocity(0, 0), canvas);
let starlist = [];
let enemylist = [];
 // Game loop
 function gameLoop() {
    screen.clearRect(0, 0, canvas.width, canvas.height);

    // Implement your game logic here
    if (starlist.length <= 20) {
        starlist.push(new Star(canvas));
    }
    for (let star of starlist) {
        star.move(20);
        star.draw(screen);
    }

    if (enemylist.length <= DIFFICULTY) {
        enemylist.push(new Alien(canvas));
    }

    for (let enemy of enemylist) {
        enemy.move(SPEED);
        enemy.draw(screen);

        if (detectCollision(ship, enemy)) {
            console.log('there is a collision');
            gameover = true;
        }
    }

    ship.move(canvas);
    firestate = ship.fireWeapon(screen, canvas);

    enemylist = enemylist.filter(enemy => !(detectHit(ship, enemy) && firestate));

    SCORE += (DIFFICULTY + 1) - enemylist.length;

    ship.draw(screen);

    font = "36px Arial";
    screen.fillStyle = "#FFFFFF";
    screen.font = font;
    screen.fillText("Score: " + (SCORE - 1), 10, 10);

    if (gameover) {
        // Game over logic
        gameoverScreen.draw(screen);
    } else {
        requestAnimationFrame(gameLoop);
    }
}

// Event listeners
document.addEventListener("keydown", (event) => {
    keyState[event.key] = true;
});

document.addEventListener("keyup", (event) => {
    keyState[event.key] = false;
});

// Start the game loop
gameLoop();