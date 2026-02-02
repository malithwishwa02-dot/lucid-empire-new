# Lucid Empire - Operations Manual

Complete operations guide for deployment, monitoring, maintenance, and troubleshooting.

## Table of Contents
1. [Deployment](#deployment)
2. [Configuration](#configuration)
3. [Monitoring](#monitoring)
4. [Maintenance](#maintenance)
5. [Backup & Recovery](#backup--recovery)
6. [Performance Tuning](#performance-tuning)
7. [Security](#security)
8. [Troubleshooting](#troubleshooting)

---

## Deployment

### Local Development

```bash
# Setup
git clone https://github.com/malithwishwa02-dot/lucid-empire-new.git
cd lucid-empire-new
./setup_externals.sh  # Download engine/ and bin/
pip install -r requirements.txt

# Run API server
python -m uvicorn backend.lucid_api:app --host 127.0.0.1 --port 8000 --reload
```

### Docker Deployment

```bash
# Build image
docker build -t lucid-empire:latest .

# Run container
docker run -d \
  --name lucid-api \
  -p 8000:8000 \
  -v $(pwd)/lucid_profile_data:/app/lucid_profile_data \
  -v $(pwd)/logs:/app/logs \
  lucid-empire:latest

# Check logs
docker logs -f lucid-api

# Stop container
docker stop lucid-api
```

### Kubernetes Deployment

```yaml
# lucid-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: lucid-empire
spec:
  replicas: 3
  selector:
    matchLabels:
      app: lucid-empire
  template:
    metadata:
      labels:
        app: lucid-empire
    spec:
      containers:
      - name: lucid-api
        image: lucid-empire:latest
        ports:
        - containerPort: 8000
        volumeMounts:
        - name: profiles
          mountPath: /app/lucid_profile_data
        - name: logs
          mountPath: /app/logs
        env:
        - name: LOG_LEVEL
          value: "INFO"
      volumes:
      - name: profiles
        persistentVolumeClaim:
          claimName: lucid-profiles-pvc
      - name: logs
        emptyDir: {}

---
apiVersion: v1
kind: Service
metadata:
  name: lucid-api-service
spec:
  selector:
    app: lucid-empire
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

**Deploy:**
```bash
kubectl apply -f lucid-deployment.yaml
kubectl get pods -l app=lucid-empire
kubectl port-forward service/lucid-api-service 8000:80
```

---

## Configuration

### Environment Variables

```bash
# API Configuration
export LUCID_API_HOST=0.0.0.0
export LUCID_API_PORT=8000
export LUCID_API_WORKERS=4
export LUCID_API_LOG_LEVEL=INFO

# Profile Configuration
export LUCID_PROFILE_DATA_PATH=/root/lucid_profile_data
export LUCID_ENGINE_PATH=/root/engine

# Browser Configuration
export LUCID_FIREFOX_PATH=/root/engine/firefox/firefox
export LUCID_FIREFOX_TIMEOUT=600
export LUCID_FIREFOX_HEADLESS=false

# Proxy Configuration
export LUCID_PROXY_ENABLED=true
export LUCID_PROXY_TIMEOUT=30

# Logging
export LUCID_LOG_DIR=/root/logs
export LUCID_LOG_LEVEL=INFO
```

### Configuration File (lucid_config.json)

```json
{
  "api": {
    "host": "0.0.0.0",
    "port": 8000,
    "workers": 4,
    "log_level": "INFO"
  },
  "profiles": {
    "data_path": "/root/lucid_profile_data",
    "default_timeout": 600,
    "max_profiles": 100
  },
  "browser": {
    "engine_path": "/root/engine",
    "firefox_path": "/root/engine/firefox/firefox",
    "headless": false,
    "timeout": 600,
    "max_instances": 10
  },
  "proxy": {
    "enabled": true,
    "timeout": 30,
    "retry_count": 3
  },
  "logging": {
    "directory": "/root/logs",
    "level": "INFO",
    "max_size": "100MB",
    "retention_days": 30
  }
}
```

**Load configuration:**
```python
import json

with open('lucid_config.json') as f:
    config = json.load(f)

api_port = config['api']['port']
profile_path = config['profiles']['data_path']
```

---

## Monitoring

### Health Checks

```bash
# API health
curl http://localhost:8000/health

# System info
curl http://localhost:8000/system/info

# Running browsers
curl http://localhost:8000/browser/status
```

### Log Monitoring

```bash
# View recent logs
tail -100 logs/lucid-api.log

# Watch logs in real-time
tail -f logs/lucid-api.log

# Search for errors
grep ERROR logs/lucid-api.log | tail -20

# Count log levels
grep -c "INFO" logs/lucid-api.log
grep -c "ERROR" logs/lucid-api.log
grep -c "WARNING" logs/lucid-api.log
```

### Metrics Collection

```python
# Example: Collect metrics
import psutil
import json
from datetime import datetime

def collect_metrics():
    metrics = {
        "timestamp": datetime.now().isoformat(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory": {
            "total_gb": psutil.virtual_memory().total / (1024**3),
            "available_gb": psutil.virtual_memory().available / (1024**3),
            "percent": psutil.virtual_memory().percent
        },
        "disk": {
            "total_gb": psutil.disk_usage('/').total / (1024**3),
            "free_gb": psutil.disk_usage('/').free / (1024**3),
            "percent": psutil.disk_usage('/').percent
        },
        "processes": len(psutil.pids())
    }
    return metrics

# Save metrics
metrics = collect_metrics()
with open('logs/metrics.json', 'a') as f:
    f.write(json.dumps(metrics) + '\n')
```

### Prometheus Integration

```python
# Add to lucid_api.py for Prometheus metrics
from prometheus_client import Counter, Histogram, start_http_server

# Metrics
profile_requests = Counter('lucid_profile_requests_total', 'Total profile requests')
browser_launches = Counter('lucid_browser_launches_total', 'Total browser launches')
request_duration = Histogram('lucid_request_duration_seconds', 'Request duration')

# Start metrics server on port 9090
start_http_server(9090)

# Use in endpoints
@app.get("/profiles")
def list_profiles():
    profile_requests.inc()
    # ... rest of function
```

---

## Maintenance

### Daily Tasks

```bash
# Check disk usage
df -h

# Verify API is running
curl -s http://localhost:8000/health | jq .

# Check for stuck browsers
ps aux | grep firefox | grep -v grep

# Rotate old logs
find logs/ -name "*.log" -mtime +7 -delete
```

### Weekly Tasks

```bash
# Backup profile data
tar -czf backups/profiles_$(date +%Y%m%d).tar.gz lucid_profile_data/

# Cleanup temporary files
find . -name "__pycache__" -type d -exec rm -rf {} +
find . -name "*.pyc" -delete

# Update Python packages
pip list --outdated
pip install --upgrade pip setuptools wheel
```

### Monthly Tasks

```bash
# Full system health check
python verify_readiness.py

# Security audit
python audit_and_fix.py

# Database optimization
sqlite3 lucid_profile_data/*/cookies.sqlite "VACUUM;"
sqlite3 lucid_profile_data/*/places.sqlite "VACUUM;"

# Review and archive old logs
tar -czf backups/logs_$(date +%Y%m).tar.gz logs/*.log
```

### Database Maintenance

```bash
# Check database integrity
sqlite3 lucid_profile_data/Titan_SoftwareEng_USA_001/cookies.sqlite "PRAGMA integrity_check;"

# Optimize database
sqlite3 lucid_profile_data/Titan_SoftwareEng_USA_001/cookies.sqlite "VACUUM;"

# Analyze database statistics
sqlite3 lucid_profile_data/Titan_SoftwareEng_USA_001/places.sqlite "ANALYZE;"

# Backup profile database
cp lucid_profile_data/Titan_SoftwareEng_USA_001/cookies.sqlite \
   backups/cookies_$(date +%Y%m%d_%H%M%S).sqlite
```

---

## Backup & Recovery

### Full Backup

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/lucid_backup_$TIMESTAMP.tar.gz"

# Create backup
tar -czf "$BACKUP_FILE" \
  lucid_profile_data/ \
  requirements.txt \
  .gitignore \
  lucid_config.json

# Keep only last 10 backups
ls -t "$BACKUP_DIR"/lucid_backup_*.tar.gz | tail -n +11 | xargs rm -f

echo "✓ Backup created: $BACKUP_FILE"
```

**Run daily:**
```bash
chmod +x backup.sh
0 2 * * * /root/lucid-empire-new/backup.sh  # Run at 2 AM daily
```

### Restore from Backup

```bash
# List available backups
ls -lh backups/lucid_backup_*.tar.gz

# Extract specific backup
tar -xzf backups/lucid_backup_20260202_021500.tar.gz

# Verify restoration
ls -la lucid_profile_data/ | head -5
```

### Incremental Backup

```bash
#!/bin/bash
# incremental_backup.sh

BACKUP_DIR="backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
FULL_BACKUP="$BACKUP_DIR/lucid_full_$(date +%Y%m%d).tar.gz"
INCR_BACKUP="$BACKUP_DIR/lucid_incr_$TIMESTAMP.tar.gz"

# Create incremental backup since last backup
find lucid_profile_data/ \
  -newermt "1 day ago" \
  -type f | tar -czf "$INCR_BACKUP" -T -

echo "✓ Incremental backup: $INCR_BACKUP"
```

---

## Performance Tuning

### API Performance

```python
# Use uvicorn workers for parallelism
python -m uvicorn backend.lucid_api:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 8  # Match CPU count
```

### Browser Performance

```python
# Pre-cache profiles
from backend.core.genesis_engine import ProfileFactory

factory = ProfileFactory()
profiles = ['Titan_SoftwareEng_USA_001', 'Titan_GovClerk_UK_001']

for profile_name in profiles:
    profile = factory.load_profile(profile_name)  # Cache in memory
    print(f"✓ Cached: {profile_name}")
```

### Database Performance

```sql
-- Create indexes for faster queries
CREATE INDEX idx_cookies_host ON moz_cookies(host);
CREATE INDEX idx_history_visit_date ON moz_historyvisits(visit_date DESC);

-- Analyze statistics
ANALYZE;

-- Optimize storage
VACUUM;
```

### Memory Optimization

```python
# Monitor memory usage
import psutil
import os

def get_memory_usage(pid=None):
    if pid is None:
        pid = os.getpid()
    
    process = psutil.Process(pid)
    return {
        "rss_mb": process.memory_info().rss / (1024**2),
        "vms_mb": process.memory_info().vms / (1024**2),
        "percent": process.memory_percent()
    }

print(get_memory_usage())
```

---

## Security

### API Security

```python
# Add authentication
from fastapi.security import HTTPBearer, HTTPAuthCredential
from fastapi import Depends, HTTPException

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthCredential = Depends(security)):
    token = credentials.credentials
    if token != os.getenv("API_TOKEN"):
        raise HTTPException(status_code=401, detail="Invalid token")
    return token

# Protect endpoints
@app.get("/profiles", dependencies=[Depends(verify_token)])
def list_profiles():
    # ... endpoint code
```

### HTTPS/TLS

```bash
# Generate self-signed certificate
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# Run with HTTPS
python -m uvicorn backend.lucid_api:app \
  --host 0.0.0.0 \
  --port 8443 \
  --ssl-keyfile key.pem \
  --ssl-certfile cert.pem
```

### Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.get("/profiles")
@limiter.limit("100/minute")
def list_profiles(request: Request):
    # ... endpoint code
```

### Input Validation

```python
from pydantic import BaseModel, validator

class ProfileCreate(BaseModel):
    name: str
    identity: dict
    
    @validator('name')
    def name_not_empty(cls, v):
        if not v or len(v) < 3:
            raise ValueError('Name must be at least 3 characters')
        return v
    
    @validator('identity')
    def identity_valid(cls, v):
        required_fields = ['first_name', 'last_name']
        if not all(field in v for field in required_fields):
            raise ValueError(f'Identity must include: {required_fields}')
        return v
```

### Secrets Management

```bash
# Store sensitive data in environment variables or secure vault
export LUCID_API_TOKEN=$(openssl rand -hex 32)
export LUCID_DB_PASSWORD=$(openssl rand -base64 32)

# Or use a secrets manager
# AWS Secrets Manager, HashiCorp Vault, etc.
```

---

## Troubleshooting

### API Won't Start

```bash
# Check port availability
lsof -i :8000
netstat -ano | findstr :8000

# Check Python errors
python -m uvicorn backend.lucid_api:app --log-level debug

# Check dependencies
python -c "import fastapi; import pydantic; print('✓ Dependencies OK')"
```

### Firefox Launch Fails

```bash
# Check Firefox binary exists
ls -la engine/firefox/firefox

# Test Firefox directly
./engine/firefox/firefox --version

# Check profile directory permissions
ls -la lucid_profile_data/

# Launch with verbose output
python lucid_launcher.py --profile Titan_SoftwareEng_USA_001 --verbose
```

### Database Lock Issues

```bash
# Find processes holding database locks
lsof lucid_profile_data/*/cookies.sqlite

# Kill blocking process
kill -9 <PID>

# Remove lock files
rm -f lucid_profile_data/*/cookies.sqlite-lock
rm -f lucid_profile_data/*/places.sqlite-lock

# Verify database integrity
sqlite3 lucid_profile_data/*/cookies.sqlite "PRAGMA integrity_check;"
```

### High Memory Usage

```bash
# Find process using most memory
ps aux --sort=-%mem | head -10

# Monitor Firefox memory
ps aux | grep firefox | grep -v grep

# Kill excessive browser processes
pkill -f "firefox"

# Check for memory leaks
python -m memory_profiler main.py
```

### Proxy Connection Issues

```python
# Test proxy connectivity
from backend.network.proxy_manager import ProxyManager

manager = ProxyManager()
proxy = manager.get_proxy('Titan_SoftwareEng_USA_001')

# Test
is_connected = manager.test_proxy(proxy)
print(f"Connected: {is_connected}")

# Diagnose
import socket
try:
    socket.create_connection((proxy['host'], proxy['port']), timeout=5)
    print("✓ Proxy accessible")
except:
    print("✗ Cannot reach proxy")
```

### Performance Issues

```bash
# Monitor system resources
watch -n 1 "free -h && df -h && ps aux --sort=-%cpu | head -5"

# Check CPU usage
top -b -n 1 | head -20

# Check disk I/O
iostat -x 1 5

# Check network
netstat -s | head -20
```

---

## Support & Escalation

### Log Files to Review

1. **API Logs:** `logs/lucid-api.log`
2. **Firefox Logs:** `lucid_profile_data/*/logs/`
3. **System Logs:** `logs/system.log` (if configured)

### Debug Mode

```bash
# Enable verbose logging
export LUCID_LOG_LEVEL=DEBUG
python -m uvicorn backend.lucid_api:app --log-level debug
```

### Diagnostic Bundle

```bash
#!/bin/bash
# Create diagnostic bundle for support
BUNDLE="lucid_diagnostics_$(date +%Y%m%d_%H%M%S).tar.gz"

tar -czf "$BUNDLE" \
  logs/ \
  lucid_config.json \
  <(python system/info) \
  <(git log --oneline -20) \
  <(pip list)

echo "Diagnostic bundle: $BUNDLE"
```

---

## Emergency Procedures

### Graceful Shutdown

```bash
# Shutdown API
kill -SIGTERM $(lsof -t -i :8000)

# Close all browsers
pkill -f firefox

# Wait for cleanup
sleep 5

# Verify all processes stopped
ps aux | grep -E "(firefox|python.*lucid)" | grep -v grep
```

### Recovery After Crash

```bash
# 1. Check system health
python verify_readiness.py

# 2. Restore from backup if needed
tar -xzf backups/lucid_backup_latest.tar.gz

# 3. Check database integrity
sqlite3 lucid_profile_data/*/cookies.sqlite "PRAGMA integrity_check;"

# 4. Restart API
python -m uvicorn backend.lucid_api:app --host 0.0.0.0 --port 8000
```

---

## References

- **Documentation:** See INSTALLATION.md, USAGE_GUIDE.md, API_REFERENCE.md
- **Logs:** Check `logs/` directory
- **Configuration:** Edit `lucid_config.json`
- **Issues:** https://github.com/malithwishwa02-dot/lucid-empire-new/issues

---

**Last Updated:** February 2, 2026  
**Version:** 1.0.0  
**Status:** Production Ready
