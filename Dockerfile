# Base Image: Lightweight Python
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt .

# Install dependencies (no cache for smaller image)
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY run_aero_tests.py .

# Create a non-root user for security
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Default command: Run the Engineering Simulation (CREA-SP)
CMD ["python", "-m", "src.main_simulation"]
