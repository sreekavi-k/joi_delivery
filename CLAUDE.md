# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
poetry install --with dev

# Run the app
poetry run python app.py
# or via the installed script:
app

# Run all tests
poetry run pytest

# Run a single test file
poetry run pytest tests/controller/test_cart_controller.py

# Run a single test by name
poetry run pytest -k "test_should_add_the_requested_product_to_the_cart"

# Run tests with coverage
poetry run pytest --cov=src/joi_delivery

# Lint
poetry run ruff check .

# Format
poetry run ruff format .
```

App runs at `http://localhost:8020`. API docs at `/docs`.

## Architecture

The app follows a three-layer architecture with no database — all data lives in-memory, seeded at startup.

```
controller/  →  service/  →  domain/
(HTTP in/out)   (logic)      (data structures)
```

**Request lifecycle:** FastAPI router dispatches to a controller → controller receives injected services via `Depends()` → service performs business logic using domain objects → domain objects serialise themselves via `to_json()` → JSON response returned.

**Service injection:** `main.py:create_app()` seeds data, constructs the three services (`UserService`, `ProductService`, `CartService`), and stores them on `app.state`. `dependencies.py` exposes them as FastAPI dependency functions that controllers declare with `Depends()`.

**`CartService`** depends on both `UserService` and `ProductService` — it is the only service with inter-service dependencies.

**Domain model hierarchy:**
- `Product` (ABC) → `GroceryProduct` (concrete), `FoodProduct` (stub)
- `Outlet` (base) → `GroceryStore` (concrete), `Restaurant` (stub)
- `User` holds a reference to a `Cart`; `Cart` holds a list of `Product` objects and belongs to an `Outlet`

**Seed data (defined in `generator/app_initializer.py`):**
- Users: `user101` (John Doe)
- Stores: `store101` (Fresh Picks), `store102` (Natural Choice)
- Products: `product101` (Wheat Bread), `product102` (Spinach), `product103` (Crackers) — all at `store101`

## What is incomplete

- `FoodProduct` and `Restaurant` are stubs with no logic
- `GET /inventory/health` returns 200 but no data (marked to be implemented)
- No persistence — all state resets on restart
