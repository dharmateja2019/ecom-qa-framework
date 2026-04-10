# E-Commerce QA Automation Framework

API and UI test automation framework for an e-commerce domain.
Built from scratch over 4 days as a learning project to own
every line of code.

## Tech stack

- Python, Pytest
- Playwright (UI testing)
- Requests (API testing)
- GitHub Actions (CI/CD)

## Project structure

ecom-qa-framework/
tests/
api/ — API test suite
ui/ — UI test suite
pages/ — Page Object Model classes
utils/ — API client
config/ — Environment settings
conftest.py — Shared fixtures
pytest.ini — Pytest configuration

## Setup

pip install -r requirements.txt
playwright install chromium

## Run tests

pytest tests/ -v # full suite
pytest tests/ -v -m smoke # smoke only
pytest tests/ -v -m regression # regression only

## Environment config

BASE_URL=https://dummyjson.com pytest tests/ -v

## CI/CD

GitHub Actions runs smoke tests on every push.
Regression tests run after smoke passes.
See .github/workflows/tests.yml

## What I built and can explain

- API client with timeout and environment config
- Session-scoped fixtures for shared test data
- Parametrized tests across product IDs and categories
- Page Object Model with BasePage inheritance
- Smoke vs regression marker strategy
- Integration test that validates API data matches UI
- Found and documented a real API bug (GET /products/99999
  returns 200 with null body instead of 404)

## Known issues

- fakestor.com is unrealiable due to block by github actions IPs
