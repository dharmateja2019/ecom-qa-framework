.PHONY: lint test coverage security all

lint:
	flake8 .
	pylint .

security:
	bandit -r utils pages -c bandit.yaml

test:
	pytest

coverage:
	pytest --cov=. --cov-report=term-missing

all: lint security test
	@echo "All checks passed."