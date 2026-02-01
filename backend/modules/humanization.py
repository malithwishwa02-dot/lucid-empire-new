# LUCID EMPIRE :: HUMANIZATION ENGINE
# Purpose: Add human-like movement and behavior patterns

import asyncio
import random
import math

class HumanizationEngine:
    """Generate realistic human-like interactions"""
    
    @staticmethod
    async def human_mouse_move(page, start_x, start_y, end_x, end_y, duration=1.0):
        """Move mouse in a curved, human-like path"""
        steps = int(duration * 100)  # 100 steps per second
        
        for i in range(steps):
            t = i / steps
            # Easing function for natural movement
            eased_t = t * t * (3 - 2 * t)  # smoothstep
            
            current_x = start_x + (end_x - start_x) * eased_t
            current_y = start_y + (end_y - start_y) * eased_t
            
            # Add subtle jitter
            jitter_x = random.gauss(0, 2)
            jitter_y = random.gauss(0, 2)
            
            await page.mouse.move(
                current_x + jitter_x,
                current_y + jitter_y
            )
            await asyncio.sleep(0.01)
    
    @staticmethod
    async def scroll_naturally(page, distance=1000, duration=5.0):
        """Scroll page with natural deceleration"""
        steps = int(duration * 30)  # 30 steps per second
        
        for i in range(steps):
            progress = i / steps
            # Easing out for natural deceleration
            eased = 1 - (1 - progress) ** 3
            scroll_amount = distance * eased
            
            await page.evaluate(f"window.scrollBy(0, {int(scroll_amount)});")
            await asyncio.sleep(1/30)
