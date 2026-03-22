import pytest
from app import create_grid, randomize_grid, count_neighbors, step, app


def test_create_grid_all_zeros():
    grid = create_grid(5, 5)
    assert len(grid) == 5
    assert len(grid[0]) == 5
    assert all(cell == 0 for row in grid for cell in row)


def test_create_grid_default_size():
    grid = create_grid()
    assert len(grid) == 50
    assert len(grid[0]) == 50


def test_randomize_grid_size():
    grid = randomize_grid(10, 10)
    assert len(grid) == 10
    assert len(grid[0]) == 10
    assert all(cell in (0, 1) for row in grid for cell in row)


def test_count_neighbors_center():
    grid = create_grid(5, 5)
    grid[0][1] = 1
    grid[1][0] = 1
    grid[1][2] = 1
    assert count_neighbors(grid, 1, 1) == 3


def test_count_neighbors_no_neighbors():
    grid = create_grid(5, 5)
    grid[2][2] = 1
    assert count_neighbors(grid, 2, 2) == 0


def test_count_neighbors_edge_wrapping():
    grid = create_grid(5, 5)
    # Place live cell at bottom-right corner
    grid[4][4] = 1
    # Top-left corner should see it as a neighbor (wrapping)
    assert count_neighbors(grid, 0, 0) == 1


def test_count_neighbors_wrapping_horizontal():
    grid = create_grid(5, 5)
    grid[0][0] = 1
    # Cell at (0, 4) should see (0, 0) as neighbor via wrap
    assert count_neighbors(grid, 0, 4) == 1


def test_step_underpopulation():
    grid = create_grid(5, 5)
    grid[2][2] = 1  # lone cell, 0 neighbors
    new = step(grid)
    assert new[2][2] == 0


def test_step_survival():
    grid = create_grid(5, 5)
    grid[1][1] = 1
    grid[1][2] = 1
    grid[2][1] = 1  # (1,1) has 2 neighbors
    new = step(grid)
    assert new[1][1] == 1


def test_step_overpopulation():
    grid = create_grid(5, 5)
    grid[1][1] = 1
    grid[0][0] = 1
    grid[0][1] = 1
    grid[0][2] = 1
    grid[1][0] = 1  # (1,1) has 4 neighbors
    new = step(grid)
    assert new[1][1] == 0


def test_step_reproduction():
    grid = create_grid(5, 5)
    grid[0][1] = 1
    grid[1][0] = 1
    grid[1][2] = 1  # (0,0) is dead with 2 neighbors, (1,1) dead with 3
    new = step(grid)
    assert new[1][1] == 1


def test_glider_advances():
    """A glider should move one step correctly."""
    grid = create_grid(10, 10)
    # Standard glider pattern:
    #   .X.
    #   ..X
    #   XXX
    grid[0][1] = 1
    grid[1][2] = 1
    grid[2][0] = 1
    grid[2][1] = 1
    grid[2][2] = 1

    new = step(grid)

    # After one step the glider becomes:
    #   ...
    #   X.X
    #   .XX
    #   .X.
    expected_alive = {(1, 0), (1, 2), (2, 1), (2, 2), (3, 1)}
    for r in range(10):
        for c in range(10):
            if (r, c) in expected_alive:
                assert new[r][c] == 1, f"Expected alive at ({r},{c})"
            else:
                assert new[r][c] == 0, f"Expected dead at ({r},{c})"


# --- Flask API Tests ---

import app as app_module


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app_module.grid = create_grid()
    with app.test_client() as client:
        yield client


def test_get_index(client):
    resp = client.get("/")
    assert resp.status_code == 200


def test_get_state(client):
    resp = client.get("/api/state")
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == 50
    assert len(data[0]) == 50


def test_post_step(client):
    # Place a blinker and step
    app_module.grid[1][0] = 1
    app_module.grid[1][1] = 1
    app_module.grid[1][2] = 1
    resp = client.post("/api/step")
    data = resp.get_json()
    # Blinker flips vertical
    assert data[0][1] == 1
    assert data[1][1] == 1
    assert data[2][1] == 1


def test_post_toggle(client):
    resp = client.post("/api/toggle", json={"row": 5, "col": 5})
    data = resp.get_json()
    assert data[5][5] == 1
    # Toggle back
    resp = client.post("/api/toggle", json={"row": 5, "col": 5})
    data = resp.get_json()
    assert data[5][5] == 0


def test_post_reset(client):
    app_module.grid[0][0] = 1
    resp = client.post("/api/reset")
    data = resp.get_json()
    assert all(cell == 0 for row in data for cell in row)


def test_post_random(client):
    resp = client.post("/api/random")
    data = resp.get_json()
    assert len(data) == 50
    assert all(cell in (0, 1) for row in data for cell in row)
