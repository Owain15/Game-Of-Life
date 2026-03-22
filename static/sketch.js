const ROWS = 50;
const COLS = 50;
const CELL_SIZE = 10;

let grid = [];

function setup() {
  let canvas = createCanvas(COLS * CELL_SIZE, ROWS * CELL_SIZE);
  canvas.parent("main");
  noLoop();
  fetchState();
}

function draw() {
  background(0);
  for (let r = 0; r < ROWS; r++) {
    for (let c = 0; c < COLS; c++) {
      if (grid[r] && grid[r][c] === 1) {
        fill(255);
      } else {
        fill(0);
      }
      stroke(40);
      rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE);
    }
  }
}

function fetchState() {
  fetch("/api/state")
    .then((res) => res.json())
    .then((data) => {
      grid = data;
      redraw();
    });
}

function mousePressed() {
  let col = Math.floor(mouseX / CELL_SIZE);
  let row = Math.floor(mouseY / CELL_SIZE);
  if (row >= 0 && row < ROWS && col >= 0 && col < COLS) {
    fetch("/api/toggle", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ row: row, col: col }),
    })
      .then((res) => res.json())
      .then((data) => {
        grid = data;
        redraw();
      });
  }
}

// Auto-step
let running = false;
let intervalId = null;

function doStep() {
  fetch("/api/step", { method: "POST" })
    .then((res) => res.json())
    .then((data) => {
      grid = data;
      redraw();
    });
}

document.getElementById("startStop").addEventListener("click", function () {
  running = !running;
  this.textContent = running ? "Stop" : "Start";
  if (running) {
    let speed = document.getElementById("speed").value;
    intervalId = setInterval(doStep, 1000 / speed);
  } else {
    clearInterval(intervalId);
  }
});

document.getElementById("stepBtn").addEventListener("click", doStep);

document.getElementById("resetBtn").addEventListener("click", function () {
  fetch("/api/reset", { method: "POST" })
    .then((res) => res.json())
    .then((data) => {
      grid = data;
      redraw();
    });
});

document.getElementById("randomBtn").addEventListener("click", function () {
  fetch("/api/random", { method: "POST" })
    .then((res) => res.json())
    .then((data) => {
      grid = data;
      redraw();
    });
});

document.getElementById("speed").addEventListener("input", function () {
  if (running) {
    clearInterval(intervalId);
    intervalId = setInterval(doStep, 1000 / this.value);
  }
});
