# Lucid Empire - Usage Guide

Complete guide to using Lucid Empire for profile management, browser operations, and API access.

## Table of Contents
1. [Quick Start](#quick-start)
2. [Profile Management](#profile-management)
3. [Launching Firefox](#launching-firefox)
4. [API Usage](#api-usage)
5. [Advanced Features](#advanced-features)
6. [Examples](#examples)

---

## Quick Start

### Launch the Application

**Python Entry Point:**
```bash
python main.py
```

**API Server Only:**
```bash
python -m uvicorn backend.lucid_api:app --host 0.0.0.0 --port 8000
```

**Browser with Default Profile:**
```bash
python lucid_launcher.py --profile Titan_SoftwareEng_USA_001
```

---

## Profile Management

### Available Profiles

Lucid Empire includes pre-configured profiles:

#### 1. **Titan_SoftwareEng_USA_001** (USA Software Engineer)
- **Location:** San Francisco, CA
- **Identity:** James Mitchell
- **Payment:** Mastercard (5412752589637849)
- **Behavior:** Professional, tech-focused browsing
- **Proxy:** SOCKS5 (US-based)
- **Use Case:** Software development, tech news, cloud services

#### 2. **Titan_GovClerk_UK_001** (UK Government Clerk)
- **Location:** London, UK
- **Identity:** Margaret Thompson
- **Payment:** Visa (4916830899839814)
- **Behavior:** Administrative, office-focused browsing
- **Proxy:** SOCKS5 (UK-based)
- **Use Case:** Government services, documentation, research

### Listing Available Profiles

```python
# Python API
from backend.core.genesis_engine import ProfileFactory

profiles = ProfileFactory.list_available_profiles()
for profile in profiles:
    print(f"✓ {profile}")
```

**CLI:**
```bash
python -c "
import os
profiles = [d for d in os.listdir('lucid_profile_data') if os.path.isdir(f'lucid_profile_data/{d}')]
for p in profiles:
    print(f'  • {p}')
"
```

### Create New Profile

```python
from backend.core.genesis_engine import ProfileFactory
from backend.modules.humanization import BehavioralSimulator

# Create profile factory
factory = ProfileFactory()

# Configure new profile
profile_config = {
    'name': 'Titan_Marketing_EU_001',
    'identity': {
        'first_name': 'Anna',
        'last_name': 'Schmidt',
        'email': 'anna.schmidt@example.de',
        'phone': '+49 30 123 4567',
        'location': {'city': 'Berlin', 'country': 'Germany', 'timezone': 'Europe/Berlin'}
    },
    'payment': {
        'card_number': '6011111111111111',  # Discover (test number)
        'cardholder': 'Anna Schmidt',
        'cvv': '123',
        'expiry_month': 8,
        'expiry_year': 2027
    },
    'proxy': {
        'type': 'SOCKS5',
        'host': '192.168.1.100',
        'port': 1080,
        'username': 'anna.schmidt',
        'password': 'SecurePass2024'
    }
}

# Create the profile
profile_path = factory.create_profile(profile_config)
print(f"✓ Profile created: {profile_path}")
```

### Load Profile

```python
from backend.core.genesis_engine import ProfileFactory

factory = ProfileFactory()
profile = factory.load_profile('Titan_SoftwareEng_USA_001')

print(f"Profile: {profile.name}")
print(f"Identity: {profile.identity['name']}")
print(f"Location: {profile.identity['location']['city']}, {profile.identity['location']['country']}")
```

### Clone Profile

```python
factory = ProfileFactory()

# Duplicate existing profile with modifications
new_profile = factory.clone_profile(
    source='Titan_SoftwareEng_USA_001',
    new_name='Titan_SoftwareEng_USA_002',
    modifications={
        'proxy': {
            'host': '192.168.1.51',
            'port': 1080
        }
    }
)
print(f"✓ Cloned: {new_profile.name}")
```

### Delete Profile

```python
import shutil

profile_path = 'lucid_profile_data/Titan_SoftwareEng_USA_001'
shutil.rmtree(profile_path)
print(f"✓ Deleted: Titan_SoftwareEng_USA_001")
```

---

## Launching Firefox

### Basic Launch

```python
from backend.lucid_launcher import LucidLauncher

launcher = LucidLauncher()
process = launcher.launch_firefox('Titan_SoftwareEng_USA_001')
print(f"Firefox PID: {process.pid}")

# Browser now running with profile
# Press Ctrl+C to stop
```

### Launch with Options

```python
launcher = LucidLauncher(
    headless=False,           # Show browser window
    private_mode=False,       # Normal mode (not private)
    disable_extensions=False, # Use installed extensions
    verbose=True              # Print debug output
)

process = launcher.launch_firefox(
    profile_name='Titan_GovClerk_UK_001',
    url='https://www.google.com',  # Open specific URL
    timeout=300  # Close after 5 minutes
)
```

### Headless Mode (Automation)

```python
launcher = LucidLauncher(headless=True)
process = launcher.launch_firefox(
    profile_name='Titan_SoftwareEng_USA_001',
    url='https://httpbin.org/ip'
)

# Use with Playwright or Selenium for automation
# Process runs in background
```

### Kill Firefox Process

```python
import subprocess
import os

# Option 1: Kill by name
os.system('pkill -f firefox')  # Linux/macOS
os.system('taskkill /IM firefox.exe /F')  # Windows

# Option 2: Kill specific PID
import signal
signal.kill(process.pid, signal.SIGTERM)
```

---

## API Usage

### Starting the API Server

```bash
# Standard
python -m uvicorn backend.lucid_api:app --host 127.0.0.1 --port 8000

# Production
python -m uvicorn backend.lucid_api:app --host 0.0.0.0 --port 8000 --workers 4

# With reload (development)
python -m uvicorn backend.lucid_api:app --reload
```

**API Documentation:** http://127.0.0.1:8000/docs (Swagger UI)

### REST Endpoints

#### List Profiles
```bash
curl http://localhost:8000/profiles
```

**Response:**
```json
{
  "profiles": [
    {
      "name": "Titan_SoftwareEng_USA_001",
      "identity": {
        "first_name": "James",
        "last_name": "Mitchell",
        "location": "San Francisco, CA"
      },
      "created_at": "2026-02-01T10:30:00Z"
    }
  ]
}
```

---

#### Get Profile Details
```bash
curl http://localhost:8000/profiles/Titan_SoftwareEng_USA_001
```

**Response:**
```json
{
  "name": "Titan_SoftwareEng_USA_001",
  "identity": {
    "first_name": "James",
    "last_name": "Mitchell",
    "email": "james.mitchell@techmail.com",
    "phone": "+1 415 555 0123",
    "location": {
      "city": "San Francisco",
      "state": "CA",
      "country": "USA",
      "timezone": "America/Los_Angeles"
    }
  },
  "payment": {
    "card_type": "Mastercard",
    "card_number_last4": "7849",
    "expiry": "11/2026"
  },
  "proxy": {
    "type": "SOCKS5",
    "host": "192.168.1.50",
    "port": 1080
  }
}
```

---

#### Launch Firefox
```bash
curl -X POST http://localhost:8000/browser/launch \
  -H "Content-Type: application/json" \
  -d '{
    "profile": "Titan_SoftwareEng_USA_001",
    "url": "https://www.google.com",
    "headless": false
  }'
```

**Response:**
```json
{
  "status": "started",
  "pid": 12345,
  "profile": "Titan_SoftwareEng_USA_001",
  "message": "Firefox launched successfully"
}
```

---

#### Create Profile
```bash
curl -X POST http://localhost:8000/profiles \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Custom_Profile_001",
    "identity": {
      "first_name": "John",
      "last_name": "Doe",
      "location": {"city": "New York", "country": "USA"}
    },
    "payment": {
      "card_number": "4111111111111111",
      "cardholder": "John Doe",
      "cvv": "123",
      "expiry_month": 12,
      "expiry_year": 2027
    }
  }'
```

---

### Python Client

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# List profiles
response = requests.get(f"{BASE_URL}/profiles")
profiles = response.json()
print(f"Available profiles: {len(profiles)}")

# Get profile details
profile = requests.get(f"{BASE_URL}/profiles/Titan_SoftwareEng_USA_001").json()
print(f"Profile: {profile['identity']['first_name']} {profile['identity']['last_name']}")

# Launch Firefox
launch_response = requests.post(
    f"{BASE_URL}/browser/launch",
    json={
        "profile": "Titan_SoftwareEng_USA_001",
        "url": "https://www.example.com",
        "headless": False
    }
)
result = launch_response.json()
print(f"Firefox PID: {result['pid']}")
```

---

## Advanced Features

### Browser Fingerprinting Protection

Lucid Empire includes anti-detection measures:

```python
from backend.core.genesis_engine import ProfileFactory
from backend.modules.humanization import BehavioralSimulator

# Load profile with hardened prefs
profile = ProfileFactory().load_profile('Titan_SoftwareEng_USA_001')

# Features enabled:
# ✓ WebRTC protection (disabled)
# ✓ Canvas fingerprinting resistance
# ✓ WebGL spoofing
# ✓ Geolocation spoofing
# ✓ Timezone spoofing
# ✓ Telemetry disabled
# ✓ Sync disabled
# ✓ HTTPS-only mode
# ✓ Third-party cookies blocked
```

### Network Proxy Management

```python
from backend.network.proxy_manager import ProxyManager

manager = ProxyManager()

# Get profile proxy
profile_proxy = manager.get_proxy('Titan_SoftwareEng_USA_001')
print(f"Proxy: {profile_proxy['type']}://{profile_proxy['host']}:{profile_proxy['port']}")

# Test proxy connectivity
is_connected = manager.test_proxy(profile_proxy)
print(f"Connected: {is_connected}")

# Set temporary proxy override
manager.set_proxy('Titan_SoftwareEng_USA_001', {
    'type': 'SOCKS5',
    'host': '192.168.1.100',
    'port': 1080
})
```

### Commerce Vault Access

```python
from backend.modules.commerce_injector import CommerceVault

vault = CommerceVault('Titan_SoftwareEng_USA_001')

# Get payment methods
cards = vault.get_cards()
for card in cards:
    print(f"Card: {card['card_type']} ending in {card['last4']}")

# Get purchase history
purchases = vault.get_purchase_history()
print(f"Total purchases: {len(purchases)}")
for purchase in purchases[:5]:
    print(f"  • {purchase['date']}: {purchase['merchant']} - ${purchase['amount']}")

# Add new payment method (testing only)
vault.add_card({
    'card_number': '4111111111111111',
    'cardholder': 'James Mitchell',
    'cvv': '123',
    'expiry_month': 12,
    'expiry_year': 2027
})
```

### Behavioral Simulation

```python
from backend.modules.humanization import BehavioralSimulator

simulator = BehavioralSimulator('Titan_SoftwareEng_USA_001')

# Simulate realistic browsing delays
from time import sleep
import random

urls = [
    'https://github.com',
    'https://stackoverflow.com',
    'https://python.org'
]

for url in urls:
    # Simulate human reading time
    delay = simulator.calculate_read_time(url)
    print(f"Reading {url} for ~{delay:.0f}s")
    sleep(delay)
```

### Database Access

```python
import sqlite3

# Access cookies
conn = sqlite3.connect('lucid_profile_data/Titan_SoftwareEng_USA_001/cookies.sqlite')
cursor = conn.cursor()
cursor.execute('SELECT host, name, value FROM moz_cookies LIMIT 5')
for cookie in cursor.fetchall():
    print(f"{cookie[0]}: {cookie[1]}={cookie[2][:20]}...")
conn.close()

# Access browsing history
conn = sqlite3.connect('lucid_profile_data/Titan_SoftwareEng_USA_001/places.sqlite')
cursor = conn.cursor()
cursor.execute('''
    SELECT title, url, visit_date 
    FROM moz_historyvisits h 
    JOIN moz_places p ON h.place_id = p.id 
    ORDER BY visit_date DESC LIMIT 10
''')
for row in cursor.fetchall():
    print(f"{row[0]}: {row[1]}")
conn.close()
```

---

## Examples

### Example 1: Simulate E-Commerce Browsing

```python
from backend.lucid_launcher import LucidLauncher
from backend.modules.humanization import BehavioralSimulator
import time
import random

# Launch browser
launcher = LucidLauncher(headless=False)
process = launcher.launch_firefox('Titan_SoftwareEng_USA_001', url='https://amazon.com')

# Simulate realistic browsing
simulator = BehavioralSimulator('Titan_SoftwareEng_USA_001')

# Wait for page load
time.sleep(3)

# Simulate scrolling and reading
for _ in range(random.randint(2, 5)):
    delay = simulator.calculate_read_time('product page')
    print(f"Browsing products for {delay:.0f} seconds...")
    time.sleep(delay)

# Close browser
process.terminate()
```

### Example 2: API-Based Profile Management

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Create 5 profiles
for i in range(1, 6):
    profile_data = {
        "name": f"Test_Profile_{i:03d}",
        "identity": {
            "first_name": f"User{i}",
            "last_name": "Test",
            "email": f"user{i}@example.com",
            "location": {"city": "New York", "country": "USA"}
        },
        "payment": {
            "card_number": "4111111111111111",
            "cardholder": f"User {i} Test",
            "cvv": "123",
            "expiry_month": 12,
            "expiry_year": 2027
        }
    }
    
    response = requests.post(f"{BASE_URL}/profiles", json=profile_data)
    if response.status_code == 201:
        print(f"✓ Created: {profile_data['name']}")
    else:
        print(f"✗ Failed: {response.text}")
```

### Example 3: Automated Testing with Multiple Profiles

```python
from backend.core.genesis_engine import ProfileFactory
from backend.lucid_launcher import LucidLauncher
import subprocess
import time

profiles = [
    'Titan_SoftwareEng_USA_001',
    'Titan_GovClerk_UK_001'
]

launcher = LucidLauncher(headless=True)
factory = ProfileFactory()

for profile_name in profiles:
    print(f"\nTesting: {profile_name}")
    
    # Load profile
    profile = factory.load_profile(profile_name)
    print(f"  Identity: {profile.identity['name']}")
    print(f"  Location: {profile.identity['location']['city']}")
    
    # Launch browser
    process = launcher.launch_firefox(profile_name, url='https://httpbin.org/ip')
    time.sleep(5)
    
    # Test should complete
    if process.poll() is None:
        process.terminate()
    print(f"  ✓ Launch successful")
```

### Example 4: Temporal Displacement (Libfaketime)

```bash
# Shift system time 90 days into past
faketime -90d python lucid_launcher.py --profile Titan_SoftwareEng_USA_001

# Specific date
faketime '2025-12-01' python main.py

# Combined with profile
faketime -30d python -c "
from backend.core.genesis_engine import ProfileFactory
profile = ProfileFactory().load_profile('Titan_SoftwareEng_USA_001')
print(f'Profile loaded at: {profile.created_timestamp}')
"
```

---

## Troubleshooting

### Firefox Won't Launch
```bash
# Check engine folder exists
ls -la engine/

# Check Firefox binary permissions
chmod +x engine/firefox/firefox

# Try verbose mode
python lucid_launcher.py --profile Titan_SoftwareEng_USA_001 --verbose
```

### Profile Database Locked
```bash
# Remove lock files
rm -f lucid_profile_data/*/cookies.sqlite-lock
rm -f lucid_profile_data/*/places.sqlite-lock

# Try operation again
```

### API Won't Start
```bash
# Check port availability
lsof -i :8000  # Linux/macOS
netstat -ano | findstr :8000  # Windows

# Try different port
python -m uvicorn backend.lucid_api:app --port 8001
```

---

## Next Steps

- **API Reference:** See `API_REFERENCE.md` for detailed endpoint documentation
- **Operations Manual:** See `OPERATIONS_MANUAL.md` for deployment and monitoring
- **Troubleshooting:** See `TROUBLESHOOTING.md` for extended issue resolution

---

**Last Updated:** February 2, 2026  
**Version:** 1.0.0
