# E-Commerce QA Automation Framework

A scalable, production-style QA automation framework designed for API, UI, and AI validation of an e-commerce system.

Built from scratch to simulate real-world testing challenges including data validation, contract testing, flaky test handling, and CI/CD execution.

## 🚀 Key Highlights

- Multi-layer testing: API + UI + AI validation
- Parallel execution using pytest-xdist
- CI/CD pipeline using GitHub Actions
- SLA validation for performance benchmarking
- LLM-based validation using local models (Ollama)
- Environment-based execution (staging/production)

## 📐 Test Strategy (Test Pyramid)

The framework follows the Test Pyramid approach:

- API Tests (Majority) → Fast, reliable, run on every commit
- UI Tests → Critical user flows, slower but necessary
- AI Tests → Advanced validation layer (local execution only)

This ensures faster feedback cycles while maintaining high coverage.

## 🏗️ Architecture Overview

The framework is designed using a layered architecture:

- Test Layer (Pytest) → Test definitions and assertions
- API Layer → Handles backend validation using Requests
- UI Layer → Handles frontend testing using Playwright
- AI Layer → Validates business logic using LLMs

Each layer is isolated to ensure maintainability, scalability, and independent execution.

## 🧠 Key Design Decisions

- Used session fixtures for static data to reduce API calls and improve speed
- Used factory fixtures for dynamic data generation across tests
- Separated API, UI, and AI tests to allow selective execution
- Excluded AI tests from CI due to infrastructure dependency (Ollama)
- Avoided caching for SLA tests to ensure accurate performance measurement

## 🐞 Bugs Identified During Testing

- GET /products/{id} returns HTTP 200 with null body instead of 404
  → Impact: Frontend cannot distinguish between valid and invalid responses

- Cloudflare blocking API requests in CI environment (403 error)
  → Solution: Migrated to DummyJSON for reliable automation execution

## 🆕 Latest Enhancements

- SQLite database validation for API ↔ DB consistency
- API contract testing using JSON Schema
- Structured logging for CI debugging
- Faker-powered dynamic test data generation
- Authentication workflow coverage (login / token / protected APIs)

## 💡 What Makes This Framework Different

- Built from scratch (not tutorial-based)
- Includes AI-powered validation layer
- Designed with real-world CI/CD constraints
- Focuses on business logic validation, not just status codes

## 📊 Current Test Coverage Snapshot

- 40+ automated tests
- Smoke + Regression suites
- API / UI / DB / AI layers
- GitHub Actions CI pipeline
- Parallel execution enabled
