# docker run -it claude-code /bin/bash
FROM node:20-bookworm

# Install essential development tools
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    sudo \
    vim \
    ripgrep \
    jq \
    python3 \
    python3-pip \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user with a different UID
RUN useradd -m -s /bin/bash -u 1001 claude && \
    echo "claude ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Install Claude Code globally
RUN npm install -g @anthropic-ai/claude-code

# Optional: Install additional Node.js tools
RUN npm install -g typescript ts-node

# Optional: Install Python tools
RUN pip3 install --break-system-packages \
    black \
    pylint \
    pytest

# Create workspace directory
RUN mkdir -p /workspace && chown claude:claude /workspace

# Switch to non-root user
USER claude
WORKDIR /workspace

# Create Claude config directory
RUN mkdir -p /home/claude/.claude

ARG CONFIG_DIR=~/.claude

# Copy Claude configuration files
COPY --chown=claude:claude claude/global/claude.json /home/claude/.claude.json
COPY --chown=claude:claude settings.json /home/claude/.claude/settings.json

# Set environment variables
ENV HOME=/home/claude \
    PATH="/home/claude/.local/bin:${PATH}"

# Default command
CMD ["claude"]