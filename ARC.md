# QA Automation Architecture

## High-Level Architecture

            ┌──────────────┐
            │   Test Layer │
            │   (Pytest)   │
            └──────┬───────┘
                   │
        ┌──────────┴──────────┐
        │                     │

┌──────────────┐ ┌──────────────┐
│ API Layer │ │ UI Layer │
│ (Requests) │ │ (Playwright) │
└──────┬───────┘ └──────┬───────┘
│ │
└──────────┬──────────┘
│
┌──────────────┐
│ Application │
│ (DummyJSON) │
└──────────────┘

## Why API, UI, and AI are in separate folders

Each layer has a different execution requirement. API tests
run fast with no browser — suitable for every commit. UI tests
are slower and need a browser installed. AI tests require a
local Ollama server and cannot run in CI. Separating them means
you can run pytest -m "not ai" in CI and pytest tests/ai/
locally without mixing concerns.

## Why session scope vs factory fixture

Session scope is used when the data doesn't change between
tests — for example fetching the product catalogue once and
sharing it across all tests that need it. This avoids repeated
API calls and speeds up the suite.

Factory fixtures return a function instead of data directly.
This is used when tests need to pass different arguments — for
example get_product(1), get_product(2). A regular session
fixture cannot accept arguments from tests. The factory pattern
solves this while still living in conftest.py.

## Why conftest.py lives at the root

Pytest automatically discovers conftest.py files and makes
their fixtures available to all tests in the same directory
and below. A root-level conftest.py means every test file —
api, ui, ai — can use the same fixtures without importing
anything. If conftest.py lived inside tests/api/, the UI tests
would not see those fixtures.

## Test strategy

| Layer | Marker     | Runs in CI | Runs locally |
| ----- | ---------- | ---------- | ------------ |
| API   | smoke      | Yes        | Yes          |
| API   | regression | Yes        | Yes          |
| UI    | smoke      | Yes        | Yes          |
| UI    | regression | Yes        | Yes          |
| AI    | ai         | No         | Yes          |

## CI/CD flow

Push to main
→ Smoke tests (API + UI, parallel)
→ Regression tests (API + UI, parallel, needs smoke pass)
→ Allure results uploaded as artifact

## Design decisions

Do not use the same fixture for SLA tests. Response time
must be measured from a live call — cached data from a
session fixture would measure elapsed time from when the
fixture ran, not when the test ran.

AI tests use pytest.skip when Ollama is unavailable rather
than failing. Infrastructure failure is different from a
test failure. A failing test means the code has a bug. A
skipped test means a dependency was unavailable.
