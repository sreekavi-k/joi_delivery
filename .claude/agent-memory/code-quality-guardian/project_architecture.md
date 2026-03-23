---
name: JOI Delivery — Architecture and Code Patterns
description: Observed architectural decisions, conventions, and patterns in the JOI Delivery codebase
type: project
---

## Architecture
Three-layer: controller → service → domain. All data in-memory, seeded at startup via `generator/app_initializer.py`. No database.

## Key Conventions Observed
- Domain objects are plain `@dataclass` classes; they serialise themselves via `to_json()` — no Pydantic in domain layer.
- `Cart` uses `response_model=Cart` directly in the router (FastAPI infers from `to_json()` dict return), not a Pydantic schema. This works because the controller returns the dataclass instance and FastAPI calls `.dict()` / Pydantic v2 model coercion.
- `CartService` is the only service allowed to depend on other services.
- Controller Pydantic models live in `controller/models.py` — request schemas (`AddProductRequest`) and response schemas (`CartProductInfo`) are defined there.
- `FoodProduct` and `Restaurant` are intentional stubs — no logic should be added unless explicitly asked.

## Known Structural Issue
- `src/joi_delivery/my-fastapi-app/` is a stray directory inside the package that should not be there. It contains a separate incomplete FastAPI scaffold that breaks `poetry run pytest` (pytest picks it up and fails because its deps are not installed). It also generates 16 ruff lint errors.

## Seed Data Issue (Bug)
- `app_initializer.py` line 55: `cart_for_users["user102"]` references `user101` as the `user` argument to `create_cart_for_user`. `user102` does not exist as a `User` object — only `user101` is created. This is a data-integrity bug in seed data.

## Import Style
- All application code (src + tests) passes ruff with zero errors when `my-fastapi-app` is excluded.
- `app.py` root entry point and test files have minor import-ordering violations (I001) that are auto-fixable.

## Test Patterns
- Tests use class-based style: `class TestCartController`, `class TestInventoryController`.
- Test naming follows `test_should_<behaviour>` convention.
- Tests mock at the service method level using `@patch("joi_delivery.controller.cart_controller.CartService.<method>")`.
- Only controller-level tests exist — no service-layer or domain-layer unit tests.

**Why these matter:** Recurring issues to check in future PRs: the my-fastapi-app directory, missing service/domain tests, and seed data correctness.
