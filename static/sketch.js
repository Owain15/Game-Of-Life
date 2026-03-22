const CELL_SIZE = 10;

let grid = [];
let canvas, ctx;
let offCanvas = document.createElement("canvas");
let offCtx = offCanvas.getContext("2d");

function gridRows() { return grid.length || 50; }
function gridCols() { return (grid[0] && grid[0].length) || 50; }

function drawGrid() {
  let rows = gridRows();
  let cols = gridCols();
  for (let r = 0; r < rows; r++) {
    let alive = grid[r];
    for (let c = 0; c < cols; c++) {
      if (alive && alive[c] === 1) {
        offCtx.fillStyle = "#00c864";
      } else {
        offCtx.fillStyle = "#141414";
      }
      offCtx.fillRect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE);
    }
  }
  ctx.drawImage(offCanvas, 0, 0);
}

function updateGrid(data) {
  grid = data;
  canvas.width = gridCols() * CELL_SIZE;
  canvas.height = gridRows() * CELL_SIZE;
  offCanvas.width = canvas.width;
  offCanvas.height = canvas.height;
  drawGrid();
}

function fetchState() {
  fetch("/api/state")
    .then((res) => res.json())
    .then(updateGrid);
}

function getInputs() {
  return {
    rows: parseInt(document.getElementById("rows").value) || 50,
    cols: parseInt(document.getElementById("cols").value) || 50,
    density: parseInt(document.getElementById("density").value) / 100,
  };
}

// Auto-step
let running = false;
let stepping = false;
let timerId = null;

function doStep() {
  if (stepping) return;
  stepping = true;
  fetch("/api/step", { method: "POST" })
    .then((res) => res.json())
    .then((data) => {
      grid = data;
      drawGrid();
    })
    .finally(() => {
      stepping = false;
      if (running) scheduleStep();
    });
}

function scheduleStep() {
  let speed = document.getElementById("speed").value;
  timerId = setTimeout(doStep, 1000 / speed);
}

// Init
canvas = document.getElementById("gameCanvas");
ctx = canvas.getContext("2d");
fetchState();

// Click to toggle
canvas.addEventListener("click", function (e) {
  let rect = canvas.getBoundingClientRect();
  let col = Math.floor((e.clientX - rect.left) / CELL_SIZE);
  let row = Math.floor((e.clientY - rect.top) / CELL_SIZE);
  if (row >= 0 && row < gridRows() && col >= 0 && col < gridCols()) {
    fetch("/api/toggle", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ row: row, col: col }),
    })
      .then((res) => res.json())
      .then((data) => {
        grid = data;
        drawGrid();
      });
  }
});

document.getElementById("startStop").addEventListener("click", function () {
  running = !running;
  this.textContent = running ? "Stop" : "Start";
  if (running) {
    scheduleStep();
  } else {
    clearTimeout(timerId);
  }
});

document.getElementById("stepBtn").addEventListener("click", doStep);

document.getElementById("resetBtn").addEventListener("click", function () {
  let inp = getInputs();
  fetch("/api/reset", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ rows: inp.rows, cols: inp.cols }),
  })
    .then((res) => res.json())
    .then(updateGrid);
});

document.getElementById("randomBtn").addEventListener("click", function () {
  let inp = getInputs();
  fetch("/api/random", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ rows: inp.rows, cols: inp.cols, density: inp.density }),
  })
    .then((res) => res.json())
    .then(updateGrid);
});

document.getElementById("speed").addEventListener("input", function () {
  if (running) {
    clearTimeout(timerId);
    scheduleStep();
  }
});

document.getElementById("density").addEventListener("input", function () {
  document.getElementById("densityVal").textContent = this.value + "%";
});
