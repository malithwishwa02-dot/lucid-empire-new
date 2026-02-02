# Lucid Empire - API Reference

Complete REST API documentation for Lucid Empire.

## Base URL
```
http://localhost:8000
```

## API Documentation (Interactive)
```
http://localhost:8000/docs       # Swagger UI
http://localhost:8000/redoc      # ReDoc UI
```

---

## Table of Contents
1. [Authentication](#authentication)
2. [Profiles API](#profiles-api)
3. [Browser API](#browser-api)
4. [System API](#system-api)
5. [Status Codes](#status-codes)
6. [Error Handling](#error-handling)

---

## Authentication

Currently, the API does not require authentication. In production, add API key or JWT:

```python
# Example: Add to future versions
headers = {
    "Authorization": "Bearer YOUR_API_KEY"
}
```

---

## Profiles API

### List All Profiles

**Endpoint:**
```
GET /profiles
```

**Description:** Get list of all available profiles.

**Response:**
```json
{
  "count": 2,
  "profiles": [
    {
      "name": "Titan_SoftwareEng_USA_001",
      "identity": {
        "first_name": "James",
        "last_name": "Mitchell"
      },
      "location": "San Francisco, CA",
      "created_at": "2026-02-01T10:30:00Z"
    },
    {
      "name": "Titan_GovClerk_UK_001",
      "identity": {
        "first_name": "Margaret",
        "last_name": "Thompson"
      },
      "location": "London, UK",
      "created_at": "2026-02-01T10:30:00Z"
    }
  ]
}
```

**Example:**
```bash
curl http://localhost:8000/profiles
```

---

### Get Profile Details

**Endpoint:**
```
GET /profiles/{profile_name}
```

**Parameters:**
- `profile_name` (string, required): Name of profile

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
      "timezone": "America/Los_Angeles",
      "latitude": 37.7749,
      "longitude": -122.4194
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
    "port": 1080,
    "username": "james.mitchell"
  },
  "browser": {
    "extensions": [
      "uBlock Origin",
      "HTTPS Everywhere",
      "Privacy Badger"
    ]
  },
  "created_at": "2026-02-01T10:30:00Z",
  "last_used": "2026-02-02T14:22:15Z"
}
```

**Example:**
```bash
curl http://localhost:8000/profiles/Titan_SoftwareEng_USA_001
```

---

### Create Profile

**Endpoint:**
```
POST /profiles
```

**Request Body:**
```json
{
  "name": "Custom_Profile_001",
  "identity": {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "+1 555 123 4567",
    "location": {
      "city": "New York",
      "state": "NY",
      "country": "USA",
      "timezone": "America/New_York"
    }
  },
  "payment": {
    "card_number": "4111111111111111",
    "cardholder": "John Doe",
    "cvv": "123",
    "expiry_month": 12,
    "expiry_year": 2027
  },
  "proxy": {
    "type": "SOCKS5",
    "host": "192.168.1.100",
    "port": 1080,
    "username": "john.doe",
    "password": "SecurePass2024"
  }
}
```

**Response (201 Created):**
```json
{
  "name": "Custom_Profile_001",
  "status": "created",
  "path": "/root/lucid_profile_data/Custom_Profile_001",
  "message": "Profile created successfully"
}
```

**Example:**
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

### Update Profile

**Endpoint:**
```
PUT /profiles/{profile_name}
```

**Parameters:**
- `profile_name` (string, required): Name of profile to update

**Request Body:** (All fields optional)
```json
{
  "identity": {
    "email": "newemail@example.com"
  },
  "proxy": {
    "host": "192.168.1.200",
    "port": 1080
  }
}
```

**Response:**
```json
{
  "name": "Titan_SoftwareEng_USA_001",
  "status": "updated",
  "message": "Profile updated successfully",
  "updated_fields": ["proxy"]
}
```

**Example:**
```bash
curl -X PUT http://localhost:8000/profiles/Titan_SoftwareEng_USA_001 \
  -H "Content-Type: application/json" \
  -d '{
    "proxy": {
      "host": "192.168.1.200",
      "port": 1080
    }
  }'
```

---

### Delete Profile

**Endpoint:**
```
DELETE /profiles/{profile_name}
```

**Parameters:**
- `profile_name` (string, required): Name of profile to delete

**Response:**
```json
{
  "name": "Custom_Profile_001",
  "status": "deleted",
  "message": "Profile deleted successfully"
}
```

**Example:**
```bash
curl -X DELETE http://localhost:8000/profiles/Custom_Profile_001
```

---

### Clone Profile

**Endpoint:**
```
POST /profiles/{profile_name}/clone
```

**Parameters:**
- `profile_name` (string, required): Source profile to clone

**Request Body:**
```json
{
  "new_name": "Cloned_Profile_001",
  "modifications": {
    "proxy": {
      "host": "192.168.1.150",
      "port": 1080
    }
  }
}
```

**Response:**
```json
{
  "source": "Titan_SoftwareEng_USA_001",
  "new_profile": "Cloned_Profile_001",
  "status": "cloned",
  "message": "Profile cloned successfully"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/profiles/Titan_SoftwareEng_USA_001/clone \
  -H "Content-Type: application/json" \
  -d '{
    "new_name": "Cloned_Profile_001"
  }'
```

---

## Browser API

### Launch Firefox

**Endpoint:**
```
POST /browser/launch
```

**Request Body:**
```json
{
  "profile": "Titan_SoftwareEng_USA_001",
  "url": "https://www.example.com",
  "headless": false,
  "timeout": 600
}
```

**Parameters:**
- `profile` (string, required): Profile name to use
- `url` (string, optional): URL to open on startup
- `headless` (boolean, optional): Run without GUI (default: false)
- `timeout` (integer, optional): Auto-close after N seconds (default: None)

**Response:**
```json
{
  "status": "started",
  "pid": 12345,
  "profile": "Titan_SoftwareEng_USA_001",
  "url": "https://www.example.com",
  "headless": false,
  "message": "Firefox launched successfully"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/browser/launch \
  -H "Content-Type: application/json" \
  -d '{
    "profile": "Titan_SoftwareEng_USA_001",
    "url": "https://www.google.com",
    "headless": false
  }'
```

---

### Kill Firefox

**Endpoint:**
```
POST /browser/kill
```

**Request Body:**
```json
{
  "pid": 12345
}
```

**Parameters:**
- `pid` (integer, required): Process ID to terminate

**Response:**
```json
{
  "status": "killed",
  "pid": 12345,
  "message": "Firefox process terminated"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/browser/kill \
  -H "Content-Type: application/json" \
  -d '{"pid": 12345}'
```

---

### Browser Status

**Endpoint:**
```
GET /browser/status
```

**Response:**
```json
{
  "running_processes": [
    {
      "pid": 12345,
      "profile": "Titan_SoftwareEng_USA_001",
      "started_at": "2026-02-02T14:22:15Z",
      "headless": false
    }
  ],
  "count": 1
}
```

**Example:**
```bash
curl http://localhost:8000/browser/status
```

---

## System API

### Health Check

**Endpoint:**
```
GET /health
```

**Response:**
```json
{
  "status": "ok",
  "version": "1.0.0",
  "timestamp": "2026-02-02T14:22:15Z",
  "python": "3.11.0",
  "platform": "linux"
}
```

**Example:**
```bash
curl http://localhost:8000/health
```

---

### System Info

**Endpoint:**
```
GET /system/info
```

**Response:**
```json
{
  "platform": "linux",
  "python_version": "3.11.0",
  "cpu_count": 8,
  "memory_total_gb": 16,
  "memory_available_gb": 8,
  "disk_total_gb": 500,
  "disk_free_gb": 150,
  "firefox_installed": true,
  "firefox_version": "147.0"
}
```

**Example:**
```bash
curl http://localhost:8000/system/info
```

---

### Configuration

**Endpoint:**
```
GET /system/config
```

**Response:**
```json
{
  "profile_data_path": "/root/lucid_profile_data",
  "engine_path": "/root/engine",
  "api_version": "1.0.0",
  "max_browsers": 10,
  "default_timeout": 600,
  "proxy_enabled": true
}
```

**Example:**
```bash
curl http://localhost:8000/system/config
```

---

## Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK | Request succeeded |
| 201 | Created | Resource created successfully |
| 204 | No Content | Request succeeded, no content |
| 400 | Bad Request | Invalid parameters |
| 401 | Unauthorized | Authentication required |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Resource already exists |
| 500 | Server Error | Internal error |

---

## Error Handling

### Error Response Format

```json
{
  "status": "error",
  "code": "PROFILE_NOT_FOUND",
  "message": "Profile 'NonExistent_Profile' not found",
  "detail": "Available profiles: Titan_SoftwareEng_USA_001, Titan_GovClerk_UK_001"
}
```

### Common Error Codes

**PROFILE_NOT_FOUND**
```json
{
  "status": "error",
  "code": "PROFILE_NOT_FOUND",
  "message": "Profile 'Nonexistent_Profile' not found",
  "http_code": 404
}
```

**PROFILE_ALREADY_EXISTS**
```json
{
  "status": "error",
  "code": "PROFILE_ALREADY_EXISTS",
  "message": "Profile 'Titan_SoftwareEng_USA_001' already exists",
  "http_code": 409
}
```

**INVALID_REQUEST**
```json
{
  "status": "error",
  "code": "INVALID_REQUEST",
  "message": "Missing required field: name",
  "http_code": 400
}
```

**FIREFOX_LAUNCH_FAILED**
```json
{
  "status": "error",
  "code": "FIREFOX_LAUNCH_FAILED",
  "message": "Failed to launch Firefox: Binary not found",
  "http_code": 500
}
```

---

## Rate Limiting

Currently no rate limiting. In production, add:
- 100 requests per minute per IP
- Burst: 200 requests

---

## Python Client Example

```python
import requests
import json

class LucidClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def list_profiles(self):
        """Get all profiles"""
        response = self.session.get(f"{self.base_url}/profiles")
        return response.json()
    
    def get_profile(self, name):
        """Get specific profile"""
        response = self.session.get(f"{self.base_url}/profiles/{name}")
        return response.json()
    
    def create_profile(self, profile_data):
        """Create new profile"""
        response = self.session.post(
            f"{self.base_url}/profiles",
            json=profile_data
        )
        return response.json()
    
    def launch_browser(self, profile_name, url=None, headless=False):
        """Launch Firefox with profile"""
        data = {
            "profile": profile_name,
            "headless": headless
        }
        if url:
            data["url"] = url
        
        response = self.session.post(
            f"{self.base_url}/browser/launch",
            json=data
        )
        return response.json()
    
    def kill_browser(self, pid):
        """Terminate Firefox process"""
        response = self.session.post(
            f"{self.base_url}/browser/kill",
            json={"pid": pid}
        )
        return response.json()

# Usage
client = LucidClient()

# List profiles
profiles = client.list_profiles()
print(f"Available profiles: {profiles['count']}")

# Get details
profile = client.get_profile("Titan_SoftwareEng_USA_001")
print(f"Profile: {profile['identity']['first_name']} {profile['identity']['last_name']}")

# Launch browser
result = client.launch_browser("Titan_SoftwareEng_USA_001", url="https://www.google.com")
print(f"Browser PID: {result['pid']}")
```

---

## Webhook Examples

### Monitor Browser Launches

```python
from fastapi import FastAPI
from pydantic import BaseModel

webhook_app = FastAPI()

class BrowserLaunchEvent(BaseModel):
    profile: str
    pid: int
    timestamp: str

@webhook_app.post("/browser-launched")
async def handle_browser_launch(event: BrowserLaunchEvent):
    print(f"Browser launched: {event.profile} (PID: {event.pid})")
    # Add custom logic here
    return {"status": "received"}
```

---

## Version History

- **v1.0.0** (Feb 2, 2026) - Initial release
- **v0.9.0** (Jan 15, 2026) - Beta release

---

**Last Updated:** February 2, 2026  
**Status:** Production Ready
