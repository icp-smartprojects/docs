# Gateway - Quick Start Guide

## Installation

```bash
cd gateway
go mod tidy
go build -o gateway ./src
./gateway
```

Server starts on port `52031`

## Health Check

```bash
curl http://localhost:52031/health
# {"status":"healthy","service":"api-gateway"}
```

## Authentication

### Login

```bash
curl -X POST http://localhost:52031/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "trader1",
    "password": "password123"
  }'
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user_id": "user_123",
  "role": "trader",
  "permissions": ["shapes.create", "shapes.read", "market.read"]
}
```

### Using Token

```bash
export TOKEN="eyJhbGciOiJIUzI1NiIs..."

curl http://localhost:52031/api/v1/semantic/state \
  -H "Authorization: Bearer $TOKEN"
```

## Correlation Tracking

Every request receives correlation headers:

```bash
curl -v http://localhost:52031/health
```

**Response Headers:**
```
X-Correlation-ID: 550e8400-e29b-41d4-a716-446655440000
X-Causation-ID: 550e8400-e29b-41d4-a716-446655440001
X-Request-ID: 550e8400-e29b-41d4-a716-446655440002
X-Service-Name: api-gateway
```

Use these IDs to track requests across services.

## Policy Enforcement

### Allowed Action

```bash
curl -X POST http://localhost:52031/api/v1/shape-engine/shapes \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "support_resistance",
    "timeframe": "1h",
    "parameters": {...}
  }'
```

**Success (200 OK)**:
```json
{
  "shape_id": "shape_789",
  "status": "created",
  "correlation_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Denied Action

```bash
curl -X POST http://localhost:52031/api/v1/core-brain/decision/shape \
  -H "Authorization: Bearer $REGULAR_USER_TOKEN"
```

**Policy Denial (403 Forbidden)**:
```json
{
  "error": "policy_violation",
  "message": "User lacks required permission for decision execution",
  "action": "decision.execute",
  "resource": "decisions",
  "violations": ["missing_permission:decisions.execute"]
}
```

## Automation Requests

Automation MUST:
1. Have SYSTEM role
2. Declare intent
3. Be reversible

```bash
curl -X POST http://localhost:52031/api/v1/core-brain/decision/shape \
  -H "Authorization: Bearer $SYSTEM_TOKEN" \
  -H "X-Automation-Source: core-brain" \
  -H "X-Automation-Intent: Execute automated shape decision" \
  -H "X-Automation-Reversible: true" \
  -H "Content-Type: application/json" \
  -d '{...}'
```

**Invalid Automation (Missing Intent)**:
```bash
curl -X POST http://localhost:52031/api/v1/core-brain/decision/shape \
  -H "Authorization: Bearer $SYSTEM_TOKEN" \
  -H "X-Automation-Source: core-brain"
```

**Response (400 Bad Request)**:
```json
{
  "error": "validation_error",
  "message": "Automation must declare intent",
  "field": "header",
  "details": "X-Automation-Intent is required for automated actions"
}
```

## Simulation Requests

Simulation MUST:
1. Declare intent
2. Include time window
3. Include constraints

```bash
curl -X GET http://localhost:52031/api/v1/dream/scenarios \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Simulation-Intent: Test portfolio rebalancing strategy" \
  -H "X-Simulation-Time-Window: 2024-01-01T00:00:00Z/2024-01-07T00:00:00Z" \
  -H 'X-Simulation-Constraints: {"max_drawdown":0.05,"position_limit":10}'
```

**Missing Constraints (400 Bad Request)**:
```json
{
  "error": "validation_error",
  "message": "Simulation must declare constraints",
  "field": "header",
  "details": "X-Simulation-Constraints is required (JSON)"
}
```

## Rate Limiting

Default: 100 requests per minute per user (or IP if unauthenticated)

```bash
# Make 101 requests in quick succession
for i in {1..101}; do
  curl http://localhost:52031/api/v1/semantic/state \
    -H "Authorization: Bearer $TOKEN"
done
```

**Rate Limit Exceeded (429 Too Many Requests)**:
```json
{
  "error": "rate_limit_exceeded",
  "message": "Too many requests. Limit: 100 per minute",
  "retry_after": 60
}
```

**Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
Retry-After: 60
```

## Request Validation

### Valid Request

```bash
curl -X POST http://localhost:52031/api/v1/data/upload \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "file_name": "market_data.csv",
    "file_size": 1024000,
    "file_type": "text/csv"
  }'
```

### Invalid JSON

```bash
curl -X POST http://localhost:52031/api/v1/data/upload \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{invalid json'
```

**Response (400 Bad Request)**:
```json
{
  "error": "validation_error",
  "message": "Invalid JSON",
  "field": "body",
  "details": "invalid character 'i' looking for beginning of object key string"
}
```

### Body Too Large

```bash
# Send 11MB file (limit is 10MB)
dd if=/dev/zero bs=1M count=11 | \
curl -X POST http://localhost:52031/api/v1/data/upload \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  --data-binary @-
```

**Response (400 Bad Request)**:
```json
{
  "error": "validation_error",
  "message": "Request body exceeds maximum size of 10485760 bytes",
  "field": "body",
  "details": "Received 11534336 bytes"
}
```

## Schema Version Validation

```bash
# Missing schema version
curl -X POST http://localhost:52031/api/v1/shape-engine/shapes \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{...}'
```

**Response (400 Bad Request)**:
```json
{
  "error": "validation_error",
  "message": "Missing schema version header",
  "field": "header",
  "details": "X-Schema-Version is required"
}
```

**Correct Usage**:
```bash
curl -X POST http://localhost:52031/api/v1/shape-engine/shapes \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "X-Schema-Version: 1.0.0" \
  -d '{...}'
```

## Frontend Isolation

Frontend CANNOT:
- Set X-Internal-Service-Call header
- Access internal service endpoints directly

```bash
# Frontend trying to bypass gateway
curl http://localhost:52031/internal/service/endpoint \
  -H "Origin: https://frontend.example.com" \
  -H "X-Internal-Service-Call: true"
```

**Response (403 Forbidden)**:
```json
{
  "error": "forbidden",
  "message": "Frontend cannot make internal service calls"
}
```

## Event Bus Audit Trail

Gateway emits events to Event Bus for:
- `request.received` - Every request
- `request.allowed` - Auth + policy passed
- `request.denied` - Auth or policy failed
- `request.forwarded` - Proxied to backend
- `request.failed` - Request failed
- `request.completed` - Request succeeded

**Event Example** (request.completed):
```json
{
  "event_type": "request.completed",
  "timestamp": "2024-01-15T10:30:00Z",
  "correlation": {
    "correlation_id": "550e8400-e29b-41d4-a716-446655440000",
    "causation_id": "550e8400-e29b-41d4-a716-446655440001",
    "request_id": "550e8400-e29b-41d4-a716-446655440002",
    "user_id": "user_123"
  },
  "request": {
    "method": "POST",
    "path": "/api/v1/shape-engine/shapes",
    "user_id": "user_123",
    "role": "trader",
    "client_ip": "192.168.1.100",
    "user_agent": "Mozilla/5.0..."
  },
  "response": {
    "status_code": 200,
    "duration_ms": 45,
    "body_size_bytes": 1024
  }
}
```

## Observability

### Prometheus Metrics

```bash
curl http://localhost:52031/metrics
```

**Metrics Exported**:
- `http_requests_total{method, path, status}` - Total requests
- `http_request_duration_seconds{method, path}` - Request latency
- `http_requests_in_flight` - Current in-flight requests
- `gateway_policy_denials_total{action, resource}` - Policy denials
- `gateway_auth_failures_total{reason}` - Auth failures
- `gateway_rate_limit_exceeded_total` - Rate limit violations

### Logs

Gateway logs all requests with correlation IDs:

```
2024-01-15T10:30:00Z INFO HTTP request method=POST path=/api/v1/shape-engine/shapes duration_ms=45 correlation_id=550e8400-e29b-41d4-a716-446655440000
2024-01-15T10:30:01Z WARN Policy denied action=simulation.start resource=simulation reason="User lacks permission" user_id=user_123
2024-01-15T10:30:02Z ERROR Request failed path=/api/v1/data/upload error="upstream service unavailable" correlation_id=550e8400-e29b-41d4-a716-446655440003
```

## Common Endpoints

### Health & Readiness

```bash
# Health check (always 200)
curl http://localhost:52031/health

# Liveness probe
curl http://localhost:52031/healthz

# Readiness probe (checks backend services)
curl http://localhost:52031/ready
```

### Authentication

```bash
# Login
POST /api/v1/auth/login

# Logout
POST /api/v1/auth/logout

# Refresh token
POST /api/v1/auth/refresh

# Get current user
GET /api/v1/auth/me
```

### Data Ingestion

```bash
# Upload file
POST /api/v1/data/upload

# Bulk upload
POST /api/v1/data/upload/bulk

# List uploads
GET /api/v1/data/uploads

# Queue ingestion
POST /api/v1/data/ingest

# Get ingestion status
GET /api/v1/data/ingest/:ingestion_id/status
```

### Shapes

```bash
# Create shape (requires policy: shape.draw)
POST /api/v1/shape-engine/shapes

# List shapes
GET /api/v1/shape-engine/shapes

# Get shape details
GET /api/v1/shape-engine/shapes/:shape_id
```

### Decisions

```bash
# Execute decision (requires policy: decision.execute)
POST /api/v1/core-brain/decision/shape
```

### Simulation

```bash
# Get scenarios (requires policy: simulation.start)
GET /api/v1/dream/scenarios
```

### WebSocket

```bash
# Connect to WebSocket (requires auth + policy: websocket.connect)
ws://localhost:52031/ws/events
```

## Error Handling

Gateway standardizes all errors:

```json
{
  "error": "error_code",
  "message": "Human-readable message",
  "field": "field_name",  // Optional
  "details": "Additional context"  // Optional
}
```

**Error Codes**:
- `unauthorized` - Missing or invalid token (401)
- `forbidden` - Insufficient permissions (403)
- `policy_violation` - Policy Engine denied action (403)
- `validation_error` - Invalid request (400)
- `rate_limit_exceeded` - Too many requests (429)
- `internal_error` - Server error (500)
- `service_unavailable` - Backend service down (503)
- `circuit_open` - Circuit breaker open (503)

## Integration Examples

### Service Consumer (with correlation)

```go
func callGateway(endpoint string, payload interface{}) (*Response, error) {
    // Build request
    body, _ := json.Marshal(payload)
    req, _ := http.NewRequest("POST", "http://gateway:52031"+endpoint, bytes.NewReader(body))
    
    // Add auth
    req.Header.Set("Authorization", "Bearer "+token)
    
    // Add correlation (if in request chain)
    if correlationID != "" {
        req.Header.Set("X-Correlation-ID", correlationID)
    }
    
    // Execute
    resp, err := httpClient.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    
    // Extract correlation from response
    respCorrelationID := resp.Header.Get("X-Correlation-ID")
    log.Printf("Request correlation: %s", respCorrelationID)
    
    return parseResponse(resp)
}
```

### Automation Client

```go
func executeAutomation(action string, payload interface{}) error {
    req, _ := http.NewRequest("POST", "http://gateway:52031"+action, ...)
    
    // SYSTEM token (not user token)
    req.Header.Set("Authorization", "Bearer "+systemToken)
    
    // Automation headers (REQUIRED)
    req.Header.Set("X-Automation-Source", "core-brain")
    req.Header.Set("X-Automation-Intent", "Execute automated shape decision")
    req.Header.Set("X-Automation-Reversible", "true")
    
    resp, err := httpClient.Do(req)
    if err != nil {
        return err
    }
    
    if resp.StatusCode == 403 {
        return errors.New("Automation denied by policy")
    }
    
    return nil
}
```

## Troubleshooting

### Problem: 401 Unauthorized

**Reasons**:
1. Missing Authorization header
2. Invalid token format (not "Bearer <token>")
3. Expired token
4. Invalid signature

**Fix**: Login again to get fresh token

### Problem: 403 Forbidden (Policy Violation)

**Reasons**:
1. User lacks required permission
2. Policy Engine denied action
3. Role insufficient for endpoint

**Fix**: Check user permissions, verify policy rules

### Problem: 429 Rate Limit Exceeded

**Reasons**:
1. Too many requests in short time
2. Runaway automation
3. Infinite loop in client

**Fix**: Wait for retry-after period, fix client code

### Problem: 400 Validation Error

**Reasons**:
1. Invalid JSON
2. Missing required fields
3. Body too large
4. Wrong Content-Type

**Fix**: Validate request structure, check schema

### Problem: Missing Correlation ID

**Reason**: Request not going through Gateway

**Fix**: Ensure all requests go through `http://gateway:52031`

## Security Best Practices

1. **Never hardcode tokens**: Use environment variables
2. **Always use HTTPS in production**: TLS encryption
3. **Rotate tokens regularly**: Implement refresh token flow
4. **Validate on frontend AND gateway**: Defense in depth
5. **Monitor rate limits**: Alert on unusual patterns
6. **Track correlation IDs**: Essential for debugging
7. **Use SYSTEM role sparingly**: Only for automation
8. **Declare automation intent**: Explain what automation does
9. **Make automation reversible**: Always have rollback plan
10. **Check policy before action**: Don't assume permissions

## Next Steps

1. **Integrate Event Bus**: Consume gateway audit events
2. **Set up Policy Engine**: Define authorization rules
3. **Configure monitoring**: Prometheus dashboards
4. **Enable TLS**: Install certificates for production
5. **Tune rate limits**: Adjust per user role/tier
6. **Add custom validators**: Domain-specific validation rules
7. **Implement circuit breakers**: Per-service fault tolerance

See: `/documentation/MASTER_LAUNCH_GUIDE.md` for full deployment sequence
