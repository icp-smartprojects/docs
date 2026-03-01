# Shape Engine — Complete Architecture Blueprint

**Version:** 2.0.0  
**Classification:** Core Cognitive Service  
**Port:** 52010  
**Status:** Enterprise-Grade, Production-Ready  

---

## Executive Summary

The Shape Engine is the **structural interpreter** of AUREXIS. It transforms raw price action into semantic, first-class shape objects that exist in **time-price space**, not on pixels.

This is not a drawing tool. This is **geometry + time + rules**.

---

## What the Shape Engine Is

The Shape Engine is where **human intuition becomes machine-usable structure**.

### Core Questions the Shape Engine Answers

1. **Where** is this structure located in time–price space?
2. **What candles** anchor it?
3. **What type** of structure is this?
4. **Is it forming, valid, mitigated, broken, or invalid?**
5. **How does it relate** across multiple timeframes?
6. **Is this structure confirmed or provisional?**
7. **Does this structure contradict higher-timeframe structure?**

### What the Shape Engine Does NOT Do

- ❌ Predict outcomes
- ❌ Decide trades
- ❌ Enforce risk
- ❌ Simulate futures

It **describes and governs structure**. Decisions come later.

---

## Foundation: Time–Price Space

### Everything is a Mathematical Object

A shape is NOT a drawing. A shape is:

```
Shape = {
    id: UUID,
    type: ShapeType,
    timeframe: String,
    t_start: Timestamp,
    t_end: Timestamp,
    p_low: Float,
    p_high: Float,
    anchors: [CandleAnchor],
    cause_events: [Event],
    state: ShapeState,
    confidence: Float
}
```

### Coordinate System

- **Time**: Unix timestamp or candle index
- **Price**: Asset units (not pixels)
- **Anchors**: Specific candles (by ID/timestamp)
- **Projection**: Frontend pixels derive from coordinates, not vice versa

### Why This Matters

- **Deterministic**: Same candles = same shape
- **Replayable**: Can reconstruct historical state
- **Testable**: Can validate against price data
- **Cross-platform**: Same coordinates work everywhere

---

## Shape Lifecycle — The Canonical State Machine

### States (Strict Sequence)

```
DORMANT
  ↓
FORMING (NEW — added per blueprint)
  ↓
ACTIVE
  ↓
TESTED
  ↓
CONFIRMED
  ↓         ↘
MITIGATED → INVALIDATED
              ↓
           ARCHIVED
```

### State Definitions

| State | Meaning | Transitions Allowed |
|-------|---------|---------------------|
| **DORMANT** | Shape created but not anchored | → FORMING |
| **FORMING** | Being constructed, anchored but unconfirmed | → ACTIVE, INVALIDATED |
| **ACTIVE** | Anchored, waiting for interaction | → TESTED, INVALIDATED |
| **TESTED** | Price has interacted | → CONFIRMED, DEGRADED, INVALIDATED |
| **CONFIRMED** | Validity confirmed by price action | → MITIGATED, INVALIDATED |
| **MITIGATED** | Zone filled but may still react | → INVALIDATED, ARCHIVED |
| **INVALIDATED** | Broken/invalid | → ARCHIVED |
| **ARCHIVED** | Final state, historical storage | (terminal) |

### Why Lifecycle is Critical

- **Automation** depends on state: FORMING shapes can't justify decisions
- **Learning** depends on state: CONFIRMED shapes can influence bias
- **Meaning** depends on state: INVALIDATED shapes kill downstream meanings

---

## Anchoring System — Deterministic Foundation

### Candle Anchoring

Every shape is anchored to specific candles:

```python
CandleAnchor = {
    candle_id: "BTC_1M_1704067200",
    timestamp: DateTime,
    price: Float,
    anchor_type: HIGH | LOW | CLOSE | OPEN,
    candle_ohlc: {...},
    bar_index: Int
}
```

### Time-Price Geometry

```python
ShapeGeometry = {
    shape_id: UUID,
    anchors: [CandleAnchor],
    time_start: Float,
    time_end: Float,
    price_low: Float,
    price_high: Float,
    edges: [Edge]
}
```

### Replayability

```python
# Replay shape state at any historical time
state = await replay_shape_at_time(shape_id, timestamp)
# Returns shape as it existed at that moment
```

### Why Anchoring Matters

- **Backtesting**: Precise historical reconstruction
- **Validation**: Deterministic price interaction
- **Learning**: Repeatable outcome measurement
- **Cross-TF**: Coherent structure across timeframes

---

## Multi-Timeframe Hierarchy — HTF Dominance

### Authority Levels

```
1W  → Authority: 11 (HIGHEST)
1D  → Authority: 10
4H  → Authority: 9
1H  → Authority: 8
15M → Authority: 6
5M  → Authority: 5
1M  → Authority: 2 (LOWEST)
```

### Dominance Rules

1. **HTF always dominates LTF**
2. **HTF invalidation instantly kills dependent LTF shapes**
3. **LTF bullish FVG inside HTF bearish supply → suppressed**
4. **Cross-timeframe consensus weighted by authority**

### Suppression Logic

```python
if htf_shape.contradicts(ltf_shape) and htf_shape.authority > ltf_shape.authority:
    ltf_shape.update_state(SUPPRESSED, "HTF contradiction")
```

### Why Multi-TF Matters

- **Prevents false signals** from LTF noise
- **Ensures coherence** across timeframes
- **Automates context** — system "sees" 12 TFs interlocking

---

## Shape Creation — Two Paths

### Path A: Human-Drawn (Assisted Intelligence)

1. Human draws shape on frontend
2. Frontend converts pixels → time-price coordinates
3. Shape Engine receives: type, coordinates, timeframe, intent
4. **Ontology validation** (shape type valid?)
5. **Anchoring** to candles
6. Lifecycle = **FORMING**
7. Shape becomes first-class object

**Important**: Human does NOT define truth. They **propose structure**.

### Path B: Machine-Detected (Autonomous)

1. Perception emits semantic events (BOS, liquidity sweep, imbalance)
2. Shape Engine listens via Event Bus
3. Detection logic scans candle sequences
4. Candidate shapes created
5. **Confidence score** assigned
6. Lifecycle = **FORMING**
7. Shape waits for confirmation/invalidation

Shapes are:
- Tagged as `machine_generated`
- Explainable (reasoning chain)
- Auditable (event sourced)

---

## Automation — 4-Phase Learning System

This is how the system **"learns to draw itself"**.

### Phase 1: ASSISTED_LEARNING

**System watches humans.**

- Observes placement timing
- Tracks anchor selection
- Records market context
- Monitors confirmation outcomes
- **Does not act** — only learns

**Transition**: After 100+ observations → Phase 2

### Phase 2: GUIDED_AUTOMATION

**System proposes, human approves/rejects.**

- System generates shape proposals
- Includes explicit reasoning
- Human reviews and provides feedback
- Feedback drives confidence calibration
- **Acts only with approval**

**Transition**: After 50+ approvals with 70%+ approval rate → Phase 3

### Phase 3: AUTONOMOUS_DRAWING

**System creates shapes independently.**

- Executes autonomously if confidence ≥ learned threshold
- Escalates if:
  - Confidence below threshold
  - Conflicting with HTF
  - Novel pattern
- **Acts independently**, escalates uncertainty

**Transition**: After 100+ autonomous creations with 85%+ success → Phase 4

### Phase 4: SELF_CORRECTION

**System learns invalidation patterns and filters weak structures.**

- Recognizes common mistakes
- Stops drawing weak patterns
- Adjusts confidence thresholds dynamically
- Prioritizes high-quality confluence
- **Self-improves** based on outcomes

### Why 4 Phases Matter

This is **not blind ML**. This is:
- Outcome-based
- Rule-governed
- Explainable
- Auditable

Automation emerges from: **outcomes + correction + memory + ontology rules**

---

## Shape Interaction & Conflict Resolution

Shapes do not live alone.

### Interaction Types

1. **OVERLAP** — Shapes overlap in time-price space
2. **NESTING** — One shape contains another
3. **CONTRADICTION** — Shapes conflict semantically
4. **CONFLUENCE** — Shapes reinforce each other
5. **ADJACENCY** — Shapes touch but don't overlap
6. **SEPARATION** — Shapes are distinct

### Conflict Detection

```python
# Example: Bullish FVG vs Bearish FVG in same zone
if overlap_detected and opposite_directions:
    conflict_severity = calculate_severity(shape1, shape2)
    # CRITICAL if HTF vs LTF
    # HIGH if same TF
```

### Resolution Hierarchy

1. **HTF always dominates LTF** → Suppress LTF
2. **Higher confidence wins** on same TF → Archive lower
3. **Newer shape wins** if equal → Archive older
4. **Escalate to human** if cannot resolve

### Confluence Detection

When multiple compatible shapes overlap:

```python
ConfluenceZone = {
    zone_id: UUID,
    timeframe: String,
    time_range: (start, end),
    price_range: (low, high),
    contributing_shapes: [shape_id],
    confluence_strength: 0.0-1.0,
    semantic_interpretation: String
}
```

**Strength = min(1.0, shape_count / 5.0)**

---

## Enterprise Features — Audit & Replay

### Audit Trail (Event Sourcing)

Every shape action is recorded:

```python
AuditEvent = {
    event_id: UUID,
    timestamp: DateTime,
    event_type: SHAPE_CREATED | STATE_CHANGED | VALIDATED | ...,
    actor: HUMAN | SYSTEM | AUTOMATION,
    entity_id: shape_id,
    payload: {...},
    caused_by_event_id: UUID
}
```

**Append-only, immutable, permanent.**

### Replayability

```python
# Reconstruct shape state at any historical time
state = await replay_entity_state_at_time(shape_id, target_time)

# Replay complete timeline
timeline = await replay_timeline(start_time, end_time)
```

### Why Audit Matters

- **Regulatory compliance**
- **Learning validation**
- **Debugging** (time-travel debugging)
- **Trust** (every action traceable)

---

## Ontology Enforcement — The Gatekeeper

Every shape MUST conform to the ontology.

### Validation Checks

1. **Shape type exists** in ontology
2. **Required properties** present
3. **Property values** valid (type, range, enum)
4. **State transitions** allowed
5. **Relationships** valid

### Example Validation

```python
# FVG must have:
- direction: BULLISH | BEARISH
- gap_size: float > 0
- exactly 3 candles

# Invalid FVG rejected before creation
```

### Integration with Ontology Service

```python
# Fetch latest ontology
ontology = await fetch_ontology_from_service()

# Validate against remote authority
result = await validate_against_remote_ontology(shape_data)
```

### Why Ontology Enforcement Matters

Without it:
- **Chaos** — shapes with invalid properties
- **Incompatibility** — downstream services break
- **Untrust** — automation makes invalid decisions

---

## Service Dependencies

### Depends On

| Service | Purpose |
|---------|---------|
| **Ontology** | Validation rules, shape definitions |
| **Perception** | Semantic events (BOS, FVG, etc) |
| **Event Bus** | Real-time streaming |
| **Schema Registry** | Schema consistency |
| **Memory** | Persistence |
| **Price Observer** | Candle data |

### Supplies To

| Service | What It Provides |
|---------|-----------------|
| **Meaning Engine** | Structure context |
| **Simulation** | Structural constraints |
| **Learning Engine** | Outcome labels |
| **Policy Engine** | Structural risk |
| **Frontend** | Visualization |
| **Explanation Engine** | Evidence |

---

## API Endpoints

### Core Operations

```
POST   /api/v1/shapes              — Create shape
GET    /api/v1/shapes/{id}         — Get shape
PUT    /api/v1/shapes/{id}         — Update shape
DELETE /api/v1/shapes/{id}         — Delete shape
POST   /api/v1/shapes/{id}/anchor  — Anchor to candles
```

### Detection & Validation

```
POST   /api/v1/detect              — Detect shapes autonomously
POST   /api/v1/validate/{id}       — Validate shape
GET    /api/v1/confidence/{id}     — Get confidence score
```

### Automation

```
POST   /api/v1/automation/propose  — Propose shape (Phase 2)
POST   /api/v1/automation/review   — Review proposal
GET    /api/v1/automation/status   — Get automation phase status
```

### Multi-TF & Interaction

```
GET    /api/v1/multi-tf/consensus  — Get cross-TF consensus
POST   /api/v1/interactions        — Analyze shape interactions
GET    /api/v1/confluence          — Get confluence zones
```

### Audit & Replay

```
GET    /api/v1/audit/{entity_id}   — Get audit trail
POST   /api/v1/replay              — Replay historical state
GET    /api/v1/replay/timeline     — Replay timeline
```

### Real-Time

```
WS     /ws/shapes                  — Shape events stream
```

---

## Implementation Modules

### Core Modules

```
src/core/
  ├── anchoring.py                 — Deterministic candle anchoring
  ├── audit.py                     — Audit trail & replay engine
  ├── conflict_resolution.py       — Interaction & conflict logic
  ├── ontology_validator.py        — Ontology enforcement
  ├── shapes/                      — Shape implementations
  ├── lifecycle/                   — State machine
  ├── detection/                   — Autonomous detection
  ├── multi_timeframe/             — HTF/LTF coordination
  └── learning/
      ├── automation_orchestrator.py  — 4-phase automation
      ├── confidence_calibration.py   — Confidence tuning
      └── pattern_evolution.py        — Pattern learning
```

---

## Enterprise-Grade Checklist

✅ **Deterministic anchoring** — Candle-based, replayable  
✅ **Strict lifecycle state machine** — DORMANT → FORMING → ACTIVE → TESTED → CONFIRMED → MITIGATED → INVALIDATED → ARCHIVED  
✅ **Multi-timeframe dominance rules** — HTF > LTF  
✅ **Explainability** — Every shape has reasoning chain  
✅ **Audit logs** — Event sourcing, append-only  
✅ **Replayability** — Time-travel to any historical state  
✅ **Ontology enforcement** — Validation before creation  
✅ **Human + machine coexistence** — Two creation paths  
✅ **Confidence calibration** — Dynamic threshold adjustment  
✅ **Conflict resolution** — Automated, rule-based  
✅ **4-phase automation** — Assisted → Guided → Autonomous → Self-Correcting  

---

## Critical Truths

### 1. Shapes Are Not Art

They are **geometry + time + rules**. Not subjective drawings.

### 2. Frontend is Not Smart

It is a **viewer and editor**. Authority lives in Shape Engine.

### 3. HTF Dominates LTF

Always. No exceptions.

### 4. Automation Emerges from Outcomes

Not from blind ML. From **correction + memory + rules**.

### 5. Every Action is Auditable

Event sourcing is non-negotiable.

### 6. Ontology is the Contract

Without enforcement, the system collapses into noise.

---

## When Shape Engine is Done Right

✅ **Simulation becomes accurate** — Structural constraints are real  
✅ **Meaning becomes stable** — Structure context is deterministic  
✅ **Learning becomes real** — Outcomes are measurable  
✅ **Automation becomes safe** — Actions are explainable  

---

## When Shape Engine is Done Wrong

❌ **Simulation lies** — Fake constraints  
❌ **Meaning collapses** — Noise instead of structure  
❌ **Learning fails** — Unmeasurable outcomes  
❌ **Automation breaks** — Unexplainable chaos  

---

## Next Steps

1. **Map Shape Engine ↔ Meaning Engine** in detail
2. **Define shape tests** that certify readiness
3. **Design autonomous shape learning gates**
4. **Walk through full example**: candle → shape → meaning

---

## Conclusion

The Shape Engine is where **human intuition becomes machine-usable structure**.

It is the bridge between:
- Raw price data
- Human intent
- Machine structure
- Automation

When done right, it is the **geometry engine of intelligence**.

When done wrong, everything above collapses into noise.

**This is not optional. This is the foundation.**

---

**End of Architecture Blueprint**
