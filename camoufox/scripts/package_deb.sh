#!/usr/bin/env bash
set -euo pipefail

# Simple .deb packager for Lucid Empire
# Usage: ./package_deb.sh [output-version]

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PACKAGE_NAME="${PACKAGE_NAME:-lucid-empire}"

# Version: prefer argument, then PACKAGE_VERSION env, then git describe, else default
if [ -n "${1:-}" ]; then
  VERSION="$1"
elif [ -n "${PACKAGE_VERSION:-}" ]; then
  VERSION="$PACKAGE_VERSION"
else
  if command -v git >/dev/null 2>&1 && [ -d "$ROOT_DIR/.git" ]; then
    VERSION=$(git -C "$ROOT_DIR" describe --tags --always --dirty 2>/dev/null || true)
    VERSION="${VERSION:-0.1.0~dev}"
  else
    VERSION="0.1.0~dev"
  fi
fi

ARCH="${ARCH:-amd64}"
STAGING_DIR="$(mktemp -d)"
DIST_DIR="$ROOT_DIR/dist"

# Maintainer: allow override via env, else use git config or fallback
if [ -n "${PACKAGE_MAINTAINER:-}" ]; then
  MAINTAINER="$PACKAGE_MAINTAINER"
else
  name=$(git -C "$ROOT_DIR" config user.name 2>/dev/null || true)
  email=$(git -C "$ROOT_DIR" config user.email 2>/dev/null || true)
  if [ -n "$name" ] && [ -n "$email" ]; then
    MAINTAINER="$name <$email>"
  else
    MAINTAINER="Your Name <you@example.com>"
  fi
fi

echo "[INFO] Building $PACKAGE_NAME version $VERSION ($ARCH)"
mkdir -p "$DIST_DIR"

# Install paths
OPT_DIR="$STAGING_DIR/opt/$PACKAGE_NAME"
USR_BIN_DIR="$STAGING_DIR/usr/bin"
DESKTOP_DIR="$STAGING_DIR/usr/share/applications"
ICON_DIR="$STAGING_DIR/usr/share/icons/hicolor/256x256/apps"
DEBIAN_DIR="$STAGING_DIR/DEBIAN"

mkdir -p "$OPT_DIR" "$USR_BIN_DIR" "$DESKTOP_DIR" "$ICON_DIR" "$DEBIAN_DIR"

# Files and directories to include (best-effort)
INCLUDES=(
  "lucid_commander.py"
  "lucid_launcher.py"
  "start_lucid.sh"
  "LUCID_V5_MANUAL.md"
  "gui_requirements.txt"
  "bin"
  "settings"
  "scripts"
  "core"
  "modules"
  "pythonlib"
  "assets"
  "additions"
  "start_lucid.sh"
  "Makefile"
  "pack_lucid.py"
)

cd "$ROOT_DIR"
for item in "${INCLUDES[@]}"; do
  if [ -e "$item" ]; then
    echo "[INFO] Including $item"
    rsync -a --exclude '.git' --exclude 'dist' "$item" "$OPT_DIR/"
  fi
done

# If branding icon exists, copy it
ICON_SRC="${ROOT_DIR}/camoufox/lucid_browser/additions/browser/branding/lucid_browser/logo.png"
if [ -f "$ICON_SRC" ]; then
  cp "$ICON_SRC" "$ICON_DIR/lucid-empire.png"
elif [ -f "${ROOT_DIR}/camoufox/additions/browser/branding/camoufox/logo.png" ]; then
  cp "${ROOT_DIR}/camoufox/additions/browser/branding/camoufox/logo.png" "$ICON_DIR/lucid-empire.png"
else
  echo "[WARN] No branding icon found; desktop icon will be missing"
fi

# Create wrapper executable
cat > "$USR_BIN_DIR/lucid-empire" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
OPT="/opt/lucid-empire"
# Prefer GUI if available
if [ -f "$OPT/lucid_commander.py" ]; then
  exec python3 "$OPT/lucid_commander.py" "$@"
elif [ -x "$OPT/start_lucid.sh" ]; then
  exec "$OPT/start_lucid.sh" "$@"
else
  echo "Lucid Empire not found in /opt/lucid-empire" >&2
  exit 2
fi
EOF
chmod 0755 "$USR_BIN_DIR/lucid-empire"

# Desktop file (fallback) - will be overwritten if provided in packaging
cat > "$DESKTOP_DIR/lucid-empire.desktop" <<'EOF'
[Desktop Entry]
Name=Lucid Empire
Comment=Lucid anti-detect browser
Exec=/usr/bin/lucid-empire %u
Icon=lucid-empire
Terminal=false
Type=Application
Categories=Network;WebBrowser;
StartupWMClass=Lucid Empire
EOF

# DEBIAN control
cat > "$DEBIAN_DIR/control" <<EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: web
Priority: optional
Architecture: $ARCH
Depends: python3 (>= 3.8), python3-venv
Maintainer: $MAINTAINER
License: MPL-2.0
Description: Lucid Empire - anti-detect web browser (packaged)
 This package installs the Lucid Empire bundle into /opt/$PACKAGE_NAME
 and provides a /usr/bin/lucid-empire launcher. For GUI features, install
 the Python GUI deps listed in gui_requirements.txt or run the optional
 setup (see /usr/share/doc/$PACKAGE_NAME/README.Debian).
EOF

# Optional postinst: create venv if requested via env flag or via /etc/default file
cat > "$DEBIAN_DIR/postinst" <<'EOF'
#!/usr/bin/env bash
set -e
# If /etc/default/lucid-empire-install exists and contains INSTALL_REQUIREMENTS=1,
# or if INSTALL_REQUIREMENTS=1 env is set during install, install GUI deps.
INSTALL_FLAG="${INSTALL_REQUIREMENTS:-0}"
if [ -f /etc/default/lucid-empire-install ]; then
  . /etc/default/lucid-empire-install || true
  INSTALL_FLAG="${INSTALL_FLAG:-${INSTALL_REQUIREMENTS:-0}}"
fi
if [ "$INSTALL_FLAG" = "1" ]; then
  py=/usr/bin/python3
  if [ -x "$py" ]; then
    $py -m venv /opt/$PACKAGE_NAME/venv || true
    # shellcheck disable=SC1091
    source /opt/$PACKAGE_NAME/venv/bin/activate
    if [ -f /opt/$PACKAGE_NAME/gui_requirements.txt ]; then
      pip install --upgrade pip
      pip install -r /opt/$PACKAGE_NAME/gui_requirements.txt || true
    fi
  fi
fi
# Update desktop database
if [ -x /usr/bin/update-desktop-database ]; then
  update-desktop-database || true
fi
exit 0
EOF
chmod 0755 "$DEBIAN_DIR/postinst"

# Add simple README.Debian and include license/copyright
mkdir -p "$STAGING_DIR/usr/share/doc/$PACKAGE_NAME"
cat > "$STAGING_DIR/usr/share/doc/$PACKAGE_NAME/README.Debian" <<'EOF'
Lucid Empire packaged for Debian/Ubuntu.

To enable GUI features, create a venv and install the GUI requirements:
  python3 -m venv /opt/lucid-empire/venv
  source /opt/lucid-empire/venv/bin/activate
  pip install -r /opt/lucid-empire/gui_requirements.txt

Note: Redistribution of Firefox binaries may require separate handling.
EOF

# Copy LICENSE files into documentation
for l in "$ROOT_DIR"/LICENSE "$ROOT_DIR"/camoufox/LICENSE "$ROOT_DIR"/camoufox/lucid_browser/LICENSE; do
  if [ -f "$l" ]; then
    cp "$l" "$STAGING_DIR/usr/share/doc/$PACKAGE_NAME/"
  fi
done

# Create a minimal copyright file
cat > "$STAGING_DIR/usr/share/doc/$PACKAGE_NAME/copyright" <<'EOF'
Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
Upstream-Name: Lucid Empire
Source: https://github.com/${GITHUB_REPO:-your/repo}

Files: *
Copyright: See individual files
License: MPL-2.0

EOF

# Set permissions where needed
chmod -R 0755 "$OPT_DIR" || true

# Build the package
PKG_FILE="$DIST_DIR/${PACKAGE_NAME}_${VERSION}_${ARCH}.deb"
rm -f "$PKG_FILE"
fakeroot dpkg-deb --build "$STAGING_DIR" "$PKG_FILE"

echo "[OK] Package created: $PKG_FILE"

# Cleanup
rm -rf "$STAGING_DIR"

exit 0
