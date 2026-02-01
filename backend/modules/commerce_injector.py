# LUCID EMPIRE :: COMMERCE INJECTOR
# Purpose: Injects localStorage artifacts and dispatches StorageEvents

import asyncio
import random

class CommerceInjector:
    def __init__(self, humanizer=None):
        self.humanizer = humanizer

    async def random_sleep(self, min_s=0.5, max_s=2.0):
        await asyncio.sleep(random.uniform(min_s, max_s))

    async def inject_trust_anchors(self, page, key, value):
        """Inject a trust anchor (key-value pair) into localStorage and dispatch a storage event"""
        # Tap 1: Write the data
        await page.evaluate(
            f"""
            localStorage.setItem('{key}', '{value}');
            """
        )

        # Tap 2: Fabricate and dispatch the StorageEvent
        await page.evaluate(
            f"""
            const event = new StorageEvent('storage', {{
                key: '{key}',
                newValue: '{value}',
                url: window.location.href
            }});
            window.dispatchEvent(event);
            """
        )
        
        await self.random_sleep()

    async def inject_commerce_signals(self, page):
        """Inject realistic commerce-related localStorage signals"""
        signals = {
            '_ga': 'GA1.2.123456789.1234567890',
            'checkout_flow': 'initiated',
            'cart_items': '3',
            'last_view': 'product_page'
        }
        
        for key, value in signals.items():
            await self.inject_trust_anchors(page, key, value)

    async def cleanup(self, page):
        """Clean up injected artifacts"""
        await page.evaluate("localStorage.clear();")
