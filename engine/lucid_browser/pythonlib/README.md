<div align="center">

# Lucid Empire Python Interface

#### Lightweight wrapper around the Playwright API to help launch Lucid Empire.

</div>

> [!NOTE]
> All the the latest documentation is avaliable [here](https://lucid_browser.com/python).

---

## What is this?

This Python library wraps around Playwright's API to help automatically generate & inject unique device characteristics (OS, CPU info, navigator, fonts, headers, screen dimensions, viewport size, WebGL, addons, etc.) into Lucid Empire.

It uses [BrowserForge](https://github.com/daijro/browserforge) under the hood to generate fingerprints that mimic the statistical distribution of device characteristics in real-world traffic.

In addition, it will also calculate your target geolocation, timezone, and locale to avoid proxy protection ([see demo](https://i.imgur.com/UhSHfaV.png)).

---

## Installation

First, install the `lucid_browser` package:

```bash
pip install -U lucid_browser[geoip]
```

The `geoip` parameter is optional, but heavily recommended if you are using proxies. It will download an extra dataset to determine the user's longitude, latitude, timezone, country, & locale.

Next, download the Lucid Empire browser:

**Windows**

```bash
lucid_browser fetch
```

**MacOS & Linux**

```bash
python3 -m lucid_browser fetch
```

To uninstall, run `lucid_browser remove`.

<details>
<summary>CLI options</summary>

```
Usage: python -m lucid_browser [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  fetch    Fetch the latest version of Lucid Empire
  path     Display the path to the Lucid Empire executable
  remove   Remove all downloaded files
  server   Launch a Playwright server
  test     Open the Playwright inspector
  version  Display the current version
```

</details>

<hr width=50>

## Usage

All of the latest documentation is avaliable at [lucid_browser.com/python](https://lucid_browser.com/python).
