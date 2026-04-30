# QA Framework Architecture

## High-Level Execution Model

```text
                    Same Test Framework
                           │
      ┌────────────────────┼────────────────────┐
      ▼                    ▼                    ▼
   Local Run        GitHub Actions          Jenkins
   pytest           Auto CI/CD              Manual CI
   docker compose   Push / PR checks        Parameterized runs
```

---

## Layered Test Architecture

```text
                 ┌─────────────────┐
                 │   Test Layer    │
                 │    (Pytest)     │
                 └────────┬────────┘
                          │
      ┌────────────┬──────┼──────┬────────────┐
      ▼            ▼             ▼            ▼
   API Layer    UI Layer      DB Layer     AI Layer
  Requests     Playwright     SQLite       Ollama
```

---

## GitHub Actions Architecture

```text
Push / Pull Request
        │
        ▼
 ┌───────────────┐
 │ tests.yml     │
 ├─ Smoke Tests  │
 └─ Regression   │

        │

 ┌───────────────┐
 │ container-ci  │
 ├─ Docker Build │
 ├─ API/UI/DB    │
 ├─ Smoke/Reg    │
 └─ Compose Test │
```

---

## Jenkins Architecture

```text
Manual Trigger
      │
      ▼
Select TEST_SUITE
(API/UI/DB/SMOKE/ALL)
      │
      ▼
Docker Compose Run
      │
      ▼
Archive Reports
```

---

## Runtime Infrastructure

```text
Dockerfile → qa-tests image
docker-compose.yml → runtime config
Jenkins/GHA → orchestration layer
```

---

## Artifact Strategy

| Platform       | Storage          |
| -------------- | ---------------- |
| Local          | reports folder   |
| GitHub Actions | upload-artifact  |
| Jenkins        | archiveArtifacts |

```

```
