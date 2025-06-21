const dino = document.getElementById("dino");
const cactus = document.getElementById("cactus");
const coin = document.getElementById("coin");
const scoreDisplay = document.getElementById("score");
let score = 0;
let gameActive = true;
let isAlive;

// Функция прыжка
function jump() {
  if (dino.classList != "jump" && gameActive) {
    dino.classList.add("jump");
    setTimeout(function () {
      dino.classList.remove("jump");
    }, 300);
  }
}

// Функция перезапуска игры
function resetGame() {
  gameActive = true;
  score = 0;
  scoreDisplay.textContent = `Счёт: ${score}`;
  cactus.style.animation = "block 2s infinite linear";
  cactus.style.animationPlayState = "running";
  coin.style.display = "none";
  coin.style.animation = "none";
  clearInterval(isAlive);
  startGameLoop();
  spawnCoin();
}

// Запуск игрового цикла
function startGameLoop() {
  isAlive = setInterval(function () {
    if (!gameActive) return;

    let dinoTop = parseInt(window.getComputedStyle(dino).getPropertyValue("top"));
    let cactusLeft = parseInt(window.getComputedStyle(cactus).getPropertyValue("left"));
    let coinLeft = parseInt(window.getComputedStyle(coin).getPropertyValue("left"));

    // Столкновение с кактусом
    if (cactusLeft < 50 && cactusLeft > 0 && dinoTop >= 140) {
      gameActive = false;
      cactus.style.animationPlayState = "paused";
      coin.style.animationPlayState = "paused";
      alert("Потрачено! Нажмите пробел для перезапуска.");
    }

    // Сбор монеты
    if (coin.style.display === "block" && coinLeft < 50 && coinLeft > 0 && dinoTop <= 140) {
      score += 1;
      scoreDisplay.textContent = `Счёт: ${score}`;
      coin.style.display = "none";
      if (score >= 100) {
        gameActive = false;
        cactus.style.animationPlayState = "paused";
        coin.style.animationPlayState = "paused";
        alert("Победа! Вы набрали 100 монет! Нажмите пробел для перезапуска.");
      }
    }
  }, 10);
}

// Спавн монетного дрона каждую секунду
function spawnCoin() {
  if (gameActive) {
    coin.style.display = "block";
    coin.style.animation = "none";
    coin.offsetHeight; // Триггер для рестарта анимации
    coin.style.animation = "coinMove 3s linear";
    setTimeout(spawnCoin, 10000); // Изменено с 30000 на 1000 для спавна каждую секунду
  }
}

// Обработчик нажатия клавиши
document.addEventListener("keydown", function (event) {
  if (event.key === " " && gameActive) {
    jump();
  } else if (event.key === " " && !gameActive) {
    resetGame();
  }
});

// Запускаем игру
startGameLoop();
setTimeout(spawnCoin, 5000); // Первый спавн через 1 секунду
