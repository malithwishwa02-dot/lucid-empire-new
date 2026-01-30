# ==============================================================================
# LUCID EMPIRE :: CONTAINERIZED UNIT
# AUTHORITY: Dva.12
# BASE: Ubuntu 24.04 (Noble Numbat) - Matching 'Upgrade Plan' Docs
# ==============================================================================

FROM ubuntu:24.04

# PREVENT INTERACTIVE PROMPTS DURING INSTALL
ENV DEBIAN_FRONTEND=noninteractive

# 1. SYSTEM LAYER & FONT HYGIENE
# Install dependencies, Xvfb, and Microsoft Fonts in a single layer to reduce image size.
RUN apt-get update && \
    echo "ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true" | debconf-set-selections && \
    apt-get install -y \
    python3 python3-pip python3-venv \
    libgtk-3-0 libasound2 libdbus-glib-1-2 \
    libx11-xcb1 libxt6 libgbm1 libdrm2 \
    libfreetype6 fontconfig \
    xvfb ttf-mscorefonts-installer \
    curl unzip tini && \
    # Clean up apt cache to keep image small
    rm -rf /var/lib/apt/lists/* && \
    # Rebuild font cache
    fc-cache -f -v

# 2. USER SECURITY (NON-ROOT)
# Running browsers as root creates detectable sandbox violations.
RUN useradd -m -s /bin/bash camoufox_user

# 3. WORKSPACE PREP
WORKDIR /home/camoufox_user/app
COPY . .

# Adjust permissions for the non-root user
RUN chown -R camoufox_user:camoufox_user /home/camoufox_user/app

# Switch to Operator User
USER camoufox_user

# 4. APPLICATION LAYER
# Create Venv and Install Lucid Engine
RUN python3 -m venv lucid_env && \
    . lucid_env/bin/activate && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir "camoufox[geoip]" browserforge playwright

# 5. BINARY FETCH
# Fetch the patched browser binary during build time
RUN . lucid_env/bin/activate && \
    python3 -m camoufox fetch

# 6. EXECUTION ENTRYPOINT
# Tini is required to reap zombie processes in Docker
ENTRYPOINT ["/usr/bin/tini", "--"]

# Default Command: Activate venv and run main.py
CMD ["/bin/bash", "-c", ". lucid_env/bin/activate && python3 main.py"]