# Claude Utils Container
# Purpose: Run Claude commands and utilities for various automation tasks
FROM python:3.11-slim

# Set working directory
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # Audio support
    alsa-utils \
    pulseaudio \
    libsdl2-mixer-2.0-0 \
    # Common utilities
    curl \
    git \
    vim \
    nano \
    jq \
    wget \
    # Build tools for Python packages
    gcc \
    g++ \
    make \
    # Cleanup
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY claude-requirements.txt /workspace/

# Install Python packages from requirements
RUN pip install --no-cache-dir -r /workspace/claude-requirements.txt

# Create a non-root user
RUN useradd -m -s /bin/bash claude && \
    chown -R claude:claude /workspace

# Switch to non-root user
USER claude

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Default command - keep container running
CMD ["tail", "-f", "/dev/null"]
