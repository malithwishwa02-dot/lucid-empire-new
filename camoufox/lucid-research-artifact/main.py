import asyncio
from camoufox import AsyncNewContext

LUCID_CONFIG = {
    "headless": "virtual",
    "os": ["windows", "macos"],
    "config": {
        "browser.theme.content-theme": 0,
        "browser.cache.memory.enable": False,
        "javascript.options.mem.gc_frequency": 10,
        "media.peerconnection.enabled": False,
    },
    "humanize": True,
    "geoip": True,
}

async def run_selftest():
    try:
        async with AsyncNewContext(**LUCID_CONFIG) as context:
            page = await context.new_page()
            await page.goto('https://abrahamjuliot.github.io/creepjs/')
            await page.screenshot(path='lucid_verification.png')
            print('SCREENSHOT_SAVED: lucid_verification.png')
            return True
    except Exception as e:
        print('SELFTEST_FAILED:', e)
        return False

if __name__ == '__main__':
    import sys
    ok = asyncio.run(run_selftest())
    if not ok:
        sys.exit(1)
