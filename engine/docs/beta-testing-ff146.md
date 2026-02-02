# Testing Firefox 146 Beta

This guide explains how to test the experimental Firefox 146 build of Lucid Empire.

> **Note:** The FF146 build is experimental and may contain bugs. For a stable production version, use branch `releases/135`.

## Build from Source

1. Clone the repository:
```bash
git clone --depth 1 https://github.com/daijro/lucid_browser
cd lucid_browser
```

2. Set up the build environment:
```bash
make dir
make bootstrap   # only needed once
```

3. Build for your target platform:
```bash
python3 multibuild.py --target <os> --arch <arch>
```

| Parameter | Options |
|-----------|---------|
| `--target` | `linux`, `windows`, `macos` |
| `--arch` | `x86_64`, `arm64`, `i686` |

Build artifacts will appear in the `dist/` folder.

### Default Install Directories

When using the Python library (`lucid_browser fetch`), the default install directory is:

| OS | Install Directory |
|------|-------------------|
| **Linux** | `~/.cache/lucid_browser/` |
| **macOS** | `~/Library/Caches/lucid_browser/` |
| **Windows** | `C:\Users\<user>\AppData\Local\lucid_browser\lucid_browser\Cache\` |

## Replacing the Binary

To test FF146 with an existing Lucid Empire installation:

1. Build from source using the instructions above
2. Extract the built zip from `dist/`
3. Replace the binary at the corresponding path for your OS:

**Linux:**
```bash
cp /path/to/built/lucid_browser-bin ~/.cache/lucid_browser/lucid_browser-bin
```

**macOS:**
```bash
cp /path/to/built/Lucid Empire.app ~/Library/Caches/lucid_browser/Lucid Empire.app
```

**Windows:**
```powershell
copy C:\path\to\built\lucid_browser.exe C:\Users\<user>\AppData\Local\lucid_browser\lucid_browser\Cache\lucid_browser.exe
```
