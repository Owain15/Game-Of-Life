import random
from flask import Flask, jsonify, request, render_template

ROWS = 50
COLS = 50


def create_grid(rows=ROWS, cols=COLS):
    return [[0 for _ in range(cols)] for _ in range(rows)]


def randomize_grid(rows=ROWS, cols=COLS):
    return [[random.randint(0, 1) for _ in range(cols)] for _ in range(rows)]


def count_neighbors(grid, row, col):
    rows = len(grid)
    cols = len(grid[0])
    count = 0
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            r = (row + dr) % rows
            c = (col + dc) % cols
            count += grid[r][c]
    return count


def step(grid):
    rows = len(grid)
    cols = len(grid[0])
    new_grid = create_grid(rows, cols)
    for r in range(rows):
        for c in range(cols):
            neighbors = count_neighbors(grid, r, c)
            if grid[r][c] == 1:
                new_grid[r][c] = 1 if neighbors in (2, 3) else 0
            else:
                new_grid[r][c] = 1 if neighbors == 3 else 0
    return new_grid


app = Flask(__name__)
grid = create_grid()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/state")
def api_state():
    return jsonify(grid)


@app.route("/api/step", methods=["POST"])
def api_step():
    global grid
    grid = step(grid)
    return jsonify(grid)


@app.route("/api/toggle", methods=["POST"])
def api_toggle():
    data = request.get_json()
    row = data["row"]
    col = data["col"]
    grid[row][col] = 1 - grid[row][col]
    return jsonify(grid)


@app.route("/api/reset", methods=["POST"])
def api_reset():
    global grid
    grid = create_grid()
    return jsonify(grid)


@app.route("/api/random", methods=["POST"])
def api_random():
    global grid
    grid = randomize_grid()
    return jsonify(grid)


if __name__ == "__main__":
    app.run(debug=True)
