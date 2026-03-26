FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

# Install baseline OS dependencies for TRL-9 Forensics
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
        curl \
        git-lfs \
        build-essential \
        libssl-dev \
        libffi-dev \
        python3-dev \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Pre-install core Data Science & Cloud components
RUN pip install --no-cache-dir \
    google-cloud-storage \
    google-cloud-pubsub \
    google-cloud-logging \
    google-cloud-kms \
    google-genai \
    vertexai \
    tensorflow \
    torch \
    scikit-learn \
    pandas \
    numpy \
    jupyterlab \
    pytest
