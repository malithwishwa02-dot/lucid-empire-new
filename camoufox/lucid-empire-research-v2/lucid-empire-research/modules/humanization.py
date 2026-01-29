# LUCID EMPIRE :: HUMANIZATION MODULE
# Purpose: Provides human-like interaction primitives for the Genesis Engine.

import asyncio
import random
import math

async def human_scroll(page):
    """
    Simulates human-like scrolling behavior with variable speed and pauses.
    """
    try:
        # Get page height
        height = await page.evaluate("document.body.scrollHeight")
        viewport_height = await page.evaluate("window.innerHeight")
        current_scroll = 0
        
        while current_scroll < height:
            # Random scroll distance between 100 and viewport height
            scroll_step = random.randint(100, int(viewport_height * 0.8))
            current_scroll += scroll_step
            
            # Smooth scroll to position
            await page.evaluate(f"window.scrollTo({{top: {current_scroll}, behavior: 'smooth'}})")
            
            # Random pause to simulate reading
            await asyncio.sleep(random.uniform(0.5, 2.0))
            
            # Occasionally scroll back up a bit (reading previous paragraph)
            if random.random() < 0.2:
                back_scroll = random.randint(50, 200)
                current_scroll -= back_scroll
                await page.evaluate(f"window.scrollTo({{top: {current_scroll}, behavior: 'smooth'}})")
                await asyncio.sleep(random.uniform(0.5, 1.5))
                
            # Break if we've reached the bottom
            if current_scroll >= height:
                break
                
    except Exception as e:
        print(f" [!] Human scroll error: {e}")

async def human_mouse_move(page):
    """
    Simulates human-like mouse movement using a Bezier curve path.
    """
    try:
        # Get viewport dimensions
        viewport = await page.viewport_size()
        if not viewport:
            width, height = 1920, 1080
        else:
            width, height = viewport['width'], viewport['height']
            
        # Start from random position
        start_x = random.randint(0, width)
        start_y = random.randint(0, height)
        
        # End at random position
        end_x = random.randint(0, width)
        end_y = random.randint(0, height)
        
        # Move mouse
        await page.mouse.move(start_x, start_y)
        steps = random.randint(20, 50)
        
        # Simple linear interpolation with noise for now
        # A full Bezier implementation would be better but this suffices for "human-like" 
        # enough to trigger simple activity monitors.
        for i in range(steps):
            t = i / steps
            # Add some sine wave noise
            noise_x = math.sin(t * math.pi) * random.randint(-20, 20)
            noise_y = math.cos(t * math.pi) * random.randint(-20, 20)
            
            curr_x = start_x + (end_x - start_x) * t + noise_x
            curr_y = start_y + (end_y - start_y) * t + noise_y
            
            await page.mouse.move(curr_x, curr_y)
            await asyncio.sleep(random.uniform(0.01, 0.05))
            
    except Exception as e:
        print(f" [!] Human mouse move error: {e}")
