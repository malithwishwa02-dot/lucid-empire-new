#!/bin/bash
# LUCID EMPIRE v5: LOCAL BUILDER
# AUTHORITY: Dva.12

echo ">>> INITIATING OBLIVION BUILD SEQUENCE..."

# 1. CLEANUP
rm -rf build dist
mkdir -p dist/lucid-empire/usr/lib/lucid-empire

# 2. COMPILE NETWORK SHIELD
echo "[*] Compiling XDP Shield..."
if command -v clang &> /dev/null; then
    clang -O2 -target bpf -c network/xdp_outbound.c -o dist/lucid-empire/usr/lib/lucid-empire/xdp_outbound.o
else
    echo "[!] Clang not found. Shield will be inactive."
fi

# 3. BUILD BACKEND
echo "[*] Freezing Python Core..."
# Check for pyinstaller, install if missing
if ! command -v pyinstaller &> /dev/null; then
    pip install pyinstaller
fi
pyinstaller --noconfirm --clean --onefile --distpath dist/lucid-empire/usr/lib/lucid-empire --name "lucid-core" lucid_api.py

# 4. PREPARE ASSETS
echo "[*] Copying Assets..."
cp -r lucid_profile_data dist/lucid-empire/usr/lib/lucid-empire/
cp -r assets dist/lucid-empire/usr/lib/lucid-empire/

# 5. GENERATE LAUNCHER
echo "[*] Creating Launcher..."
cat <<EOF > dist/lucid-empire/usr/bin/lucid-commander
#!/bin/bash
cd /usr/lib/lucid-empire
./lucid-core &
# Assume GUI is separate or integrated here
echo "Lucid Empire Started on port 13337"
EOF
chmod +x dist/lucid-empire/usr/bin/lucid-commander

echo ">>> BUILD COMPLETE. Artifacts in dist/lucid-empire"
echo "To package: dpkg-deb --build dist/lucid-empire"
