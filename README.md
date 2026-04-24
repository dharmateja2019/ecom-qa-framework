# E-Commerce QA Automation Framework

A scalable, production-style QA automation framework designed for API, UI, DB, and AI validation of an e-commerce system.

Built from scratch to simulate real-world testing challenges including data validation, contract testing, flaky test handling, parallel execution, containerised testing, and CI/CD execution.

---

## 🚀 Key Highlights

- Multi-layer testing: API + UI + DB + AI validation
- Parallel execution using pytest-xdist (`-n auto`)
- Containerised test execution using Docker and Docker Compose
- CI/CD pipeline using GitHub Actions (native runner + Docker workflows)
- SLA validation for performance benchmarking
- LLM-based validation using local models (Ollama)
- Environment-based execution (staging/production)
- Allure reporting with CI artifact upload
- Retry mechanism for flaky test resilience (`--reruns 2`)

---

## 📐 Test Strategy (Test Pyramid)

The framework follows the Test Pyramid approach:

- **API Tests (Majority)** → Fast, reliable, run on every commit
- **UI Tests** → Critical user flows, slower but necessary
- **DB Tests** → Data integrity and API ↔ DB consistency
- **AI Tests** → Advanced validation layer (local execution only)

This ensures faster feedback cycles while maintaining high coverage.

---

## 🏗️ Architecture Overview

The framework is designed using a layered architecture:

- **Test Layer (Pytest)** → Test definitions and assertions
- **API Layer** → Backend validation using Python `requests` library
- **UI Layer** → Frontend testing using Playwright
- **DB Layer** → SQLite data integrity and API ↔ DB consistency
- **AI Layer** → Business logic validation using local LLMs (Ollama)

Each layer is isolated to ensure maintainability, scalability, and independent execution.

---

## 📁 Project Structure

```
ecom-qa-framework/
├── tests/
│   ├── api/                  # API test cases
│   ├── ui/                   # Playwright UI tests
│   ├── db/                   # Database validation tests
│   └── ai/                   # LLM-based AI validation tests
├── pages/                    # Page Object Model classes
│   ├── base_page.py
│   └── product_catalog.py
├── utils/                    # Shared utilities
│   ├── api_client.py         # Requests wrapper with logging
│   ├── auth_setup.py         # JWT auth helpers
│   ├── db_helper.py          # SQLite connection and queries
│   └── ai_model.py           # Ollama LLM interface
├── .github/
│   └── workflows/
│       ├── tests.yml         # Native runner CI (smoke + regression)
│       └── docker-ci.yml     # Docker + Docker Compose CI
├── Dockerfile                # Container image for test execution
├── docker-compose.yml        # Multi-container orchestration
├── conftest.py               # Root-level shared fixtures
├── pytest.ini                # Markers, headed/headless, retries
├── requirements.txt          # Python dependencies
└── README.md
```

---

## 🐳 Docker Setup

The framework is fully containerised. Tests run inside a Docker container to ensure consistent execution across local machines and CI environments.

### Dockerfile

```dockerfile
FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install chromium
RUN playwright install-deps chromium

COPY . .
ENV PYTHONPATH=/app

CMD ["pytest", "tests/", "-v", "-s"]
```

### Build and run

```bash
# Build image
docker build -t qa-tests:latest .

# Run all tests
docker run qa-tests:latest

# Run only API tests in parallel
docker run qa-tests:latest pytest tests/api/ -v -n auto

# Run with volume to persist reports
docker run -v $(pwd)/reports:/app/reports qa-tests:latest
```

### Docker Compose

Docker Compose orchestrates the test container with environment variables and persistent volumes.

```yaml
services:
  qa-tests:
    build: .
    container_name: qa-tests
    environment:
      - BASE_URL=https://dummyjson.com
    volumes:
      - ./reports:/app/reports
      - ./test_data.db:/app/test_data.db
    command: pytest tests/ -v -s
```

```bash
# Start and run tests
docker compose up --build

# Run in background
docker compose up -d

# Run specific service
docker compose run qa-tests pytest tests/api/ -v -n auto

# Stop and clean up
docker compose down -v
```

### Results in Docker

```
39 passed, 3 skipped in 24.60s        # sequential run
29 passed in 3.51s                     # parallel run with 16 workers (-n auto)
```

All test layers — API, UI, DB, AI — run successfully inside the container.

---

## ⚙️ CI/CD — GitHub Actions

Two separate workflows handle different execution strategies.

### Workflow 1 — Native Runner (tests.yml)

Runs on every push and PR to `main`. Uses Ubuntu runner with Python 3.11 directly.

**Smoke Tests job:**

- Triggered on every push/PR
- Runs `pytest -m "smoke and not ai"` with parallel workers and retry
- Uploads Allure results as artifact

**Regression Tests job:**

- Runs only after smoke tests pass (`needs: smoke-tests`)
- Runs `pytest -m "regression and not ai"` with parallel workers
- Uploads Allure results as artifact

**Key features:**

- Pip dependency caching for faster builds
- `--reruns 2 --reruns-delay 1` for flaky test resilience
- Allure results uploaded as downloadable artifacts
- AI tests excluded from CI (`not ai`) — require local Ollama

### Workflow 2 — Docker CI (docker-ci.yml)

Validates that the Docker setup works correctly in CI.

**Docker Image Test job:**

- Builds the Docker image from Dockerfile
- Runs API tests inside the container

**Docker Compose Test job:**

- Runs after Docker Image Test passes (`needs: docker-test`)
- Spins up full stack using `docker compose up --build`
- `--abort-on-container-exit` ensures CI fails if tests fail
- Always cleans up with `docker compose down -v`

### CI Strategy

| Trigger           | Workflow      | Tests run                       | Speed    |
| ----------------- | ------------- | ------------------------------- | -------- |
| Every push/PR     | tests.yml     | Smoke (API + UI, parallel)      | Fast     |
| After smoke pass  | tests.yml     | Regression (API + UI, parallel) | Medium   |
| Every push/PR     | docker-ci.yml | API tests in Docker             | Fast     |
| After docker pass | docker-ci.yml | Full suite via Compose          | Medium   |
| Nightly (planned) | tests.yml     | Full regression                 | Complete |

---

## 🧠 Key Design Decisions

- Session fixtures for static data reduce API calls and improve speed
- Factory fixtures for dynamic data allow argument passing per test
- AI tests excluded from CI — infrastructure failure ≠ test failure, graceful skip when Ollama unavailable
- SLA tests avoid cached fixtures — response time measured from live call
- `PYTHONPATH=/app` set in Docker to resolve module imports correctly
- Separate Docker workflow validates containerised execution independently from native runner

---

## 🐞 Bugs Identified During Testing

- `GET /products/{id}` returns HTTP 200 with null body instead of 404
  → Impact: Frontend cannot distinguish valid from invalid responses

- Cloudflare blocking API requests in CI environment (403 error)
  → Solution: Migrated to DummyJSON for reliable automation execution

---

## 🆕 Latest Enhancements

- **Docker containerisation** — full test suite runs inside Docker
- **Docker Compose** — environment variables and volume persistence
- **Docker CI workflow** — GitHub Actions validates container execution
- SQLite database validation for API ↔ DB consistency
- API contract testing using JSON Schema
- Structured logging for CI debugging
- Faker-powered dynamic test data generation
- Authentication workflow coverage (login / token / protected APIs)

---

## 📊 Current Test Coverage

- **42 automated tests** across 4 layers
- **39 passing, 3 skipped** (AI tests skip gracefully without Ollama)
- Smoke + Regression suites with markers
- API / UI / DB / AI layers
- GitHub Actions CI — 2 workflows, both green ✅
- Docker + Docker Compose execution verified ✅
- Parallel execution — 16 workers, 29 API tests in 3.51s

---

## 💡 What Makes This Framework Different

- Built from scratch — not tutorial-based
- Fully containerised with Docker and Docker Compose
- Dual CI strategy — native runner + Docker workflow
- Includes AI-powered validation layer
- Designed with real-world CI/CD constraints
- Focuses on business logic validation, not just status codes
- Test Pyramid structure with independent layer execution
