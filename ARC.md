# QA Automation Architecture

## High-Level Architecture

```
            ┌──────────────────────────┐
            │       Test Layer         │
            │        (Pytest)          │
            └────────────┬─────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
┌────────┴──────┐ ┌──────┴──────┐ ┌─────┴───────┐
│   API Layer   │ │   UI Layer  │ │   DB Layer  │
│  (Requests)   │ │ (Playwright)│ │  (SQLite)   │
└───────┬───────┘ └──────┬──────┘ └──────┬──────┘
        │                │               │
        └────────────────┼───────────────┘
                         │
              ┌──────────┴──────────┐
              │    Application      │
              │    (DummyJSON)      │
              └─────────────────────┘
```

## Extended Architecture (All Layers)

```
            ┌──────────────────────────────┐
            │          Test Layer          │
            │           (Pytest)           │
            └──────────────┬───────────────┘
                           │
     ┌──────────┬──────────┼──────────┬──────────┐
     │          │          │          │          │
┌────┴────┐ ┌──┴──────┐ ┌─┴──────┐ ┌─┴──────┐   │
│  API    │ │   UI    │ │   DB   │ │   AI   │   │
│Requests │ │Playwright│ │SQLite  │ │ Ollama │   │
└─────────┘ └─────────┘ └────────┘ └────────┘   │
                                                  │
                    ┌─────────────────────────────┘
                    │
          ┌─────────┴──────────┐
          │  Infrastructure    │
          │  Docker / GitHub   │
          │  Actions CI/CD     │
          └────────────────────┘
```

## Container Architecture

```
┌─────────────────────────────────────────────┐
│              Docker Container               │
│              (qa-tests:latest)              │
│                                             │
│  FROM python:3.11                           │
│  ├── requirements.txt installed             │
│  ├── Playwright chromium installed          │
│  ├── PYTHONPATH=/app                        │
│  └── CMD: pytest tests/ -v -s              │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │           Test Suite                │   │
│  │  tests/api/  tests/ui/              │   │
│  │  tests/db/   tests/ai/              │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
          │                    │
          ▼                    ▼
  ./reports (volume)   ./test_data.db (volume)
  persisted on host    persisted on host
```

## Docker Compose Architecture

```
┌─────────────────────────────────────────────┐
│           docker-compose.yml                │
│                                             │
│  services:                                  │
│    qa-tests:                                │
│      build: .  (from Dockerfile)            │
│      env: BASE_URL=https://dummyjson.com    │
│      volumes:                               │
│        ./reports  → /app/reports            │
│        ./test_data.db → /app/test_data.db   │
│      command: pytest tests/ -v -s           │
└─────────────────────────────────────────────┘
```

**One command to run everything:**

```bash
docker compose up --build
# Result: 39 passed, 3 skipped in 24.60s
```

## CI/CD Architecture — GitHub Actions

### Workflow 1: Native Runner (tests.yml)

```
Push / PR to main
        │
        ▼
┌───────────────────┐
│   Smoke Tests     │  runs-on: ubuntu-latest
│                   │  pytest -m "smoke and not ai"
│  - pip cache      │  -n auto (parallel)
│  - install deps   │  --reruns 2
│  - run smoke      │  --alluredir=allure-results
│  - upload allure  │
└────────┬──────────┘
         │ needs: smoke-tests
         ▼
┌───────────────────┐
│ Regression Tests  │  runs-on: ubuntu-latest
│                   │  pytest -m "regression and not ai"
│  - pip cache      │  -n auto (parallel)
│  - install deps   │  --reruns 2
│  - run regression │  --alluredir=allure-results
│  - upload allure  │
└───────────────────┘
```

### Workflow 2: Docker CI (docker-ci.yml)

```
Push / PR to main
        │
        ▼
┌───────────────────────┐
│  Docker Image Test    │  runs-on: ubuntu-latest
│                       │
│  docker build \       │
│    -t qa-tests:latest │
│                       │
│  docker run \         │
│    qa-tests:latest \  │
│    pytest tests/api   │
└──────────┬────────────┘
           │ needs: docker-test
           ▼
┌───────────────────────┐
│  Docker Compose Test  │  runs-on: ubuntu-latest
│                       │
│  docker compose up \  │
│    --build \          │
│    --abort-on-        │
│    container-exit     │
│                       │
│  post: always         │
│  docker compose down  │
└───────────────────────┘
```

### Full CI Strategy

| Trigger           | Workflow      | Job              | Tests                       | Execution       |
| ----------------- | ------------- | ---------------- | --------------------------- | --------------- |
| Push/PR           | tests.yml     | smoke-tests      | API + UI smoke, not AI      | parallel, retry |
| After smoke       | tests.yml     | regression-tests | API + UI regression, not AI | parallel, retry |
| Push/PR           | docker-ci.yml | docker-test      | API tests in container      | docker run      |
| After docker      | docker-ci.yml | compose-test     | Full suite via Compose      | docker compose  |
| Nightly (planned) | tests.yml     | full-regression  | All tests including AI      | sequential      |

---

## Why GitHub Actions over Jenkins

GitHub Actions is natively integrated with GitHub — no separate server to maintain, secrets management is built-in, and the YAML syntax maps directly to the workflow. For this project it was the practical choice. Jenkins is appropriate for enterprise setups where a central CI server is already running and pipelines need to integrate with non-GitHub tooling.

---

## Why API, UI, DB, and AI are in separate folders

Each layer has different execution requirements:

- **API tests** run fast with no browser — suitable for every commit
- **UI tests** are slower and require browser binaries
- **DB tests** need SQLite — fast and runs in CI
- **AI tests** require a local Ollama server — cannot run in CI

Separating them allows:

```bash
pytest -m "not ai"          # CI execution
pytest tests/ai/            # local only
pytest -m "smoke"           # fast PR feedback
pytest -m "regression"      # nightly full run
```

---

## Why session scope vs factory fixture

**Session scope** is used when data doesn't change between tests — for example fetching the product catalogue once and sharing it across all tests. This avoids repeated API calls and speeds up the suite.

**Factory fixtures** return a function instead of data directly. Used when tests need to pass different arguments — for example `get_product(1)`, `get_product(2)`. A regular session fixture cannot accept arguments from tests. The factory pattern solves this while still living in `conftest.py`.

---

## Why conftest.py lives at the root

Pytest automatically discovers `conftest.py` files and makes their fixtures available to all tests in the same directory and below. A root-level `conftest.py` means every test file — api, ui, db, ai — can use the same fixtures without importing anything. If `conftest.py` lived inside `tests/api/`, UI and DB tests would not see those fixtures.

---

## Why PYTHONPATH=/app in Docker

When running inside a Docker container, Python cannot resolve imports like `from utils.api_client import ApiClient` unless the project root is in the Python path. Setting `ENV PYTHONPATH=/app` in the Dockerfile tells Python to look for modules from `/app` — the working directory. This prevents `ModuleNotFoundError` in containerised execution.

---

## Test Strategy

| Layer | Marker     | Runs in CI | Runs locally | Runs in Docker |
| ----- | ---------- | ---------- | ------------ | -------------- |
| API   | smoke      | ✅ Yes     | ✅ Yes       | ✅ Yes         |
| API   | regression | ✅ Yes     | ✅ Yes       | ✅ Yes         |
| UI    | smoke      | ✅ Yes     | ✅ Yes       | ✅ Yes         |
| UI    | regression | ✅ Yes     | ✅ Yes       | ✅ Yes         |
| DB    | regression | ✅ Yes     | ✅ Yes       | ✅ Yes         |
| AI    | ai         | ❌ No      | ✅ Yes       | ❌ No          |

---

## CI/CD Flow (Complete)

```
Push to main
  │
  ├── Workflow 1: tests.yml
  │     ├── Smoke tests (API + UI, parallel, retry)
  │     │     └── Allure results → artifact
  │     └── Regression tests (needs smoke pass)
  │           └── Allure results → artifact
  │
  └── Workflow 2: docker-ci.yml
        ├── Docker build + API tests in container
        └── Docker Compose full suite (needs docker pass)
              └── Cleanup: docker compose down -v
```

---

## Design Decisions

**Do not use session fixture for SLA tests.**
Response time must be measured from a live call — cached data from a session fixture would measure elapsed time from when the fixture ran, not when the test ran. SLA tests always make a fresh request.

**AI tests use pytest.skip when Ollama is unavailable.**
Infrastructure failure is different from a test failure. A failing test means the code has a bug. A skipped test means a dependency was unavailable. Skipping gracefully keeps CI green while making the gap visible.

**Docker volumes for reports and database.**
Test reports and the SQLite database are mounted as volumes so they persist on the host after the container stops. Without volumes, all generated data would be lost when the container exits.

**`--abort-on-container-exit` in Docker Compose CI.**
Ensures the GitHub Actions job fails immediately if the test container exits with a non-zero code. Without this flag, `docker compose up` would hang waiting for other services even after tests finish.

**Pip caching in GitHub Actions.**
Caching `~/.cache/pip` with a key based on `requirements.txt` hash means dependencies are only re-downloaded when requirements change. This reduces CI build time significantly on unchanged runs.

---

## Supporting Utilities

| Utility               | Purpose                                                   |
| --------------------- | --------------------------------------------------------- |
| `utils/api_client.py` | Requests wrapper with structured logging                  |
| `utils/auth_setup.py` | JWT token management for authenticated tests              |
| `utils/db_helper.py`  | SQLite connection, insert, fetch, clear operations        |
| `utils/ai_model.py`   | Ollama LLM interface with graceful skip on unavailability |
| Logger                | Structured INFO logs for every request/response in CI     |
| Faker                 | Dynamic test data generation (unique emails, usernames)   |
| Schema validator      | JSON Schema contract testing for API responses            |
| Fixtures              | Session + factory pattern in root conftest.py             |
