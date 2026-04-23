# Start from official Python image
FROM python:3.11

# Set working directory inside container
WORKDIR /app

# Copy requirements first (better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install chromium
RUN playwright install-deps chromium

# Copy all test files
COPY . .
ENV PYTHONPATH=/app
# Default command — run tests
#
CMD ["pytest", "tests/", "-v", "-s"]