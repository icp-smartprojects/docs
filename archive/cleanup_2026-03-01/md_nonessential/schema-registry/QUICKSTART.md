# Schema Registry - Quick Start Guide

## Installation

```bash
cd schema-registry
go mod tidy
go build -o schema-registry ./src
./schema-registry
```

Server starts on port `52053`

## Health Check

```bash
curl http://localhost:52053/health
# {"status":"healthy","service":"schema-registry","version":"1.0.0"}
```

## Basic Workflow

### 1. Register a DRAFT Schema

```bash
curl -X POST http://localhost:52053/api/v1/schemas \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "event.market.price_update",
    "namespace": "market",
    "version": "1.0.0",
    "schema_type": "json",
    "schema": "{\"type\":\"object\",\"properties\":{\"symbol\":{\"type\":\"string\"},\"price\":{\"type\":\"number\"},\"timestamp\":{\"type\":\"integer\"}},\"required\":[\"symbol\",\"price\",\"timestamp\"]}",
    "owner_service": "market-ingestion",
    "compatibility_mode": "BACKWARD",
    "description": "Price update events from exchanges"
  }'
```

**Response:**
```json
{
  "id": "sch_123",
  "subject": "event.market.price_update",
  "namespace": "market",
  "version": "1.0.0",
  "status": "DRAFT",
  "schema_type": "json",
  "compatibility_mode": "BACKWARD",
  "owner_service": "market-ingestion",
  "hash": "a1b2c3d4...",
  "created_at": "2024-01-15T10:00:00Z"
}
```

### 2. Approve Schema (DRAFT → ACTIVE)

```bash
curl -X POST http://localhost:52053/api/v1/schemas/event.market.price_update/approve \
  -H "Content-Type: application/json" \
  -d '{
    "requested_by": "market-ingestion-team",
    "justification": "Initial schema for real-time price updates from Binance/Coinbase"
  }'
```

**Response:**
```json
{
  "schema_id": "event.market.price_update",
  "approved": true,
  "approved_by": "market-ingestion-team",
  "approved_at": "2024-01-15T10:05:00Z",
  "previous_status": "DRAFT",
  "new_status": "ACTIVE"
}
```

### 3. Validate Data Against Schema

```bash
curl -X POST http://localhost:52053/api/v1/enforce/event \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "price.update",
    "payload": "{\"symbol\":\"BTC/USD\",\"price\":42350.50,\"timestamp\":1705315200}"
  }'
```

**Valid Response:**
```json
{
  "valid": true,
  "schema_id": "event.market.price_update",
  "schema_version": "1.0.0",
  "schema_status": "ACTIVE",
  "enforced_at": "2024-01-15T10:10:00Z",
  "enforcement_time_ms": 1.2
}
```

**Invalid Response:**
```json
{
  "valid": false,
  "errors": [
    {
      "code": "VALIDATION_FAILED",
      "message": "Missing required field: timestamp",
      "field": "timestamp"
    }
  ],
  "enforced_at": "2024-01-15T10:10:00Z",
  "enforcement_time_ms": 0.8
}
```

### 4. Analyze Impact Before Change

```bash
curl -X POST http://localhost:52053/api/v1/schemas/event.market.price_update/impact \
  -H "Content-Type: application/json" \
  -d '{
    "new_schema": "{\"type\":\"object\",\"properties\":{\"symbol\":{\"type\":\"string\"},\"price\":{\"type\":\"number\"},\"timestamp\":{\"type\":\"integer\"},\"exchange_fee\":{\"type\":\"number\"}},\"required\":[\"symbol\",\"price\",\"timestamp\"]}"
  }'
```

**Response:**
```json
{
  "affected_services": ["price-observer", "reasoning-engine"],
  "breaking_changes": [],
  "severity": "LOW",
  "compatible": true,
  "rollout_plan": {
    "phases": [
      {
        "name": "Phase 1 - Canary",
        "services": ["market-ingestion"],
        "percentage": 10,
        "duration_minutes": 30
      },
      {
        "name": "Phase 2 - Rollout",
        "services": ["price-observer"],
        "percentage": 50,
        "duration_minutes": 60
      },
      {
        "name": "Phase 3 - Full Deployment",
        "services": ["reasoning-engine"],
        "percentage": 100,
        "duration_minutes": 120
      }
    ]
  }
}
```

### 5. Get Schema Lifecycle Status

```bash
curl http://localhost:52053/api/v1/schemas/event.market.price_update/lifecycle
```

**Response:**
```json
{
  "current_status": "ACTIVE",
  "created_at": "2024-01-15T10:00:00Z",
  "approved_at": "2024-01-15T10:05:00Z",
  "approved_by": "market-ingestion-team",
  "allowed_actions": ["deprecate"],
  "forbidden_actions": ["approve", "retire", "modify", "delete"],
  "next_states": ["DEPRECATED"],
  "is_immutable": true
}
```

### 6. Deprecate Schema

```bash
curl -X POST http://localhost:52053/api/v1/schemas/event.market.price_update/deprecate
```

**Response:**
```json
{
  "subject": "event.market.price_update",
  "status": "deprecated",
  "deprecated_at": "2024-02-01T10:00:00Z",
  "message": "Schema marked as deprecated"
}
```

### 7. Retire Schema

```bash
curl -X POST http://localhost:52053/api/v1/schemas/event.market.price_update/retire \
  -H "Content-Type: application/json" \
  -d '{
    "retired_by": "platform-team",
    "reason": "Migrated to event.market.price_update_v2 with improved structure"
  }'
```

**Response:**
```json
{
  "subject": "event.market.price_update",
  "status": "retired",
  "retired_by": "platform-team",
  "retired_at": "2024-03-01T10:00:00Z",
  "reason": "Migrated to event.market.price_update_v2 with improved structure"
}
```

## Common Patterns

### Pattern 1: Version Pinning (Production)

Services should pin exact schema versions:

```bash
# Pin to specific version
curl -X POST http://localhost:52053/api/v1/enforce/event \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "price.update",
    "payload": "{\"symbol\":\"BTC/USD\",\"price\":42350.50,\"timestamp\":1705315200}",
    "version": "1.0.0",
    "enforce_hash": true,
    "expected_hash": "a1b2c3d4..."
  }'
```

### Pattern 2: Schema Evolution (Non-Breaking)

Adding optional fields:

```bash
# Step 1: Analyze impact
curl -X POST http://localhost:52053/api/v1/schemas/event.market.price_update/impact \
  -d '{...new schema with optional field...}'

# Step 2: Register new version as DRAFT
curl -X POST http://localhost:52053/api/v1/schemas \
  -d '{
    "subject": "event.market.price_update",
    "version": "1.1.0",
    "schema": "{...with new optional field...}",
    ...
  }'

# Step 3: Approve new version
curl -X POST http://localhost:52053/api/v1/schemas/event.market.price_update/approve \
  -d '{"requested_by":"...", "justification":"..."}'

# Step 4: Gradual rollout (services update to 1.1.0 over time)
```

### Pattern 3: Breaking Changes

Require new major version:

```bash
# Step 1: Register breaking change as new major version
curl -X POST http://localhost:52053/api/v1/schemas \
  -d '{
    "subject": "event.market.price_update_v2",
    "version": "2.0.0",
    "schema": "{...breaking changes...}",
    "migrates_from": "event.market.price_update@1.x.x",
    ...
  }'

# Step 2: Approve v2
curl -X POST http://localhost:52053/api/v1/schemas/event.market.price_update_v2/approve \
  -d '{...}'

# Step 3: Dual-write period (services write to both v1 and v2)
# Step 4: Migrate consumers to v2
# Step 5: Deprecate v1
curl -X POST http://localhost:52053/api/v1/schemas/event.market.price_update/deprecate

# Step 6: After grace period, retire v1
curl -X POST http://localhost:52053/api/v1/schemas/event.market.price_update/retire \
  -d '{"retired_by":"...", "reason":"Migrated to v2"}'
```

### Pattern 4: Testing with DRAFT Schemas

```bash
curl -X POST http://localhost:52053/api/v1/enforce/event \
  -d '{
    "event_type": "price.update",
    "payload": "{...}",
    "allow_draft": true
  }'
```

**Note**: Production systems should NEVER set `allow_draft: true`

## Enforcement Metrics

```bash
curl http://localhost:52053/api/v1/enforce/metrics
```

**Response:**
```json
{
  "total_enforcements": 152340,
  "successful_enforcements": 151000,
  "failed_enforcements": 1340,
  "success_rate": 99.12,
  "violations_by_code": {
    "SCHEMA_NOT_FOUND": 450,
    "VALIDATION_FAILED": 670,
    "SCHEMA_INACTIVE": 120,
    "HASH_MISMATCH": 100
  },
  "violations_by_subject": {
    "event.market.price_update": 230,
    "api.gateway.request": 150,
    "event.reasoning.decision": 80
  }
}
```

## Schema Categories

### EVENT Schemas (Event Bus)

```bash
# Subject pattern: event.<namespace>.<event_type>
curl -X POST http://localhost:52053/api/v1/schemas \
  -d '{
    "subject": "event.market.price_update",
    "namespace": "market",
    "category": "EVENT",
    ...
  }'
```

### ENTITY Schemas (Domain Objects)

```bash
# Subject pattern: entity.<namespace>.<entity_type>
curl -X POST http://localhost:52053/api/v1/schemas \
  -d '{
    "subject": "entity.market.instrument",
    "namespace": "market",
    "category": "ENTITY",
    ...
  }'
```

### API Schemas (Request/Response)

```bash
# Subject pattern: api.<service>.<endpoint>
curl -X POST http://localhost:52053/api/v1/schemas \
  -d '{
    "subject": "api.gateway.price_query",
    "namespace": "gateway",
    "category": "API",
    ...
  }'
```

### PERSISTENCE Schemas (Database)

```bash
# Subject pattern: persistence.<namespace>.<table>
curl -X POST http://localhost:52053/api/v1/schemas \
  -d '{
    "subject": "persistence.market.candles",
    "namespace": "market",
    "category": "PERSISTENCE",
    ...
  }'
```

## Error Codes

| Code | Meaning | Fix |
|------|---------|-----|
| `SCHEMA_NOT_FOUND` | Schema doesn't exist | Register schema first |
| `SCHEMA_INACTIVE` | Schema not ACTIVE | Approve schema or check lifecycle status |
| `VALIDATION_FAILED` | Data doesn't match schema | Fix payload structure |
| `VERSION_MISMATCH` | Requested version doesn't exist | Check available versions |
| `HASH_MISMATCH` | Schema content tampered | Security incident - investigate |
| `UNKNOWN_SCHEMA_TYPE` | Unsupported schema type | Use json/protobuf/avro |

## Best Practices

1. **Version Pinning**: Always pin exact versions in production
2. **Hash Verification**: Enable `enforce_hash: true` for critical systems
3. **Gradual Rollout**: Use impact analysis and rollout plans for changes
4. **Non-Breaking Changes**: Add optional fields, don't remove existing ones
5. **Breaking Changes**: Create new major version with migration plan
6. **Governance**: Always provide justification for schema approvals
7. **Monitoring**: Track enforcement metrics, alert on violations
8. **Documentation**: Include description and tags on all schemas
9. **Ownership**: Set `owner_service` for accountability
10. **Compatibility**: Choose appropriate compatibility mode (BACKWARD recommended)

## Integration Examples

### Event Bus Integration

```go
// Before publishing event
result, err := schemaRegistry.EnforceEvent(ctx, eventType, payload)
if err != nil {
    return fmt.Errorf("enforcement failed: %w", err)
}
if !result.Valid {
    return &SchemaViolationError{Errors: result.Errors}
}

// Add schema metadata
event.SchemaID = result.SchemaID
event.SchemaVersion = result.SchemaVersion
event.SchemaHash = result.Hash

// Publish
eb.publish(ctx, event)
```

### Service Consumer Integration

```go
// Pin schema version at service startup
const PRICE_UPDATE_SCHEMA_VERSION = "1.0.0"

// Validate consumed events
result, err := schemaRegistry.Enforce(ctx, &EnforceRequest{
    Subject: "event.market.price_update",
    Version: PRICE_UPDATE_SCHEMA_VERSION,
    Data: payload,
    EnforceHash: true,
})
```

## Troubleshooting

### Problem: Schema validation fails but data looks correct

**Check:**
1. Schema is ACTIVE: `GET /schemas/{subject}/lifecycle`
2. Using correct version: `GET /schemas/{subject}/versions`
3. Data matches JSON schema exactly (types, required fields)

### Problem: Cannot modify schema

**Reason:** Schemas are immutable once ACTIVE

**Solution:**
1. For non-breaking changes: Create new minor version (1.0.0 → 1.1.0)
2. For breaking changes: Create new major version (1.x.x → 2.0.0)

### Problem: Hash mismatch error

**Reason:** Schema content has been tampered with or modified

**Action:**
1. SECURITY INCIDENT - investigate immediately
2. Check schema content integrity
3. Verify schema hash matches expected value
4. Do NOT bypass - this protects against corruption

## Next: Event Bus Integration

Schema Registry is ready. Next steps:

1. Integrate enforcement into Event Bus (validate before publish)
2. Update services to pin schema versions
3. Add schema hash to event metadata
4. Monitor enforcement metrics
5. Set up alerts for violations

See: `/documentation/MASTER_LAUNCH_GUIDE.md` for full deployment sequence
