# 🛒 E-Commerce QA Automation Framework

## 🚀 Overview

A production-ready QA automation framework combining **API + UI testing** using:

- Pytest
- Playwright
- Allure Reports
- GitHub Actions (CI/CD)

---

## 🧩 Features

- ✅ API Testing (REST)
- ✅ UI Testing (Playwright)
- ✅ Parallel Execution (`pytest-xdist`)
- ✅ CI/CD Pipeline (GitHub Actions)
- ✅ Allure Reporting
- ✅ Environment-based configuration
- ✅ Mocking support (for CI stability)

---

## 🏗️ Tech Stack

- Python
- Pytest
- Playwright
- Requests
- Allure
- GitHub Actions

---

## 📂 Project Structure

```
ecom-qa-framework/
│
├── tests/
│   ├── api/
│   ├── ui/
│
├── pages/
├── utils/
├── conftest.py
├── pytest.ini
├── requirements.txt
```

---

## ⚙️ Setup

```bash
git clone <repo>
cd ecom-qa-framework
pip install -r requirements.txt
playwright install
```

---

## ▶️ Run Tests

### Smoke Tests

```bash
pytest -m smoke
```

### Regression Tests

```bash
pytest -m regression
```

### Parallel Execution

```bash
pytest -n auto
```

---

## 📊 Reports

### Allure

```bash
pytest --alluredir=allure-results
allure serve allure-results
```

---

## 🔄 CI/CD

- Runs on push & PR
- Smoke → Regression flow
- Parallel execution
- Artifact upload

---

## ⚠️ Challenges & Solutions

### Problem:

API blocked in CI

### Solution:

- Used environment variables
- Introduced mocking
- Skipped invalid UI assertions

---

## 🎯 Future Enhancements

- Contract testing (JSON schema)
- Visual UI testing
- Service virtualization
- Test data management

---

## 💡 Author

Dharmateja – QA Automation Engineer

---

## 🧠 Key Learning

Reliable automation =
✔ Independent
✔ Stable
✔ CI-friendly
✔ Scalable
