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
# Default command: Run the Engineering Simulation (Standalone)
COPY standalone_sim.py .
CMD ["python", "standalone_sim.py"]
