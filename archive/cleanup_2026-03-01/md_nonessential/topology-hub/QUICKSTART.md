# Topology Hub - Quick Start Guide

## What is Topology Hub?

Topology Hub is the **network brain** for your microservices system. It:
- Tracks service locations (name, URL, port, version)
- Maps dependencies (Service A → Service B)
- Monitors runtime health (UP/DOWN/DEGRADED)
- Detects cascade failures (dependency down → service DEGRADED)
- Enforces contracts (schema version validation)
- Streams real-time updates (WebSocket/Socket.IO)

**Critical**: This is **observability only** — your system runs even if Topology Hub dies.

---

## Architecture

```
┌─────────────────────────────────────┐
│  Topology Hub (Go) - Port 52015     │  ← SOURCE OF TRUTH
│  ├─ Service Registry                │
│  ├─ Dependency Map                  │
│  ├─ Health Monitoring               │
│  └─ Schema Validation               │
└─────────────────────────────────────┘
               ▼
┌─────────────────────────────────────┐
│  Topology Hub Express - Port 3000   │  ← PRESENTATION LAYER
│  ├─ JS-Friendly API                 │
│  ├─ Socket.IO Streaming             │
│  └─ Reads from Go Hub               │
└─────────────────────────────────────┘
               ▼
┌─────────────────────────────────────┐
│  Frontend Dashboard                 │
│  Real-Time Topology Visualization   │
└─────────────────────────────────────┘
```

---

## Start Services

### 1. Start Go Hub (Source of Truth)

```bash
cd topology-hub
go run main.go
# → Listening on http://localhost:52015
```

### 2. Start Express (Presentation Layer)

```bash
cd topology-hub-express
npm install
node server.js
# → Listening on http://localhost:3000
# → Proxying to Go hub at http://localhost:52015
```

### 3. Verify Health

```bash
curl http://localhost:52015/health
# → {"status":"healthy","timestamp":1234567890,"connected_clients":0}

curl http://localhost:3000/health
# → {"status":"healthy","go_hub":"http://localhost:52015"}
```

---

## Core API Endpoints

### Health & Readiness

```bash
# Is hub alive?
curl http://localhost:52015/health

# Is hub ready? (loaded topology + can reach Schema Registry)
curl http://localhost:52015/ready
```

### View Topology

```bash
# Full topology (all services + metadata)
curl http://localhost:52015/topology

# Graph format (nodes + edges for dashboard)
curl http://localhost:52015/topology/graph

# Runtime health (UP/DOWN/DEGRADED status)
curl http://localhost:52015/topology/health

# Validation report (schema mismatches + dependency issues)
curl http://localhost:52015/topology/validate
```

### Service Management

```bash
# List all services
curl http://localhost:52015/services

# Get service detail
curl http://localhost:52015/services/perception

# Hub metrics (uptime, client count, update rate)
curl http://localhost:52015/metrics
```

---

## Report Service Updates

Services report their status to Topology Hub:

```bash
curl -X POST http://localhost:52015/report \
  -H "Content-Type: application/json" \
  -d '{
    "id": "perception",
    "sides": 6,
    "status": "online",
    "scale": 1.2,
    "connections": ["event-bus", "knowledge-graph"],
    "dependencies": [
      {
        "target": "event-bus",
        "required": true,
        "health_status": "UP",
        "traffic": 1200,
        "latency": 45
      }
    ],
    "metadata": {
      "schema_version": "1.0.0",
      "team": "core-intelligence"
    }
  }'
```

**Dependency Cascade Example**:
```bash
# 1. Report Event-Bus as DOWN
curl -X POST http://localhost:52015/report -d '{
  "id": "event-bus",
  "status": "faulty"
}'

# 2. Perception becomes DEGRADED (required dependency down)
curl http://localhost:52015/topology/health
# → perception.dependent_status = "DEGRADED"

# 3. Reasoning-Engine becomes DEGRADED (depends on Perception)
# → reasoning-engine.dependent_status = "DEGRADED"
```

---

## Real-Time Streaming

### WebSocket (Go Hub)

```javascript
const ws = new WebSocket('ws://localhost:52015/ws');

ws.onopen = () => {
  console.log('[WS] Connected to Topology Hub');
};

ws.onmessage = (event) => {
  const update = JSON.parse(event.data);
  console.log('[WS] Topology update:', update);
  // → {services: {...}, center_radius: 250, timestamp: 1234567890}
};
```

### Socket.IO (Express)

```javascript
import io from 'socket.io-client';

const socket = io('http://localhost:3000');

socket.on('connect', () => {
  console.log('[SOCKET.IO] Connected');
});

socket.on('topology:initial', (topology) => {
  console.log('[SOCKET.IO] Initial topology:', topology);
});

socket.on('topology:update', (topology) => {
  console.log('[SOCKET.IO] Topology update:', topology);
});
```

---

## Integration Examples

### React Hook (Frontend)

```javascript
import { useEffect, useState } from 'react';
import io from 'socket.io-client';

export function useTopologyHub() {
  const [topology, setTopology] = useState(null);
  const [health, setHealth] = useState(null);

  useEffect(() => {
    const socket = io('http://localhost:3000');

    socket.on('topology:initial', setTopology);
    socket.on('topology:update', setTopology);

    // Fetch health periodically
    const healthInterval = setInterval(async () => {
      const response = await fetch('http://localhost:3000/topology/health');
      const data = await response.json();
      setHealth(data);
    }, 5000);

    return () => {
      socket.disconnect();
      clearInterval(healthInterval);
    };
  }, []);

  return { topology, health };
}
```

### Service Integration (Go)

```go
package main

import (
    "bytes"
    "encoding/json"
    "net/http"
    "time"
)

type TopologyUpdate struct {
    ID           string       `json:"id"`
    Status       string       `json:"status"`
    Dependencies []Dependency `json:"dependencies"`
    Metadata     map[string]interface{} `json:"metadata"`
}

type Dependency struct {
    Target       string `json:"target"`
    Required     bool   `json:"required"`
    HealthStatus string `json:"health_status"`
}

func reportToTopologyHub(serviceName string) {
    update := TopologyUpdate{
        ID:     serviceName,
        Status: "online",
        Dependencies: []Dependency{
            {Target: "event-bus", Required: true, HealthStatus: "UP"},
        },
        Metadata: map[string]interface{}{
            "schema_version": "1.0.0",
        },
    }

    data, _ := json.Marshal(update)
    http.Post("http://localhost:52015/report", "application/json", bytes.NewBuffer(data))
}

func main() {
    // Report to Topology Hub every 30 seconds
    ticker := time.NewTicker(30 * time.Second)
    defer ticker.Stop()

    for range ticker.C {
        reportToTopologyHub("perception")
    }
}
```

### Service Integration (Python)

```python
import requests
import time
import json

def report_to_topology_hub(service_name):
    update = {
        "id": service_name,
        "status": "online",
        "dependencies": [
            {"target": "event-bus", "required": True, "health_status": "UP"}
        ],
        "metadata": {
            "schema_version": "1.0.0"
        }
    }
    
    try:
        response = requests.post(
            "http://localhost:52015/report",
            json=update,
            timeout=5
        )
        print(f"[TOPOLOGY] Reported: {response.status_code}")
    except Exception as e:
        print(f"[TOPOLOGY] Error: {e}")

if __name__ == "__main__":
    while True:
        report_to_topology_hub("perception")
        time.sleep(30)
```

---

## Validation & Troubleshooting

### Check for Issues

```bash
# Get validation report
curl http://localhost:52015/topology/validate
```

**Example Response**:
```json
{
  "valid": false,
  "issues": [
    {
      "type": "dependency_down",
      "severity": "critical",
      "service": "perception",
      "dependency": "event-bus",
      "message": "Service perception has required dependency event-bus that is DOWN"
    },
    {
      "type": "missing_dependency",
      "severity": "critical",
      "service": "reasoning-engine",
      "dependency": "knowledge-graph",
      "message": "Service reasoning-engine depends on knowledge-graph, but knowledge-graph is not registered"
    }
  ],
  "warnings": [
    {
      "type": "invalid_schema_version",
      "severity": "warning",
      "service": "simulation",
      "message": "Service simulation has invalid schema version format: bad-version"
    }
  ],
  "issue_count": 2,
  "warning_count": 1
}
```

### Common Issues

**Problem**: Express can't connect to Go hub
```bash
# Check Go hub is running
curl http://localhost:52015/health

# Check Express GO_HUB_URL environment variable
echo $GO_HUB_URL
# → Should be http://localhost:52015 (or container name in Docker)
```

**Problem**: Service not appearing in topology
```bash
# Verify service is reporting updates
curl http://localhost:52015/services
# → Check if your service ID is in the list

# Check service logs for errors reporting to hub
```

**Problem**: Dependency status not updating
```bash
# Check dependency health is being reported
curl http://localhost:52015/topology/health
# → Check dependent_status field

# Verify Required flag is set correctly in dependency
curl http://localhost:52015/topology/graph
# → Check edges[].required field
```

---

## Environment Variables

### Go Hub
```bash
PORT=52015                           # HTTP server port
BASE_CENTER_RADIUS=250               # Geometric center radius
SCHEMA_REGISTRY_URL=http://localhost:52012  # Schema Registry URL
SCHEMA_VALIDATION_ENABLED=true       # Enable schema validation
```

### Express
```bash
PORT=3000                            # HTTP server port
GO_HUB_URL=http://localhost:52015    # Go hub URL (single source of truth)
STREAM_INTERVAL=500                  # Polling interval (ms)
CORS_ORIGIN=*                        # CORS allowed origins
```

---

## Docker Deployment

```yaml
# docker-compose.yml
version: '3.8'

services:
  topology-hub:
    build: ./topology-hub
    ports:
      - "52015:52015"
    environment:
      - PORT=52015
      - SCHEMA_REGISTRY_URL=http://schema-registry:52012
    depends_on:
      - schema-registry

  topology-hub-express:
    build: ./topology-hub-express
    ports:
      - "3000:3000"
    environment:
      - PORT=3000
      - GO_HUB_URL=http://topology-hub:52015
    depends_on:
      - topology-hub
```

```bash
docker-compose up -d
```

---

## Key Concepts

### Dependency-Aware Health

**Scenario**: Event-Bus goes down

```
Event-Bus (DOWN)
    ▼
Perception (required dependency) → DEGRADED
    ▼
Reasoning-Engine (required dependency) → DEGRADED
    ▼
System Dashboard (required dependency) → DEGRADED
```

### Schema Validation

Topology Hub validates service schema versions against Schema Registry:

```bash
# Service reports schema version
curl -X POST http://localhost:52015/report -d '{
  "id": "perception",
  "metadata": {"schema_version": "1.0.0"}
}'

# Hub validates against Schema Registry
# → GET http://schema-registry:52012/api/v1/schemas/perception/versions/1.0.0

# Check validation status
curl http://localhost:52015/topology/validate
```

### Single Source of Truth

**CORRECT** ✅:
```
Go Hub → Express → Frontend
(authoritative state)
```

**WRONG** ❌:
```
Go Hub → Express (separate state) → Frontend
         ↑
     State Drift!
```

---

## Next Steps

1. **Integrate Services**: Add topology reporting to your services
2. **Build Dashboard**: Connect frontend to Express Socket.IO
3. **Set Up Alerts**: Monitor `/topology/validate` for critical issues
4. **Configure Dependencies**: Define required vs optional dependencies
5. **Enable Schema Validation**: Connect to Schema Registry

---

## Resources

- **Full Documentation**: [ENTERPRISE_IMPLEMENTATION_COMPLETE.md](./ENTERPRISE_IMPLEMENTATION_COMPLETE.md)
- **API Reference**: [README.md](./README.md)
- **Schema Registry**: [../schema-registry/](../schema-registry/)
- **Event Bus**: [../event-bus/](../event-bus/)

---

**Questions?** Check the full documentation or examine the codebase.

