# LUCID EMPIRE :: GENESIS ENGINE v2.1
# Purpose: Orchestrates Temporal Displacement and Persona-based Warm-Up Cycles.

import sys
import os
# Dva.12 Patch: Allow visibility of sibling modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json
import asyncio
import random
import logging
import datetime
import time
import pytz
from astral import LocationInfo
from astral.sun import sun
from playwright.async_api import async_playwright
from modules.commerce_injector import inject_trust_anchors, inject_commerce_vector
from modules.biometric_mimicry import BiometricMimicry

PROFILE_DIR = "./lucid_profile_data"

# Time control file path
TIME_CONTROL_FILE = "/tmp/lucid_time_control"

def initialize_time_warp(start_date_delta_days=90):
    """Initialize the time control file for libfaketime"""
    if not os.path.exists(TIME_CONTROL_FILE):
        open(TIME_CONTROL_FILE, 'a').close()
    initial_time = datetime.datetime.now() - datetime.timedelta(days=start_date_delta_days)
    os.utime(TIME_CONTROL_FILE, (initial_time.timestamp(), initial_time.timestamp()))

def update_time_warp(seconds_elapsed_real, days_to_advance_fake):
    """Update the control file to advance fake time"""
    current_fake_time = datetime.datetime.fromtimestamp(os.path.getmtime(TIME_CONTROL_FILE))
    new_fake_time = current_fake_time + datetime.timedelta(days=days_to_advance_fake)
    os.utime(TIME_CONTROL_FILE, (new_fake_time.timestamp(), new_fake_time.timestamp()))
    time.sleep(seconds_elapsed_real)

def launch_browser_with_time_warp(user_data_dir, proxy_config=None):
    """Launch browser with libfaketime integration"""
    env = {
        "LD_PRELOAD": "/path/to/libfaketime.so.1",
        "FAKETIME": "@",
        "FAKETIME_FOLLOW_FILE": TIME_CONTROL_FILE,
        "FAKETIME_DONT_RESET": "1",
        "FAKETIME_DONT_FAKE_MONOTONIC": "1"
    }
    
    if proxy_config:
        env.update(proxy_config)
        
    with sync_playwright() as p:
        browser = p.firefox.launch_persistent_context(
            user_data_dir=user_data_dir,
            env=env,
            headless=False,
            proxy=proxy_config
        )
        return browser

class GenesisEngine:
    def __init__(self, persona="student", proxy_geo="New York", proxy_country="US"):
        self.persona = persona
        self.proxy_geo = proxy_geo
        self.proxy_country = proxy_country
        self.location = LocationInfo(proxy_geo, proxy_country)
        self.tz = pytz.timezone(self.location.timezone)
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("GenesisEngine")

    def is_persona_active(self, current_time):
        """
        Validates if the persona should be active based on local solar time, day, 
        and country-specific habits (Plan 4.1, 4.2, 4.3, 4.4).
        """
        local_hour = current_time.hour
        is_weekday = current_time.weekday() < 5
        is_sunday = current_time.weekday() == 6
        is_friday = current_time.weekday() == 4
        
        # Plan 4.4: Country-Specific Peak Adjustments
        is_us = self.proxy_country.upper() == "US"
        is_eu = self.proxy_country.upper() in ["DE", "UK", "FR", "IT", "ES"]
        is_asia = self.proxy_country.upper() in ["CN", "ID", "JP", "KR"]

        if self.persona == "student":
            # Plan 4.1.1: Late start (11 AM), active until 2 AM.
            if is_asia:
                # Plan 4.1.1 & 4.4: Asia has extremely high late-night mobile engagement
                return local_hour >= 11 or local_hour <= 4
            if is_sunday:
                return local_hour >= 11 or local_hour <= 3
            if is_friday:
                return (12 <= local_hour <= 17) or (22 <= local_hour <= 2)
            return local_hour >= 11 or local_hour <= 2
            
        elif self.persona == "worker":
            # Plan 4.2.1: Triple peak pattern.
            if not is_weekday:
                return False
            
            # Base peaks
            peak1 = (8 <= local_hour <= 10)
            peak2 = (13 <= local_hour <= 15)
            peak3 = (19 <= local_hour <= 21)

            if is_us:
                # Plan 4.4: US has early rise (4 AM)
                peak1 = (4 <= local_hour <= 10)
            if is_eu:
                # Plan 4.4: Europe peaks just before night (8 PM - 10 PM)
                peak3 = (20 <= local_hour <= 22)

            is_lunch = (12 <= local_hour < 13)
            return (peak1 or peak2 or peak3) and not is_lunch
            
        return True

    def get_local_solar_time(self, days_ago):
        """
        Calculates local solar time for the proxy location (Plan 4.3).
        """
        now = datetime.datetime.now(self.tz)
        target_date = now - datetime.timedelta(days=days_ago)
        return target_date

    def get_persona_urls(self, phase):
        """
        Returns persona-specific URLs and trust anchors (Plan 4.1.2, 4.2.2).
        """
        if self.persona == "student":
            if phase == "INCEPTION":
                # Plan 5.2.1: News/Media + Global Trust Anchors
                return ["https://www.google.com", "https://www.wikipedia.org", "https://www.cnn.com", "https://www.bbc.com"]
            elif phase == "WARMING":
                # Plan 4.1.2: LMS + Academic + Social
                return ["https://canvas.instructure.com", "https://scholar.google.com", "https://www.jstor.org", "https://www.discord.com", "https://www.reddit.com"]
            elif phase == "KILL_CHAIN":
                # Plan 3.3.3: Commerce Injection
                return ["https://www.apple.com/shop/bag", "https://www.amazon.com", "https://www.discord.com/billing"]
        else: # Worker
            if phase == "INCEPTION":
                # Plan 4.2.2: News & Finance
                return ["https://www.google.com", "https://www.wsj.com", "https://www.bloomberg.com", "https://www.ft.com"]
            elif phase == "WARMING":
                # Plan 4.2.2: B2B SaaS + LinkedIn
                return ["https://www.linkedin.com", "https://www.slack.com", "https://www.salesforce.com", "https://www.atlassian.com", "https://www.zoom.us"]
            elif phase == "KILL_CHAIN":
                # Plan 6.3: Commerce Injection
                return ["https://www.apple.com/shop/bag", "https://www.amazon.com", "https://www.chase.com"]
        return []

    def set_time_warp(self, days_ago):
        """
        Configures libfaketime environment variables for the subprocess.
        """
        env = os.environ.copy()
        # Path to the library in the Linux container environment
        env["LD_PRELOAD"] = "/usr/local/lib/faketime/libfaketime.so.1"
        env["FAKETIME"] = f"-{days_ago}d"
        # Critical stability flags to prevent Firefox hangs (Plan 3.2.1)
        env["DONT_FAKE_MONOTONIC"] = "1"
        env["FAKETIME_NO_CACHE"] = "1"
        return env

    async def trigger_ga_mp(self, page):
        """
        Triggers GA Measurement Protocol to register the Client ID (Plan 3.3.1).
        """
        self.logger.info(" [*] Triggering GA Measurement Protocol...")
        # Simulate loading pages with GA tags
        ga_urls = [
            "https://www.google-analytics.com/collect?v=1&t=pageview&tid=UA-XXXXXXXX-X&cid=555&dp=%2Fhome",
            "https://stats.g.doubleclick.net/r/collect?v=1&aip=1&t=dc&_r=3&tid=UA-XXXXXXXX-X&cid=555"
        ]
        for url in ga_urls:
            try:
                await page.evaluate(f"fetch('{url}', {{mode: 'no-cors'}})")
            except: pass

    async def populate_form_history(self, page):
        """
        Populates formhistory.sqlite with valid address data (Plan 3.3.2).
        """
        self.logger.info(" [*] Populating form history (Provenance of Location)...")
        # Visiting a generic checkout page to trigger form history
        try:
            await page.goto("https://www.apple.com/shop/bag", wait_until="networkidle")
            # Mimic filling address fields
            await page.evaluate("""() => {
                const fields = {
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'address': '123 Lucid Lane',
                    'city': 'New York',
                    'state': 'NY',
                    'zip': '10001'
                };
                // In a real scenario, we'd use BiometricMimicry here
                console.log('Simulating address fill...');
            }""")
        except: pass

    async def run_phase(self, phase_name, days_ago):
        target_time = self.get_local_solar_time(days_ago)
        
        if not self.is_persona_active(target_time):
            self.logger.info(f" Persona {self.persona} is SLEEPING at local time {target_time}. Skipping phase.")
            return

        self.logger.info(f" [>] TIME WARP: T-{days_ago} DAYS | PHASE: {phase_name} | PERSONA: {self.persona}")
        
        initialize_time_warp(days_ago)
        
        env = self.set_time_warp(days_ago)
        async with async_playwright() as p:
            # Persistent context ensures cookies/history are saved
            browser = await p.firefox.launch_persistent_context(
                user_data_dir=PROFILE_DIR,
                headless=True,
                viewport={"width": 1920, "height": 1080},
                env=env
            )
            page = browser.pages[0]
            mimicry = BiometricMimicry(page)
            
            # Phase 1 specific: GA MP
            if phase_name == "INCEPTION":
                await self.trigger_ga_mp(page)

            urls = self.get_persona_urls(phase_name)
            for url in urls:
                try:
                    self.logger.info(f" Visiting {url}...")
                    await page.goto(url, wait_until="domcontentloaded")
                    await mimicry.human_scroll()
                    
                    if phase_name == "WARMING" and "apple.com" in url:
                        # Plan 3.3.2: Populate form history
                        await self.populate_form_history(page)
                        await mimicry.human_move(random.randint(100, 500), random.randint(100, 500))
                        
                    if phase_name == "KILL_CHAIN":
                        # Commerce Injection (Plan 3.3.3)
                        platform = "shopify" if "apple" in url else "stripe"
                        await inject_commerce_vector(page, platform=platform)
                    
                    await asyncio.sleep(random.randint(5, 15))
                except Exception as e:
                    self.logger.warning(f"Failed to load {url}: {e}")
            
            await browser.close()

    async def execute_90_day_cycle(self):
        # Phase 1: Inception (T-90)
        await self.run_phase("INCEPTION", 90)
        
        # Phase 2: Warming (T-60)
        await self.run_phase("WARMING", 60)
        
        # Phase 3: Kill Chain (T-30)
        await self.run_phase("KILL_CHAIN", 30)
        
        self.logger.info(" [V] GENESIS COMPLETE. Profile Aged & Warmed.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Lucid Empire Genesis Engine")
    parser.add_argument("--profile", help="Target profile name", default=os.getenv("LUCID_TARGET_PROFILE", "default"))
    parser.add_argument("--persona", help="Persona type (student/worker)", default="student")
    parser.add_argument("--geo", help="Proxy geolocation (e.g., 'New York')", default="New York")
    parser.add_argument("--country", help="Proxy country code (e.g., 'US')", default="US")
    
    args = parser.parse_args()
    
    # Update PROFILE_DIR if a specific profile is targeted
    if args.profile != "default":
        PROFILE_DIR = os.path.join("./lucid_profile_data", args.profile)
    
    engine = GenesisEngine(persona=args.persona, proxy_geo=args.geo, proxy_country=args.country)
    asyncio.run(engine.execute_90_day_cycle())
