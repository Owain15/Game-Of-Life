# Claude Code Guidelines

## Workflow Rules

- **Feature independence**: Each feature must be independent and testable on its own.
- **Stop after each feature**: After completing a feature, stop and wait for human verification before continuing.
- **Git checkpoints**: The user will review and commit after each feature. Do not auto-commit.
- **Test before stopping**: Ensure all tests pass before presenting the completed feature for review.
- **Commit summary**: After presenting a feature for review, provide a suggested git commit title and short summary describing the changes made.

## Solution Structure & Responsibilities

| Layer | Technology | Responsibility |
|-------|-----------|----------------|
| **Backend** | Python / Flask (`app.py`) | Game logic (grid model, Conway rules, step function), REST API endpoints |
| **Frontend display** | p5.js (`static/sketch.js`) | Rendering the grid visually, all drawing/animation — p5 is responsible for displaying backend state |
| **Frontend page** | HTML (`templates/index.html`) | Page structure, loading p5.js via CDN, UI controls (buttons, speed slider) |
| **API** | Flask routes in `app.py` | Bridge between frontend and backend — serves grid state as JSON, accepts user actions |

| **Tests** | pytest (`test_game.py`) | Verify each feature independently before presenting for review |

### Key principle
The backend owns all game state and logic. The frontend (p5.js) is purely a display and input layer — it fetches state from the API and renders it, but never computes game logic itself.
