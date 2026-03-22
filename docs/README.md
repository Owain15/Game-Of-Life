# Conway's Game of Life

## What is Conway's Game of Life?

Conway's Game of Life is a cellular automaton devised by mathematician John Conway in 1970. It is a zero-player game — its evolution is determined by its initial state, with no further input. Despite simple rules, it produces remarkably complex and unpredictable behavior, making it a classic example of emergent complexity.

## Rules

The game is played on a 2D grid of cells. Each cell is either **alive** or **dead**. Every generation, cells update simultaneously based on their 8 neighbors:

1. **Underpopulation** — A live cell with fewer than 2 live neighbors dies.
2. **Survival** — A live cell with 2 or 3 live neighbors survives.
3. **Overpopulation** — A live cell with more than 3 live neighbors dies.
4. **Reproduction** — A dead cell with exactly 3 live neighbors becomes alive.

## How to Run

```bash
pip install -r requirements.txt
python app.py
```

Then open `http://localhost:5000` in your browser.

## How to Use

- **Click** on the grid to toggle cells alive/dead.
- **Start/Stop** — begin or pause automatic generation stepping.
- **Step** — advance one generation manually.
- **Reset** — clear the grid.
- **Random** — fill the grid with random cells.
- **Speed control** — adjust how fast auto-step runs.
