# Shape Engine — Complete System Map

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          SHAPE ENGINE (52010)                                │
│                    Structural Intelligence Service                           │
└─────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  1. TIME-PRICE SPACE FOUNDATION                                             │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Shape = Mathematical Object in Time-Price Space                            │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────┐          │
│  │  TimePriceCoordinate                                          │          │
│  │  ├── time: Float (timestamp or index)                         │          │
│  │  ├── price: Float (asset units, not pixels)                  │          │
│  │  ├── timeframe: String                                        │          │
│  │  └── candle_id: String (deterministic reference)             │          │
│  └──────────────────────────────────────────────────────────────┘          │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────┐          │
│  │  CandleAnchor                                                 │          │
│  │  ├── candle_id: "BTC_1M_1704067200"                          │          │
│  │  ├── timestamp: DateTime                                      │          │
│  │  ├── price: Float                                             │          │
│  │  ├── anchor_type: HIGH | LOW | CLOSE | OPEN                  │          │
│  │  └── candle_ohlc: {open, high, low, close}                   │          │
│  └──────────────────────────────────────────────────────────────┘          │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────┐          │
│  │  ShapeGeometry                                                │          │
│  │  ├── anchors: [CandleAnchor]                                 │          │
│  │  ├── time_start, time_end                                    │          │
│  │  ├── price_low, price_high                                   │          │
│  │  └── edges: [Edge]                                            │          │
│  └──────────────────────────────────────────────────────────────┘          │
│                                                                              │
│  RESULT: Deterministic, Replayable, Testable                               │
└────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  2. CANONICAL LIFECYCLE STATE MACHINE                                       │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│      DORMANT                                                                │
│         │  (Shape created, not anchored)                                    │
│         ▼                                                                    │
│      FORMING  ◄── NEW: Blueprint-compliant                                 │
│         │  (Being constructed, anchored but unconfirmed)                    │
│         ▼                                                                    │
│      ACTIVE                                                                 │
│         │  (Anchored, waiting for price interaction)                        │
│         ▼                                                                    │
│      TESTED                                                                 │
│         │  (Price has interacted with shape)                                │
│         ▼                                                                    │
│     CONFIRMED                                                               │
│         │  (Validity confirmed by price action)                             │
│         ▼                                                                    │
│     MITIGATED                                                               │
│         │  (Zone filled, may still react)                                   │
│         ▼                                                                    │
│    INVALIDATED                                                              │
│         │  (Broken/invalid)                                                 │
│         ▼                                                                    │
│     ARCHIVED                                                                │
│         ●  (Terminal state, historical storage)                             │
│                                                                              │
│  ENFORCEMENT: Strict transitions, no skipping states                        │
└────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  3. SHAPE CREATION — TWO PATHS                                              │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  PATH A: HUMAN-DRAWN (Assisted Intelligence)                                │
│  ┌──────────────────────────────────────────────────────────┐              │
│  │  1. Human draws on frontend                               │              │
│  │  2. Pixels → Time-Price Coordinates                       │              │
│  │  3. Ontology Validation                                   │              │
│  │  4. Anchor to Candles                                     │              │
│  │  5. State = FORMING                                       │              │
│  │  6. Shape created ✓                                       │              │
│  └──────────────────────────────────────────────────────────┘              │
│                                                                              │
│  PATH B: MACHINE-DETECTED (Autonomous)                                      │
│  ┌──────────────────────────────────────────────────────────┐              │
│  │  1. Perception emits semantic event (BOS, FVG, etc)      │              │
│  │  2. Detection logic scans candles                         │              │
│  │  3. Candidate shape created                               │              │
│  │  4. Confidence score assigned                             │              │
│  │  5. Ontology validation                                   │              │
│  │  6. State = FORMING                                       │              │
│  │  7. Shape created (with reasoning) ✓                      │              │
│  └──────────────────────────────────────────────────────────┘              │
│                                                                              │
│  BOTH: Explainable, Auditable, Anchored                                    │
└────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  4. AUTOMATION ORCHESTRATOR — 4 PHASES                                      │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓              │
│  ┃ PHASE 1: ASSISTED_LEARNING                              ┃              │
│  ┃ ─────────────────────────                               ┃              │
│  ┃ • System WATCHES humans                                 ┃              │
│  ┃ • Records placement, timing, context                    ┃              │
│  ┃ • Builds pattern library                                ┃              │
│  ┃ • DOES NOT ACT — only learns                            ┃              │
│  ┃                                                          ┃              │
│  ┃ Transition: 100+ observations → Phase 2                 ┃              │
│  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛              │
│                          ▼                                                  │
│  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓              │
│  ┃ PHASE 2: GUIDED_AUTOMATION                               ┃              │
│  ┃ ──────────────────────                                   ┃              │
│  ┃ • System PROPOSES shapes (with reasoning)               ┃              │
│  ┃ • Human APPROVES/REJECTS                                ┃              │
│  ┃ • Feedback calibrates confidence                        ┃              │
│  ┃ • Acts only with approval                               ┃              │
│  ┃                                                          ┃              │
│  ┃ Transition: 50+ approvals, 70%+ rate → Phase 3          ┃              │
│  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛              │
│                          ▼                                                  │
│  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓              │
│  ┃ PHASE 3: AUTONOMOUS_DRAWING                              ┃              │
│  ┃ ───────────────────────                                  ┃              │
│  ┃ • System ACTS INDEPENDENTLY                              ┃              │
│  ┃ • Auto-approves if confidence ≥ threshold               ┃              │
│  ┃ • Escalates if: low confidence, HTF conflict, novel     ┃              │
│  ┃ • Humans intervene rarely                               ┃              │
│  ┃                                                          ┃              │
│  ┃ Transition: 100+ creations, 85%+ success → Phase 4      ┃              │
│  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛              │
│                          ▼                                                  │
│  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓              │
│  ┃ PHASE 4: SELF_CORRECTION                                 ┃              │
│  ┃ ────────────────────                                     ┃              │
│  ┃ • System LEARNS MISTAKES                                 ┃              │
│  ┃ • Filters weak patterns automatically                    ┃              │
│  ┃ • Adjusts thresholds dynamically                         ┃              │
│  ┃ • Prioritizes high-quality confluence                    ┃              │
│  ┃ • Self-improving                                         ┃              │
│  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛              │
│                                                                              │
│  RESULT: Outcome-based, Rule-governed, Explainable                         │
└────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  5. MULTI-TIMEFRAME HIERARCHY                                               │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   Authority Levels                    HTF Dominance Rules                   │
│   ───────────────                     ─────────────────────                 │
│                                                                              │
│   1W  ─┐ Authority: 11 (HIGHEST)      1. HTF ALWAYS dominates LTF          │
│   1D  ─┤ Authority: 10                2. HTF invalidation → LTF suppression │
│   4H  ─┤ Authority: 9                 3. LTF bullish + HTF bearish          │
│   1H  ─┤ Authority: 8                    → LTF SUPPRESSED                   │
│   15M ─┤ Authority: 6                 4. Cross-TF consensus weighted by     │
│   5M  ─┤ Authority: 5                    authority                          │
│   1M  ─┘ Authority: 2 (LOWEST)                                              │
│                                                                              │
│  ┌────────────────────────────────────────────────────────┐                │
│  │  Example: HTF Suppression                              │                │
│  │                                                         │                │
│  │  4H Bearish Supply Zone (CONFIRMED)                    │                │
│  │       │                                                 │                │
│  │       ├─ Contradicts ──> 15M Bullish FVG              │                │
│  │       │                        │                        │                │
│  │       │                        ▼                        │                │
│  │       │                  State = SUPPRESSED            │                │
│  │       │                  Reason = "HTF contradiction"  │                │
│  │       │                                                 │                │
│  │       └─ Result: 15M signal IGNORED in decisions      │                │
│  └────────────────────────────────────────────────────────┘                │
│                                                                              │
│  ENFORCEMENT: HTF > LTF always, no exceptions                              │
└────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  6. SHAPE INTERACTION & CONFLICT RESOLUTION                                 │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Interaction Types                    Resolution Hierarchy                  │
│  ─────────────────                    ──────────────────────                │
│                                                                              │
│  • OVERLAP    — Shapes overlap        1. HTF dominates LTF → Suppress LTF  │
│  • NESTING    — One contains other    2. Higher confidence → Archive lower │
│  • CONTRADICTION — Semantic conflict  3. Newer shape → Archive older       │
│  • CONFLUENCE — Reinforce each other  4. Cannot resolve → Escalate human   │
│  • ADJACENCY  — Touch but separate                                          │
│  • SEPARATION — Distinct              Conflict Severity:                    │
│                                        ──────────────────                    │
│  ┌───────────────────────────────┐    • CRITICAL: HTF vs LTF (3+ TF diff) │
│  │  Confluence Zone Detection    │    • HIGH: Same TF opposite signals     │
│  │                                │    • MEDIUM: Adjacent TF conflicts      │
│  │  When 2+ compatible shapes     │    • LOW: Minor geometric overlap       │
│  │  overlap in time-price:        │                                         │
│  │                                │                                          │
│  │  ┌─────────────────────────┐  │                                          │
│  │  │ ConfluenceZone          │  │                                          │
│  │  │ ├── zone_id             │  │                                          │
│  │  │ ├── timeframe           │  │                                          │
│  │  │ ├── time_range          │  │                                          │
│  │  │ ├── price_range         │  │                                          │
│  │  │ ├── contributing_shapes │  │                                          │
│  │  │ ├── strength: 0.0-1.0   │  │                                          │
│  │  │ └── interpretation      │  │                                          │
│  │  └─────────────────────────┘  │                                          │
│  │                                │                                          │
│  │  Strength = min(1.0, count/5) │                                          │
│  └───────────────────────────────┘                                          │
│                                                                              │
│  RESULT: Automated conflict resolution, confluence tracking                 │
└────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  7. ENTERPRISE AUDIT TRAIL & REPLAYABILITY                                  │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Event Sourcing (Append-Only, Immutable)                                   │
│  ────────────────────────────────────────                                   │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────┐              │
│  │  AuditEvent                                               │              │
│  │  ├── event_id: UUID                                       │              │
│  │  ├── timestamp: DateTime                                  │              │
│  │  ├── event_type: CREATED | STATE_CHANGED | VALIDATED...  │              │
│  │  ├── actor: HUMAN | SYSTEM | AUTOMATION                   │              │
│  │  ├── entity_id: shape_id                                  │              │
│  │  ├── payload: {...}                                       │              │
│  │  ├── caused_by_event_id: UUID (causal chain)             │              │
│  │  └── correlation_id: UUID (related events)               │              │
│  └──────────────────────────────────────────────────────────┘              │
│                                                                              │
│  Event Types:                                                               │
│  • Lifecycle: CREATED, ANCHORED, STATE_CHANGED, UPDATED, DELETED           │
│  • Interactions: TOUCHED, VALIDATED, INVALIDATED                            │
│  • Automation: PROPOSAL_CREATED, REVIEWED, AUTO_CREATED                     │
│  • Learning: FEEDBACK_RECEIVED, PATTERN_LEARNED                             │
│  • Multi-TF: HTF_SUPPRESSION, CONFLUENCE_DETECTED                          │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────┐              │
│  │  Replayability Engine                                     │              │
│  │                                                           │              │
│  │  # Replay entity at historical time                      │              │
│  │  state = replay_entity_state_at_time(id, timestamp)     │              │
│  │  # Result: Shape state as it existed then               │              │
│  │                                                           │              │
│  │  # Replay complete timeline                              │              │
│  │  timeline = replay_timeline(start, end, entity_ids)     │              │
│  │  # Result: All state transitions in chronological order │              │
│  │                                                           │              │
│  │  # Validate event sequence integrity                     │              │
│  │  validation = validate_event_sequence(entity_id)        │              │
│  │  # Result: Check causal chain, state transitions        │              │
│  └──────────────────────────────────────────────────────────┘              │
│                                                                              │
│  USE CASES: Compliance, debugging, learning validation, trust               │
└────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  8. ONTOLOGY ENFORCEMENT — THE GATEKEEPER                                   │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Validation Before Creation (BLOCKING)                                      │
│  ─────────────────────────────────────                                      │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────┐              │
│  │  OntologyValidator.validate_shape_creation()             │              │
│  │                                                           │              │
│  │  1. ✓ Shape type exists in ontology?                     │              │
│  │  2. ✓ Required properties present?                       │              │
│  │  3. ✓ Property values valid? (type, range, enum)        │              │
│  │  4. ✓ Shape-specific rules?                              │              │
│  │       • FVG: 3 candles, direction, gap_size             │              │
│  │       • CHOCH: from ≠ to direction                       │              │
│  │       • TREND_LINE: 2+ anchors, not same price          │              │
│  │  5. ✓ Anchor count sufficient?                           │              │
│  │  6. ✓ Timeframe valid?                                   │              │
│  │                                                           │              │
│  │  Result: ValidationResult {                              │              │
│  │    valid: bool,                                          │              │
│  │    violations: [...],                                    │              │
│  │    warnings: [...]                                       │              │
│  │  }                                                        │              │
│  └──────────────────────────────────────────────────────────┘              │
│                                                                              │
│  State Transition Validation                                                │
│  ──────────────────────────                                                 │
│                                                                              │
│  • Checks if transition allowed by state machine                           │
│  • Requires reason for critical transitions                                │
│  • Prevents invalid state jumps                                            │
│                                                                              │
│  Integration with Ontology Service (52007)                                 │
│  ──────────────────────────────────────────                                 │
│                                                                              │
│  • Fetches latest shape definitions                                        │
│  • Stays in sync with canonical ontology                                   │
│  • Validates against authoritative source                                  │
│                                                                              │
│  PREVENTS: Invalid shapes, chaos, downstream breakage                      │
└────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  9. SERVICE INTEGRATION MAP                                                 │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│         DEPENDS ON                   SUPPLIES TO                            │
│         ───────────                  ──────────                             │
│                                                                              │
│    Ontology (52007) ──┐                                                     │
│      • Validation     │         ┌──> Meaning Engine (52003)                │
│      • Definitions    │         │      • Structure context                 │
│                       │         │                                           │
│    Perception (52002)─┤         ├──> Simulation                            │
│      • Semantic       │         │      • Structural constraints             │
│        events         │  SHAPE  │                                           │
│                       ├─ ENGINE ├──> Learning Engine (52004)               │
│    Event Bus ─────────┤  52010  │      • Outcome labels                    │
│      • Streaming      │         │                                           │
│                       │         ├──> Policy Engine                          │
│    Memory ────────────┤         │      • Structural risk                    │
│      • Persistence    │         │                                           │
│                       │         ├──> Frontend                               │
│    Price Observer ────┘         │      • Visualization                      │
│      • Candle data              │                                           │
│                                 └──> Explanation Engine                     │
│                                        • Evidence chain                     │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  10. IMPLEMENTATION SUMMARY                                                 │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  NEW MODULES CREATED                                                        │
│  ───────────────────                                                         │
│                                                                              │
│  ✅ src/core/learning/automation_orchestrator.py (600+ lines)              │
│     • 4-phase automation: Assisted → Guided → Autonomous → Self-Correction │
│     • Proposal management, feedback processing, pattern learning           │
│                                                                              │
│  ✅ src/core/anchoring.py (450+ lines)                                     │
│     • Deterministic candle anchoring                                        │
│     • Time-price coordinate system                                          │
│     • Historical replay capability                                          │
│                                                                              │
│  ✅ src/core/conflict_resolution.py (650+ lines)                           │
│     • Overlap, nesting, contradiction detection                             │
│     • Confluence zone tracking                                              │
│     • Automated conflict resolution                                         │
│                                                                              │
│  ✅ src/core/audit.py (550+ lines)                                         │
│     • Event sourcing audit trail                                            │
│     • Replay engine                                                          │
│     • Event queries and statistics                                          │
│                                                                              │
│  ✅ src/core/ontology_validator.py (500+ lines)                            │
│     • Shape creation validation                                             │
│     • State transition enforcement                                          │
│     • Ontology service integration                                          │
│                                                                              │
│  ✅ ARCHITECTURE.md (500+ lines)                                           │
│     • Complete blueprint documentation                                      │
│                                                                              │
│  MODULES UPDATED                                                            │
│  ───────────────                                                             │
│                                                                              │
│  ✅ src/constants.py                                                        │
│     • Added FORMING state with documentation                                │
│                                                                              │
│  ✅ src/core/lifecycle/state_machine.py                                    │
│     • Updated state transitions to include FORMING                          │
│                                                                              │
│  TOTAL: 8 files, ~3,200 lines of enterprise-grade code + docs              │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  11. ENTERPRISE-GRADE CHECKLIST                                             │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ✅ Deterministic anchoring (candle-based, replayable)                     │
│  ✅ Strict lifecycle state machine (blueprint-compliant)                   │
│  ✅ Multi-timeframe dominance rules (HTF > LTF enforced)                   │
│  ✅ Explainability (every shape/proposal has reasoning)                    │
│  ✅ Audit logs (event sourcing, append-only, immutable)                    │
│  ✅ Replayability (time-travel to any historical state)                    │
│  ✅ Ontology enforcement (validation before creation)                      │
│  ✅ Human + machine coexistence (two creation paths)                       │
│  ✅ Confidence calibration (dynamic threshold adjustment)                   │
│  ✅ Conflict resolution (automated, rule-based)                             │
│  ✅ 4-phase automation (complete learning progression)                     │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  CRITICAL TRUTHS                                                            │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. Shapes are MATHEMATICAL OBJECTS, not art                                │
│  2. Frontend is NOT smart — authority lives in Shape Engine                │
│  3. HTF dominates LTF — ALWAYS, no exceptions                              │
│  4. Automation emerges from OUTCOMES, not blind ML                         │
│  5. Every action is AUDITABLE — event sourcing non-negotiable             │
│  6. Ontology is the CONTRACT — enforcement prevents chaos                  │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  RESULT                                                                     │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  The Shape Engine is now the GEOMETRY ENGINE OF INTELLIGENCE.               │
│                                                                              │
│  When the rest of AUREXIS asks "WHERE IS STRUCTURE?",                      │
│  the Shape Engine answers with PRECISION, DETERMINISM, and TRUTH.           │
│                                                                              │
│  ✅ Simulation becomes ACCURATE (deterministic constraints)                │
│  ✅ Meaning becomes STABLE (anchored structure)                            │
│  ✅ Learning becomes REAL (measurable outcomes)                            │
│  ✅ Automation becomes SAFE (explainable actions)                          │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────┘
```
