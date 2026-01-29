#!/bin/bash
# LUCID EMPIRE :: FONT HARMONIZATION SCRIPT
# Purpose: Physically installs Microsoft TrueType Core Fonts to ensure rendering consistency.

echo " [!] INITIALIZING FONT HARMONIZATION..."

# Ensure we are running as root/sudo
if [ "$EUID" -ne 0 ]; then 
  echo "Please run as root"
  exit
fi

# 1. Add Contrib and Non-Free repositories (Debian/Ubuntu specific)
echo " [*] Updating package lists and adding MS font installer..."
apt-get update
apt-get install -y debconf-utils

# 2. Automate the EULA acceptance for ttf-mscorefonts-installer
echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | debconf-set-selections

# 3. Install the fonts
apt-get install -y ttf-mscorefonts-installer

# 4. Refresh font cache
echo " [*] Refreshing system font cache..."
fc-cache -fv

# 5. Verify installation
echo " [*] Verifying font installation..."
fc-list | grep -i "Arial"
fc-list | grep -i "Times New Roman"

echo " [V] FONT HARMONIZATION COMPLETE. Physical state aligns with Application state."
