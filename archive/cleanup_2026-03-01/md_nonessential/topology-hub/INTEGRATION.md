# Integration Guide: Connecting Existing Services to Topology Hub

This guide shows how to integrate existing Go, Rust, and Python services with the Central Topology Hub.

## Quick Integration (5 minutes)

### For Python Services

1. **Copy the client library**:
```bash
cp topology-hub/client_python.py your-service/
```

2. **Import and initialize**:
```python
from client_python import TopologyClient

hub = TopologyClient(
    hub_url="http://localhost:8080",
    service_id="your-service-01",
    initial_sides=4,
)
```

3. **Report capabilities when added**:
```python
@app.route("/api/feature/nlu", methods=["POST"])
def add_nlu_feature():
    hub.add_capability("natural_language_understanding")
    hub.report()
    return {"status": "nlu_enabled"}
```

4. **Start background reporting**:
```python
hub.start_periodic_reporting(interval=3.0)
```

### For Rust Services

1. **Copy the client module**:
```bash
cp topology-hub/client_rust.rs your-service/src/
```

2. **Add to Cargo.toml**:
```toml
tokio = { version = "1.0", features = ["full"] }
reqwest = { version = "0.11", features = ["json"] }
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
```

3. **Import in your service**:
```rust
mod topology;
use topology::TopologyClient;
```

4. **Initialize**:
```rust
let client = TopologyClient::new(
    "http://localhost:8080".to_string(),
    "rust-service-01".to_string(),
    6, // hexagon
);
```

5. **Report on capabilities**:
```rust
client.add_capability("async_processing".to_string()).await?;
client.report().await?;
```

### For Go Services

Use the standard `net/http` or create a wrapper around the REST API:

```go
package main

import (
    "bytes"
    "encoding/json"
    "net/http"
)

type ServiceUpdate struct {
    ID           string   `json:"id"`
    Sides        int      `json:"sides"`
    Status       string   `json:"status"`
    Scale        float64  `json:"scale"`
    Capabilities []string `json:"capabilities"`
    Connections  []map[string]interface{} `json:"connections"`
}

func reportToHub(update ServiceUpdate) error {
    body, _ := json.Marshal(update)
    resp, err := http.Post(
        "http://topology-hub:8080/report",
        "application/json",
        bytes.NewBuffer(body),
    )
    if err != nil {
        return err
    }
    defer resp.Body.Close()
    return nil
}
```

## Deep Integration Patterns

### Pattern 1: Metrics-Driven Scale

Automatically adjust the visual scale based on system metrics:

```python
import psutil

def update_scale():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_percent = psutil.virtual_memory().percent
    
    # Scale from 0.5 (idle) to 2.0 (under load)
    load = (cpu_percent + memory_percent) / 100
    scale = 0.5 + (1.5 * load)
    hub.set_scale(scale)
    hub.report()
```

### Pattern 2: Event-Driven Sides

Increment sides when new modules or features are loaded:

```python
from importlib import import_module

async def dynamic_import_module(module_name):
    try:
        module = import_module(f"features.{module_name}")
        hub.add_capability(module_name)
        hub.report()
    except ImportError:
        hub.set_status("feature_load_error")
        hub.report()
```

### Pattern 3: Connection Tracking

Automatically register connections based on actual service calls:

```python
from functools import wraps

def track_calls(target_service):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if target_service not in hub.connections:
                hub.add_connection(target_service)
                hub.report()
            return func(*args, **kwargs)
        return wrapper
    return decorator

@track_calls("knowledge-graph-01")
def query_knowledge_base(query):
    # Call knowledge graph service
    pass
```

### Pattern 4: Batch Reporting for Microservice Mesh

For systems with many small services, batch updates to reduce network overhead:

```python
services_to_report = [
    {
        "id": f"service-{i}",
        "sides": 3 + i,
        "status": "online",
        "scale": 1.0 + (i * 0.1),
        "connections": [],
        "capabilities": ["basic"],
    }
    for i in range(10)
]

hub.batch_report(services_to_report)
```

### Pattern 5: Health-Based Status

Update status based on service health checks:

```python
from enum import Enum

class ServiceStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"

async def health_check_loop():
    while True:
        checks = await run_health_checks()
        
        if all(checks.values()):
            hub.set_status(ServiceStatus.HEALTHY.value)
        elif any(checks.values()):
            hub.set_status(ServiceStatus.DEGRADED.value)
        else:
            hub.set_status(ServiceStatus.UNHEALTHY.value)
        
        hub.report()
        await asyncio.sleep(5)
```

## Docker Integration

### Example: Python Service with Hub

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY client_python.py .
COPY my_service.py .

ENV HUB_URL=http://topology-hub:8080
ENV SERVICE_ID=python-service-01

CMD ["python", "my_service.py"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  topology-hub:
    build: ./topology-hub
    ports:
      - "8080:8080"
    networks:
      - mesh

  python-service:
    build: ./python-service
    environment:
      HUB_URL: http://topology-hub:8080
    depends_on:
      - topology-hub
    networks:
      - mesh

  rust-service:
    build: ./rust-service
    environment:
      HUB_URL: http://topology-hub:8080
    depends_on:
      - topology-hub
    networks:
      - mesh

networks:
  mesh:
    driver: bridge
```

## Kubernetes Integration

### ConfigMap for Hub URL

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: topology-config
data:
  hub_url: "http://topology-hub.default.svc.cluster.local:8080"
```

### Example Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: python-service
spec:
  replicas: 2
  selector:
    matchLabels:
      app: python-service
  template:
    metadata:
      labels:
        app: python-service
    spec:
      containers:
      - name: service
        image: python-service:latest
        env:
        - name: HUB_URL
          valueFrom:
            configMapKeyRef:
              name: topology-config
              key: hub_url
        - name: SERVICE_ID
          value: $(HOSTNAME)
        lifecycle:
          preStop:
            exec:
              command: ["python", "/app/shutdown.py"]
```

## Monitoring Integration

### Prometheus Integration

Export hub metrics to Prometheus:

```go
import "github.com/prometheus/client_golang/prometheus"

var (
    servicesRegistered = prometheus.NewGauge(prometheus.GaugeOpts{
        Name: "topology_hub_services_registered",
        Help: "Number of registered services",
    })
    connectedClients = prometheus.NewGauge(prometheus.GaugeOpts{
        Name: "topology_hub_connected_clients",
        Help: "Number of connected WebSocket clients",
    })
)

func init() {
    prometheus.MustRegister(servicesRegistered)
    prometheus.MustRegister(connectedClients)
}

func updateMetrics(hub *Hub) {
    metrics := hub.GetMetrics()
    servicesRegistered.Set(float64(metrics["registered_services"].(int)))
    connectedClients.Set(float64(metrics["connected_clients"].(int)))
}
```

## Troubleshooting

### Issue: "Connection refused" to Hub

```bash
# Check if hub is running
curl -v http://localhost:8080/health

# Check from service container (Docker)
docker exec my-service curl http://topology-hub:8080/health

# Check Kubernetes service discovery
kubectl exec pod/my-service -- curl http://topology-hub:8080/health
```

### Issue: Updates not appearing

1. Verify service ID is correct
2. Check hub logs: `docker logs topology-hub | grep -i "service-id"`
3. Test manual update: `curl -X POST http://localhost:8080/report -d '{...}'`
4. Verify JSON schema matches expected format

### Issue: High latency / timeout

1. Increase report interval: `client.start_periodic_reporting(interval=5.0)`
2. Use batch updates for multiple services
3. Check network: `ping topology-hub`
4. Monitor hub metrics: `curl http://localhost:8080/metrics`

## Best Practices

1. **Use meaningful service IDs**: `python-nlp-engine-01` instead of `service1`

2. **Update scale based on real metrics**:
   - CPU usage
   - Memory usage
   - Request latency
   - Queue depth

3. **Maintain connection accuracy**: Only list actual service dependencies

4. **Use metadata for debugging**:
   ```python
   hub.set_metadata("version", "1.2.3")
   hub.set_metadata("git_commit", os.getenv("GIT_COMMIT"))
   hub.set_metadata("build_time", os.getenv("BUILD_TIME"))
   ```

5. **Graceful shutdown**: Close reports when service stops
   ```python
   signal.signal(signal.SIGTERM, lambda s, f: hub.stop_periodic_reporting())
   ```

6. **Error handling**: Topology updates should not block service logic
   ```python
   try:
       hub.report()
   except Exception as e:
       logger.warning(f"Failed to report to hub: {e}")
       # Continue running regardless
   ```

7. **Batch updates**: For systems with many services, use batch API

8. **Test with hub unavailable**: Services should work even if hub is down

## Example: Full Service Integration

See `example_complete.py` for a complete working example with 4 different service types.

Run it with:
```bash
# Terminal 1: Start hub
cd topology-hub && go run main.go hub.go api.go

# Terminal 2: Start AI service
python3 example_complete.py ai

# Terminal 3: Start knowledge graph
python3 example_complete.py kg

# Terminal 4: Start memory service
python3 example_complete.py memory

# Terminal 5: Start cache service
python3 example_complete.py cache

# Terminal 6: Monitor topology
python3 example_complete.py monitor
```

The monitor will show the topology updating in real-time as services report their capabilities.
