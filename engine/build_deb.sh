#!/bin/bash

# Build the application with PyInstaller
pyinstaller --onedir --add-binary "libs/libfaketime.so.1:." --add-data "assets:assets" --name lucid-empire dashboard/main.py

# Create the Debian package structure
mkdir -p lucid-empire/opt/lucid-empire
mkdir -p lucid-empire/usr/bin
mkdir -p lucid-empire/usr/share/applications

# Copy the PyInstaller output
cp -r dist/lucid-empire/* lucid-empire/opt/lucid-empire/

# Create a launcher script
echo '#!/bin/bash
cd /opt/lucid-empire
./lucid-empire' > lucid-empire/usr/bin/lucid
chmod +x lucid-empire/usr/bin/lucid

# Create a desktop entry
cat <<EOF > lucid-empire/usr/share/applications/lucid.desktop
[Desktop Entry]
Name=Lucid Empire
Exec=lucid
Icon=/opt/lucid-empire/icon.png
Type=Application
Categories=Utility;
EOF

# Create the control file
mkdir -p lucid-empire/DEBIAN
cat <<EOF > lucid-empire/DEBIAN/control
Package: lucid-empire-suite
Version: 1.0.0
Architecture: amd64
Maintainer: Prometheus-Core
Description: Sovereign Anti-Detect Suite with Time-Warping Capabilities
Depends: libgconf-2-4, libappindicator1
EOF

# Build the package
dpkg-deb --build lucid-empire
