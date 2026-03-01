# ONTOLOGY SERVICE - ARCHITECTURE & FLOW

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     ONTOLOGY SERVICE                             │
│  (Authoritative Dictionary + Rules Engine for Meaning)           │
└─────────────────────────────────────────────────────────────────┘

                              ▲
                    ┌─────────┴─────────┐
                    │                   │
              API Layer          Event Bus
              ┌─────────┐        (Pub/Sub)
              │ FastAPI │
              └────┬────┘
                   │
    ┌──────────────┼──────────────┐
    │              │              │
 Write Ops    Read Ops      Metrics
    │              │              │
    ▼              ▼              ▼
┌────────┐  ┌───────────┐  ┌──────────┐
│Version │  │ Query     │  │Prometheus│
│Manager │  │ Engine    │  │ Metrics  │
└────┬───┘  └─────┬─────┘  └──────────┘
     │            │
     └────┬───────┘
          ▼
    ┌──────────────────────────┐
    │  Integrity Gate          │
    │  (Activation Blocker)    │
    └────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│   PostgreSQL Database (Truth)    │
│                                  │
│  ├─ concepts                     │
│  ├─ relations                    │
│  ├─ attributes                   │
│  ├─ constraints                  │
│  ├─ versions                     │
│  ├─ audit_log                    │
│  └─ [in-memory schema_registry]  │
└──────────────────────────────────┘
```

## Request Flows

### CREATE CONCEPT Flow
```
Client
  │
  ├─ POST /schema/{name}/class
  │
  ▼
┌──────────────────────┐
│ Validate Input       │
│ - name not empty     │
│ - class_type valid   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ get_db_context() creates Session     │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ repository.create_concept(session)   │
│ - session.add(concept)               │
│ - _log_audit(session, ...)           │
│ - session.flush() [NOT commit]       │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ [Auto-commit on context exit]        │
│ [Auto-rollback on exception]         │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ publish_entity_created(...)          │
│ - Event published to subscribers     │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ Update schema_registry cache         │
│ metrics.update_ontology_stats()      │
└──────────┬───────────────────────────┘
           │
           ▼
Return 200 + ConceptModel
```

### ACTIVATE VERSION Flow
```
Client
  │
  ├─ POST /versions/{id}/activate
  │
  ▼
┌──────────────────────────────────────┐
│ get_db_context() creates Session     │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ ActivationGate.verify_before_...()   │
│                                      │
│ 1. _check_structural_integrity()     │
│    - refs valid?                     │
│    - cycles exist?                   │
│                                      │
│ 2. _check_semantic_integrity()       │
│    - contradictions?                 │
│    - cardinality ok?                 │
│                                      │
│ 3. _check_completeness()             │
│    - required fields present?        │
│                                      │
│ 4. _check_constraint_executability() │
│    - expressions valid?              │
│                                      │
│ IF ANY FAIL: raise IntegrityError ❌ │
└──────────┬───────────────────────────┘
           │ ✅ All pass
           ▼
┌──────────────────────────────────────┐
│ set_active_version(version_id)       │
│ - Deactivate all current versions    │
│ - Activate target version            │
│ - session.flush()                    │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ [Auto-commit on context exit]        │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ publish_version_activated(...)       │
│ - Event published to subscribers     │
│ - Event: version = new_version       │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ schema_registry cache invalidated    │
│ Other services subscribe to event    │
│ and update their caches              │
└──────────┬───────────────────────────┘
           │
           ▼
Return 200 + VersionModel
```

### VERIFY INSTANCE Flow
```
Client
  │
  ├─ POST /schema/{name}/verify/instance
  │   Body: {"_class": "Candle", "open": 100.0, ...}
  │
  ▼
┌──────────────────────────────────────┐
│ Validate request                     │
│ - _class field present?              │
│ - Class exists in schema?            │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ OntologyValidator.validate_instance()│
│                                      │
│ - Class membership check             │
│ - Property type validation           │
│ - Cardinality validation             │
│ - Constraint satisfaction            │
│ - Inheritance validation             │
│                                      │
│ Returns: ValidationResult            │
│   - is_valid: bool                   │
│   - errors: [...]                    │
│   - warnings: [...]                  │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ if is_valid:                         │
│   Return 200 + result                │
│ else:                                │
│   Return 400 + errors                │
└──────────────────────────────────────┘
```

## Database Schema (PostgreSQL)

```sql
-- Concepts (entity types)
concepts (
  id UUID PRIMARY KEY,
  name VARCHAR(255) UNIQUE NOT NULL,
  description TEXT,
  category VARCHAR(50),          -- entity, relation, attribute, state
  immutable BOOLEAN DEFAULT FALSE,
  version VARCHAR(20),
  created_at DATETIME DEFAULT now(),
  updated_at DATETIME DEFAULT now()
)

-- Relations (edges between concepts)
relations (
  id UUID PRIMARY KEY,
  from_concept_id UUID FK -> concepts,
  to_concept_id UUID FK -> concepts,
  relation_type VARCHAR(100),    -- has, is_a, contains, emits
  cardinality VARCHAR(20),       -- 1:1, 1:N, N:N
  description TEXT,
  created_at DATETIME DEFAULT now(),
  updated_at DATETIME DEFAULT now(),
  UNIQUE(from_concept_id, to_concept_id, relation_type)
)

-- Attributes (properties of concepts)
attributes (
  id UUID PRIMARY KEY,
  concept_id UUID FK -> concepts,
  name VARCHAR(255),
  data_type VARCHAR(100),        -- string, int, float, bool, datetime, json
  required BOOLEAN DEFAULT FALSE,
  mutable BOOLEAN DEFAULT TRUE,
  description TEXT,
  default_value TEXT,
  created_at DATETIME DEFAULT now(),
  updated_at DATETIME DEFAULT now(),
  UNIQUE(concept_id, name)
)

-- Constraints (validation rules)
constraints (
  id UUID PRIMARY KEY,
  concept_id UUID FK -> concepts NULLABLE,
  name VARCHAR(255) UNIQUE,
  rule_type VARCHAR(100),        -- value, cardinality, relationship, temporal
  rule_expression TEXT NOT NULL, -- VALIDATED before insert
  severity VARCHAR(20),          -- hard, soft
  applies_to TEXT,               -- JSON list of concept IDs
  description TEXT,
  created_at DATETIME DEFAULT now(),
  updated_at DATETIME DEFAULT now()
)

-- Versions (schema versioning)
versions (
  id UUID PRIMARY KEY,
  ontology_version VARCHAR(20) UNIQUE,  -- semver 1.0.0
  parent_version VARCHAR(20) NULLABLE,  -- lineage
  active BOOLEAN DEFAULT FALSE,         -- only one
  snapshot TEXT,                        -- JSON snapshot
  author VARCHAR(255),
  description TEXT,
  created_at DATETIME DEFAULT now(),
  updated_at DATETIME DEFAULT now()
)

-- Audit Log (compliance & debugging)
audit_log (
  id UUID PRIMARY KEY,
  entity_type VARCHAR(50),       -- concept, relation, attribute, constraint, version
  entity_id UUID,
  entity_name VARCHAR(255),
  action VARCHAR(20),            -- create, update, delete, activate
  author VARCHAR(255),
  timestamp DATETIME DEFAULT now(),
  old_value TEXT,                -- JSON
  new_value TEXT,                -- JSON
  change_reason TEXT,
  immutability_blocked BOOLEAN DEFAULT FALSE,
  
  INDEX(entity_type, entity_id, timestamp),
  INDEX(entity_type, action, timestamp),
  INDEX(author, timestamp)
)
```

## Session Lifecycle (CRITICAL)

```
┌─────────────────────────────────────────────────────────┐
│ Service Method (e.g., create_concept_with_validation)  │
└────┬────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────┐
│ with get_db_context() as session:  # Enter transaction  │
│     # session is SessionLocal() instance                │
│     # autocommit=False, autoflush=False                 │
└────┬────────────────────────────────────────────────────┘
     │
     ├─ repo.create_concept(..., session=session)
     │      ├─ session.add(concept)
     │      ├─ session.flush()     [writes to buffer]
     │      └─ _log_audit(session=session, ...)
     │
     ├─ repo.create_constraint(..., session=session)
     │      ├─ session.add(constraint)
     │      ├─ session.flush()
     │      └─ _log_audit(session=session, ...)
     │
     └─ # Exit context
        │
        ├─ If all success: session.commit() ✅
        │   (atomic: all changes or nothing)
        │
        └─ If any exception: session.rollback() ❌
           (automatic: all changes reverted)
           (exception re-raised to caller)
```

## Immutability Enforcement

```
ConceptModel.immutable = True
  │
  ├─ Created manually (design time)
  ├─ Example: "Trade", "Market", "Candle" (core concepts)
  │
  ▼
┌──────────────────────────────────────┐
│ Immutability Checks (at service time)│
└──────────────────────────────────────┘
  │
  ├─ update_concept(concept_id):
  │    IF concept.immutable:
  │      ├─ _log_audit(..., immutability_blocked=True)
  │      └─ raise ValueError (BLOCKS UPDATE)
  │
  └─ delete_concept(concept_id):
       IF concept.immutable:
         ├─ _log_audit(..., immutability_blocked=True)
         └─ raise ValueError (BLOCKS DELETE)
```

## Event Publishing Flow

```
┌──────────────────────────────────────┐
│ User/Service Action                  │
│ (create concept, activate version)   │
└────┬─────────────────────────────────┘
     │
     ▼
┌──────────────────────────────────────┐
│ Service completes operation          │
│ (in DB transaction)                  │
└────┬─────────────────────────────────┘
     │
     ▼
┌──────────────────────────────────────┐
│ Transaction commits ✅               │
└────┬─────────────────────────────────┘
     │
     ▼
┌──────────────────────────────────────┐
│ publish_entity_created(              │
│   entity_type="concept",             │
│   entity_id=...,                     │
│   version="1.0.0"                    │
│ )                                    │
└────┬─────────────────────────────────┘
     │
     ▼
┌──────────────────────────────────────┐
│ EventPublisher.publish(event)        │
│                                      │
│ 1. Store in _event_history           │
│ 2. Notify subscribers:               │
│    for callback in subscribers:      │
│      callback(event)                 │
└────┬─────────────────────────────────┘
     │
     ▼
┌──────────────────────────────────────┐
│ Subscribers process event            │
│ - Update local cache                 │
│ - Publish to message bus             │
│ - Trigger downstream processing      │
└──────────────────────────────────────┘
```

---

This architecture ensures:
✅ ACID transactions via PostgreSQL
✅ Atomic versioning (one active at a time)
✅ Integrity gates (broken versions blocked)
✅ Audit trails (all changes logged)
✅ Event-driven updates (cache invalidation)
✅ Session isolation (no race conditions)
✅ Immutability enforcement (core concepts protected)
