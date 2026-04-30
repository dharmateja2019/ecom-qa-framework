# E-Commerce QA Automation Framework

A production-style QA automation framework designed for **API, UI, DB, and AI validation** of an e-commerce system.

Built to simulate real-world testing challenges including:

- Parallel execution
- Flaky test retries
- Dockerized execution
- Local + CI/CD runs
- GitHub Actions automation
- Jenkins enterprise pipelines
- Reporting and artifacts

---

## 🚀 Key Highlights

- Multi-layer testing: API + UI + DB + AI
- Pytest + Playwright + Requests + SQLite
- Parallel execution using `pytest-xdist`
- Retry flaky tests using `pytest-rerunfailures`
- Docker + Docker Compose support
- GitHub Actions CI/CD
- Jenkins parameterized CI pipeline
- Allure artifact reporting

---

## 📁 Project Structure

```text
ecom-qa-framework/
├── tests/
│   ├── api/
│   ├── ui/
│   ├── db/
│   └── ai/
├── pages/
├── utils/
├── .github/workflows/
│   ├── tests.yml
│   └── container-ci.yml
├── Dockerfile
├── docker-compose.yml
├── Jenkinsfile
├── requirements.txt
├── pytest.ini
└── README.md
```

---

## 🖥️ Execution Modes

This framework supports **three execution modes**:

### 1. Local Execution

Used for development, debugging, and fast feedback.

```bash
pytest tests/ -v
pytest tests/api -n auto
pytest tests/ui
pytest -m smoke
pytest -m regression
```

### Local Docker Run

```bash
docker build -t qa-tests:latest .
docker run qa-tests:latest
```

### Local Docker Compose Run

```bash
docker compose up --build
docker compose run qa-tests pytest tests/api -n auto
docker compose down -v
```

---

## ⚙️ GitHub Actions CI/CD

### Workflow 1: Native Runner (`tests.yml`)

Runs on every push / PR.

- Smoke tests
- Regression tests
- Parallel execution
- Retry failures
- Upload Allure artifacts

### Workflow 2: Container CI (`container-ci.yml`)

Runs containerized validation.

- Build Docker image
- Run API / UI / DB / Smoke / Regression suites
- Upload suite artifacts
- Run Docker Compose integration tests
- Cleanup environment

---

## 🏢 Jenkins CI Pipeline

Enterprise-style parameterized pipeline.

### Build Parameters

- SMOKE
- REGRESSION
- API
- DB
- UI
- ALL

### Features

- GitHub SCM integration
- Docker Compose execution
- Build history
- Artifact archival
- Logs + timings
- Cleanup after build

---

## 📊 Reporting

### GitHub Actions

Uses `upload-artifact`

### Jenkins

Uses `archiveArtifacts`

Artifacts include:

- reports/
- allure-results/
- logs/

---

## 🧠 Why This Framework Is Strong

- Same tests run locally, in GitHub Actions, and Jenkins
- Containerized for consistency
- Real CI/CD architecture
- Scalable for enterprise QA teams

---

## 💼 Resume Value

Designed and implemented a Dockerized QA automation framework integrated with Jenkins and GitHub Actions supporting API, UI, DB, smoke, regression, and artifact-driven CI pipelines.
