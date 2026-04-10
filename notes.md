# QA Automation Notes (API + UI + CI/CD)

---

## 1. Expected vs Actual Behaviour

- **Expected Behaviour**: Validate against predefined requirements
  👉 Use when requirements are clear

- **Actual Behaviour**: Observe system output without strict expectation
  👉 Use for debugging, exploratory testing

---

## 2. Why Check curl + Browser?

- `curl` → raw response (status, headers, JSON)
- Browser → UI rendering

✅ Ensures issue is not tool-specific
✅ Helps isolate backend vs frontend problems

---

## 3. Frontend Impact of API Bug

- Broken product listing
- Missing/incorrect data
- Poor UX → loss of trust/revenue

---

## 4. Types of API Assertions

- **Status Code** → API success/failure
- **Response Body** → Data correctness
- **Headers** → metadata validation
- **Performance (SLA)** → response time
- **Error Handling** → invalid inputs

---

## 5. Why Use Fixtures?

- Reusable setup
- Cleaner tests
- Centralized logic

⚠️ Rule:

- Use fixture for **static/shared data**
- Avoid for **dynamic inputs (use parametrize)**

---

## 6. autouse=True Usage

Use when:

- Common setup required for all tests

Avoid when:

- Only some tests need it
- Adds unnecessary overhead

---

## 7. Fixture Return Type

✅ Return parsed data (JSON)
❌ Avoid raw response unless needed

---

## 8. Why SLA Test Avoids Fixtures

- Fixture data is cached (session scope)
- SLA requires **real-time measurement**

👉 Always make fresh API call for performance tests

---

## 9. API Blocking in CI/CD (GitHub Actions)

### Problem

Tests failed in CI but passed locally.

### Root Cause

- Public APIs block CI IPs
- Rate limiting / instability

---

### Solution

- Use environment variables for BASE_URL
- Avoid hardcoded endpoints
- Skip invalid UI-API tests

---

## 10. CI/CD Enhancements

### Environment Config

```python
BASE_URL = os.getenv("BASE_URL", "https://dummyjson.com")
```

---

### Mocking (Recommended)

```python
page.route("**/products", lambda route: route.fulfill(
    status=200,
    body='{"products":[{"id":1,"title":"Mock Product","price":100}]}'
))
```

---

### Retry (Optional)

- Helps flaky tests
- Should not hide real issues

---

### Test Strategy

- Smoke → real API
- Regression → mocked

---

### Skip Invalid Tests

```python
@pytest.mark.skip(reason="UI does not display product count reliably")
```

---

## 11. Key QA Principles

- Do not depend on external systems
- Validate layers independently (API vs UI)
- Avoid flaky assertions
- Use mocks for stability

---

## 12. Interview Insight

“In CI/CD, external APIs can be unreliable. I used environment-based configuration and mocking to ensure stable, deterministic test execution.”
