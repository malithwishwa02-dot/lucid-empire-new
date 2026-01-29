# LUCID EMPIRE :: COMMERCE INJECTOR
# Purpose: Injects localStorage artifacts AND dispatches StorageEvents.

import asyncio

async def inject_trust_anchors(page, platform="shopify"):
    print(f" [*] Injecting Commerce Vector: {platform.upper()}")
    
    # The Double-Tap Script
    # 1. Writes to LocalStorage
    # 2. Dispatches a StorageEvent to wake up fraud listeners
    script = """
    (args) => {
        const [key, value] = args;
        
        // Tap 1: Write the data
        window.localStorage.setItem(key, value);
        
        // Tap 2: Dispatch the Event
        const event = new StorageEvent('storage', {
            key: key, 
            newValue: value,
            url: window.location.href, 
            storageArea: window.localStorage,
            bubbles: true, 
            cancelable: false
        });
        
        // 3. Active Dispatch
        window.dispatchEvent(event);
    }
    """
    
    if platform == "shopify":
        # Simulate a completed checkout token from 30 days ago
        token = "c1234567-89ab-cdef-0123-4567890abcdef"
        await page.evaluate(script, ["checkout_token", token])
        await page.evaluate(script, ["shopify_pay_redirect_cookie", "true"])
        # 'completed' flag often checked by analytics
        await page.evaluate(script, ["completed", "true"])
        
    elif platform == "stripe":
        # Inject Stripe device identifiers (Plan 6.3)
        # MUID is typically a GUID structure
        fake_muid = "c6b9d635-20de-4fc6-8995-5d5b2d165881"
        await page.evaluate(script, ["muid", fake_muid])
        await page.evaluate(script, ["stripe_device_id", fake_muid])
        await page.evaluate(script, ["__stripe_mid", "mid_" + fake_muid])
        
        # Cookie Injection for session persistence
        # Note: Cookies must be set via browser context for HttpOnly support, 
        # but client-side cookies can be set via JS for tracker detection.
        await page.evaluate(f"""
            document.cookie = "_stripe_sid={fake_muid}; path=/; domain=.stripe.com; max-age=31536000";
            document.cookie = "__stripe_mid=mid_{fake_muid}; path=/; domain=.stripe.com; max-age=31536000";
        """)

    elif platform == "adyen":
        # Plan 6.3: Adyen 3D Secure 2.0 frictionless artifacts
        fake_fingerprint = "adyen_fp_550e8400-e29b-41d4-a716-446655440000"
        await page.evaluate(script, ["fingerprint", fake_fingerprint])
        await page.evaluate(script, ["dfValue", "1_001" + fake_fingerprint])
        
    print(f" [V] {platform.upper()} Artifacts Injected via Double-Tap.")
