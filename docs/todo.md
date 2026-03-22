# Implementation Todo

## Project Structure

```
Game Of Life/
├── app.py              # Flask server & game logic
├── requirements.txt    # Python dependencies
├── test_game.py        # Unit tests (pytest)
├── static/
│   └── sketch.js       # p5.js frontend code
├── templates/
│   └── index.html      # Main HTML page
└── docs/
    ├── CLAUDE.md       # Claude Code guidelines
    ├── README.md       # Project documentation
    └── todo.md         # This file
```

## Dependencies

- **Backend:** Flask (Python)
- **Frontend:** p5.js (loaded via CDN)

## Implementation Checklist

### 1. Project Setup

- [x] Create folder structure (static/, templates/, docs/)
- [x] Create requirements.txt with flask
- [x] Verify: `pip install -r requirements.txt` succeeds

### 2. Backend Core — Game Logic

- [x] Implement grid model (50x50, cells 0/1)
- [x] Implement neighbor counting
- [x] Implement Conway rules (step function)
- [x] Verify: unit test — glider advances correctly after one step

### 3. Backend — Flask Server & API

- [x] GET / serves index.html
- [x] GET /api/state returns grid JSON
- [x] POST /api/step advances generation, returns grid
- [x] POST /api/toggle toggles cell at {row, col}
- [x] POST /api/reset clears grid
- [x] POST /api/random randomizes grid
- [x] Verify: curl each endpoint, confirm correct JSON responses

### 4. Frontend — HTML & p5.js Setup

- [ ] Create index.html loading p5.js from CDN
- [ ] Create sketch.js with setup() and draw()
- [ ] Render grid fetched from /api/state
- [ ] Verify: open browser, see empty grid rendered

### 5. Frontend — Interaction & Controls

- [ ] Click to toggle cells (calls /api/toggle)
- [ ] Start/Stop button (auto-step mode)
- [ ] Step button (single generation)
- [ ] Reset button
- [ ] Random button
- [ ] Verify: all buttons work, clicking toggles cells

### 6. Polish & Integration

- [ ] Adjustable speed for auto-step
- [ ] Visual styling (alive=white, dead=black)
- [ ] Full end-to-end test: create glider, run, observe movement
