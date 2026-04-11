# E-Commerce QA Automation Framework

API and UI test automation framework built for an e-commerce
domain using DummyJSON as the backend. Built from scratch to
deeply understand how real QA frameworks are structured —
not copied from tutorials.

## Why I built this

To move from executing tests inside existing frameworks to
building one from scratch. Every line of code in this
repository I wrote, debugged, and can explain.

## Tech stack

- Python — core language for all test logic
- Pytest — test runner, fixtures, markers, parametrize
- Requests — HTTP client for API testing
- Playwright — browser automation for UI testing
- pytest-xdist — parallel test execution
- pytest-rerunfailures — retry logic for flaky tests
- Allure — test reporting with artifacts
- GitHub Actions — CI/CD pipeline
- Ollama + phi3:mini — local LLM for AI-powered validation

## Project structure

ecom-qa-framework/
tests/
api/ — API test suite
ui/ — UI test suite  
 ai/ — AI validation tests (local only)
pages/ — Page Object Model classes
utils/ — API client, AI helper
config/ — Environment settings
conftest.py — Shared fixtures (session and factory)
pytest.ini — Pytest configuration

## How to run

# Install dependencies

pip install -r requirements.txt
playwright install chromium

# Full suite (excluding AI tests)

pytest tests/ -v -m "not ai" -n auto --alluredir=allure-results

# Smoke tests only

pytest tests/ -v -m "smoke and not ai"

# Regression tests only

pytest tests/ -v -m "regression and not ai"

# AI tests (requires Ollama running locally)

ollama serve
pytest tests/ai/ -v -s

# Switch environment

BASE_URL=https://staging.example.com pytest tests/ -v -m "not ai"

## What this framework covers

- Product catalogue validation with business rule assertions
- Single product data quality checks across multiple IDs
- Category filter correctness across 5 categories
- Pagination — page overlap detection and limit validation
- Auth — JWT login, protected endpoints, unauthorized access
- SLA — response time assertions against configurable threshold
- UI — page load, URL validation, storefront verification
- AI — LLM-based product data quality validation using Ollama

## What I found while building

Bug 1: GET /products/99999 on fakestoreapi returns HTTP 200
with a null body instead of 404. Verified via curl and browser.
Documented in test with comment explaining the business impact —
frontend cannot distinguish success from failure using status
codes alone.

Bug 2: fakestoreapi is blocked by Cloudflare in GitHub Actions
with a 403 response. CI servers use known IP ranges that
Cloudflare flags as bots. Fixed by migrating to DummyJSON which
allows automation traffic.

Design decision: AI tests excluded from CI pipeline because
Ollama runs as a local server — downloading an 8B model in CI
would take 15+ minutes. In production this would use a hosted
LLM API with a key stored as a GitHub secret.

## Key things I can explain in an interview

- Why session scope vs factory fixture pattern
- Why SLA tests cannot use cached fixture data
- How POM prevents locator duplication across test files
- Why the AI test uses pytest.skip for LLM failures
  instead of assert False
- How environment variables enable staging vs production
  switching without code changes
