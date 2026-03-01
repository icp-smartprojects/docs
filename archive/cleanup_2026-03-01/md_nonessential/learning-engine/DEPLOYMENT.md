# Learning Engine - Deployment & Operations Guide

## 🚀 Quick Start

### Local Development

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set environment variables
export PORT=52004
export DEBUG=true
export REDIS_HOST=localhost
export NEO4J_URI=bolt://localhost:7687

# 3. Run the service
python src/main.py
```

### Docker Deployment

```bash
# Build image
docker build -t learning-engine:1.0 .

# Run container
docker run -d \
  --name learning-engine \
  -p 52004:52004 \
  -e REDIS_HOST=redis \
  -e NEO4J_URI=bolt://neo4j:7687 \
  learning-engine:1.0
```

### Kubernetes Deployment

```bash
# Create namespace
kubectl create namespace cognitive-system

# Deploy using kubectl
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Or using Helm
helm install learning-engine helm/ \
  --namespace cognitive-system \
  --set redis.auth.password=your-redis-password \
  --set neo4j.neo4j.password=your-neo4j-password
```

---

## 📊 Health Monitoring

### Health Check Endpoint

```bash
curl http://localhost:52004/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "learning-engine",
  "port": 52004,
  "timestamp": "2025-01-03T12:00:00.000000"
}
```

### Statistics Endpoint

```bash
curl http://localhost:52004/api/v1/stats/all
```

Returns comprehensive statistics from all learning modules.

---

## 🧪 Testing the Learning Engine

### 1. Supervised Learning Test

```python
import requests

# Add an example
response = requests.post(
    "http://localhost:52004/api/v1/supervised/examples/add",
    json={
        "example_id": "test_1",
        "concept_label": "bullish_fvg",
        "structural_features": {
            "invariants": ["gap_up", "volume_increase"],
            "geometric_properties": {"ratio": 0.618},
            "temporal_properties": {"duration": 15}
        },
        "semantic_context": {
            "domain": "trading",
            "timeframe": "M15",
            "context_metadata": {}
        },
        "confidence": 0.85,
        "quality_score": 0.9
    }
)

print(response.json())
```

### 2. Few-Shot Learning Test

```python
# Learn from few examples
examples = [
    # ... create 3-5 similar examples
]

response = requests.post(
    "http://localhost:52004/api/v1/supervised/few-shot/learn",
    json=examples
)

# Make prediction
response = requests.post(
    "http://localhost:52004/api/v1/supervised/few-shot/predict",
    json={
        "invariants": ["gap_up", "volume_increase"],
        "properties": {"ratio": 0.62}
    }
)

print(response.json())
```

### 3. Reinforcement Learning Test

```python
# Report successful outcome
outcome = {
    "outcome_id": "trade_1",
    "action_taken": "enter_long",
    "result": "success",
    "success_degree": 0.8,
    "concepts_validated": ["bullish_fvg"],
    "concepts_invalidated": [],
    "context": {"instrument": "EURUSD", "timeframe": "M15"},
    "confidence_in_outcome": 0.9,
    "domain": "trading"
}

response = requests.post(
    "http://localhost:52004/api/v1/reinforcement/outcome/learn",
    json=outcome
)
```

### 4. Punishment Test

```python
# Report failed outcome
failed_outcome = {
    "outcome_id": "trade_2",
    "action_taken": "enter_short",
    "result": "failure",
    "success_degree": -0.5,
    "concepts_validated": [],
    "concepts_invalidated": ["false_breakout"],
    "context": {"instrument": "EURUSD", "timeframe": "M15"},
    "confidence_in_outcome": 0.85,
    "domain": "trading"
}

response = requests.post(
    "http://localhost:52004/api/v1/punishment/apply",
    json=failed_outcome
)

print(response.json()["counterfactual"])
```

### 5. Active Learning Test

```python
# Detect uncertainty
response = requests.post(
    "http://localhost:52004/api/v1/active/uncertainty/detect",
    json={
        "prediction_scores": {
            "pattern_a": 0.45,
            "pattern_b": 0.42,
            "pattern_c": 0.40
        },
        "context": {"timeframe": "M15"}
    }
)

if response.json()["uncertain"]:
    query = response.json()["query"]
    print(f"Question: {query['question']}")
    print(f"Options: {query['options']}")
```

### 6. Meta Learning Test

```python
# Run pattern discovery
examples = [
    # ... 10+ examples with recurring patterns
]

response = requests.post(
    "http://localhost:52004/api/v1/meta/discover",
    json=examples
)

print(f"Discovered {response.json()['patterns_discovered']} patterns")
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 52004 | Service port |
| `DEBUG` | false | Debug mode |
| `LOG_LEVEL` | INFO | Logging level |
| `REDIS_HOST` | localhost | Redis host |
| `REDIS_PORT` | 6379 | Redis port |
| `NEO4J_URI` | bolt://localhost:7687 | Neo4j connection |
| `LEARNING_RATE_SUPERVISED` | 0.2 | Supervised learning rate |
| `LEARNING_RATE_REINFORCEMENT` | 0.15 | RL learning rate |
| `LEARNING_RATE_PUNISHMENT` | 0.25 | Punishment learning rate |
| `PUNISHMENT_DECAY_RATE` | 0.8 | Confidence decay on failure |
| `MIN_EXAMPLES_FOR_GENERALIZATION` | 3 | Minimum examples for few-shot |
| `FEW_SHOT_K` | 5 | Number of examples to use |
| `UNCERTAINTY_THRESHOLD` | 0.5 | Uncertainty detection threshold |
| `HYPOTHESIS_MIN_SUPPORT` | 5 | Minimum support for hypothesis |

---

## 📈 Scaling Guidelines

### Vertical Scaling
- **CPU**: 500m - 2000m per pod
- **Memory**: 1Gi - 4Gi per pod
- Adjust based on:
  - Number of concurrent learning operations
  - Size of knowledge graph
  - Pattern discovery workload

### Horizontal Scaling
- **Min Replicas**: 2 (for HA)
- **Max Replicas**: 10
- **Scale triggers**:
  - CPU > 70%
  - Memory > 80%
  - Custom: Learning queue depth

### Database Scaling
- **Redis**: 8Gi minimum for caching
- **Neo4j**: 20Gi minimum for knowledge graph
- Monitor graph size and adjust storage

---

## 🔒 Security Best Practices

### 1. Secrets Management
```bash
# Create secrets for production
kubectl create secret generic redis-secret \
  --from-literal=password='strong-redis-password' \
  -n cognitive-system

kubectl create secret generic neo4j-secret \
  --from-literal=password='strong-neo4j-password' \
  -n cognitive-system
```

### 2. Network Policies
- Enable network policies in Helm values
- Restrict ingress to API gateway only
- Restrict egress to Redis and Neo4j

### 3. RBAC
- Use dedicated service account
- Minimal required permissions
- Regular audit of access logs

---

## 🐛 Troubleshooting

### Service Won't Start

```bash
# Check logs
kubectl logs -f deployment/learning-engine -n cognitive-system

# Check dependencies
kubectl get pods -n cognitive-system | grep -E 'redis|neo4j'

# Verify secrets
kubectl get secrets -n cognitive-system
```

### High Memory Usage

```bash
# Check current usage
kubectl top pods -n cognitive-system | grep learning-engine

# Check statistics endpoint
curl http://localhost:52004/api/v1/stats/all

# Possible causes:
# - Large knowledge graph (too many concepts)
# - Too many cached examples
# - Memory leak in pattern discovery

# Solutions:
# - Increase memory limits
# - Clear old examples periodically
# - Tune cache eviction policies
```

### Slow Learning Performance

```bash
# Check learning statistics
curl http://localhost:52004/api/v1/stats/all | jq '.supervised'

# Possible causes:
# - Too many examples (>10,000)
# - Complex pattern discovery (>1000 patterns)
# - Slow Redis/Neo4j

# Solutions:
# - Prune low-quality examples
# - Increase MIN_EXAMPLES_FOR_GENERALIZATION
# - Scale Redis/Neo4j
```

---

## 📊 Monitoring Metrics

### Key Metrics to Track

1. **Learning Performance**
   - Examples processed/second
   - Patterns discovered/hour
   - Hypotheses validated/day

2. **Accuracy Metrics**
   - Few-shot prediction accuracy
   - Policy success rate
   - Hypothesis support rate

3. **System Health**
   - API latency (p50, p95, p99)
   - Memory usage
   - CPU utilization
   - Redis/Neo4j connection pool

4. **Business Metrics**
   - Total knowledge base size
   - Learning cycles completed
   - Active learning queries generated

---

## 🔄 Backup & Recovery

### Knowledge Graph Backup

```bash
# Backup Neo4j
kubectl exec -it neo4j-0 -n cognitive-system -- \
  neo4j-admin dump --database=neo4j --to=/backups/neo4j-backup.dump

# Restore Neo4j
kubectl exec -it neo4j-0 -n cognitive-system -- \
  neo4j-admin load --database=neo4j --from=/backups/neo4j-backup.dump
```

### Redis Backup

```bash
# Trigger Redis save
kubectl exec -it redis-master-0 -n cognitive-system -- redis-cli SAVE

# Copy RDB file
kubectl cp cognitive-system/redis-master-0:/data/dump.rdb ./redis-backup.rdb
```

---

## 📚 API Documentation

Full API documentation available at:
- Swagger UI: `http://localhost:52004/docs`
- ReDoc: `http://localhost:52004/redoc`

---

## 🎯 Performance Benchmarks

Expected performance on recommended hardware:

| Operation | Latency (p95) | Throughput |
|-----------|---------------|------------|
| Add Example | <10ms | 1000/sec |
| Few-Shot Prediction | <50ms | 200/sec |
| Learn from Outcome | <20ms | 500/sec |
| Apply Punishment | <30ms | 300/sec |
| Pattern Discovery | <500ms | N/A (batch) |

---

## 🆘 Support

For issues, questions, or contributions:
- GitHub Issues: [repository-url]/issues
- Documentation: [repository-url]/docs
- Email: team@cognitive-system.ai

---

## 📝 License

MIT License - See LICENSE file for details.