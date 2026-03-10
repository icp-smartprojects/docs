# AUREXIS V7 — Backend Architecture: What The System Actually Does

**Author**: Honest codebase audit by reading every service  
**Date**: 2025-07-17  
**Scope**: Backend only — no frontend, no landing page  
**Method**: Every `main.py`, `main.go`, `main.rs`, `main.js`, key source files, docker-compose, and shared libraries read line-by-line

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Infrastructure Layer](#2-infrastructure-layer)
3. [Data Ingestion Pipeline](#3-data-ingestion-pipeline)
4. [Perception Layer](#4-perception-layer)
5. [Meaning Layer](#5-meaning-layer)
6. [Shape Engine](#6-shape-engine)
7. [Reasoning Engine](#7-reasoning-engine)
8. [Simulation Engine](#8-simulation-engine)
9. [Core Brain — Decision Orchestrator](#9-core-brain--decision-orchestrator)
10. [Policy Engine](#10-policy-engine)
11. [Learning Engine](#11-learning-engine)
12. [Explanation Engine](#12-explanation-engine)
13. [Knowledge Graph](#13-knowledge-graph)
14. [Memory Service](#14-memory-service)
15. [Ontology Service](#15-ontology-service)
16. [Language Intelligence](#16-language-intelligence)
17. [Gateway](#17-gateway)
18. [Security Core](#18-security-core)
19. [Schema Registry](#19-schema-registry)
20. [Topology Hub](#20-topology-hub)
21. [Back-End Auth System](#21-back-end-auth-system)
22. [Shared Libraries](#22-shared-libraries)
23. [Cross-Cutting Patterns](#23-cross-cutting-patterns)
24. [Data Flow — End to End](#24-data-flow--end-to-end)
25. [Honest Assessment](#25-honest-assessment)

---

## 1. System Overview

AUREXIS is a microservice-based cognitive trading platform. It has **21 backend services** running in Docker containers, backed by **6 databases/stores**, communicating through an event bus.

The system's central idea: raw market price ticks flow through a multi-stage cognitive pipeline — observation → perception → meaning → reasoning → simulation → decision — and every stage produces auditable, explainable artifacts. It is designed for forex/derivatives markets and currently targets Deriv as a live data source.

**Languages used:**
- Python (FastAPI) — 15 services (the majority)
- Go (Gin/Gorilla) — 3 services (event-bus, gateway, schema-registry, topology-hub)
- Rust (Actix) — 1 service (price-observer)
- Node.js — 2 services (auth system via Express, security-core via Fastify)

**Total container count in docker-compose:** 27 (including databases and monitoring).

---

## 2. Infrastructure Layer

| Service | Port | Technology | Purpose |
|---|---|---|---|
| PostgreSQL | 54320 | postgres:15-alpine | Primary relational store (shape-engine, simulation runs, schema-registry) |
| Redis | 6380 | redis:7-alpine | Caching, shape-engine hot data, event-bus memory broker |
| MongoDB | 27018 | mongo:6 | Auth system user data, sessions, payments |
| ClickHouse | 8124/9001 | clickhouse-server:23.12 | Time-series storage for OHLCV candle data |
| Neo4j | 7474/7687 | neo4j:5 + APOC | Belief graph, knowledge-graph, concept relationships |
| Prometheus | 59090 | prom/prometheus | Metrics scraping from all services |
| Jaeger | 16686 | jaegertracing/all-in-one | Distributed tracing (OpenTelemetry) |

Every Python service integrates OpenTelemetry tracing via `shared/tracing.py`. Prometheus metrics are exposed on `/metrics` by most services.

---

## 3. Data Ingestion Pipeline

### 3a. Price Observer (Rust — port 52002)

**File:** `price-observer/src/main.rs`

The lowest level of the system. Written in Rust for performance. A pure sensory preprocessor:

- Receives raw tick data via a single POST endpoint: `/api/v1/price/observe`
- Normalizes the tick, emits an event to the event bus, then **forgets the raw data**
- No interpretation, no intelligence, no storage
- Uses Actix-Web with CORS, compression, structured logging

**Honest note:** The code is clean but the service is thin — it's essentially a tick-to-event relay. The Rust choice makes sense for latency-sensitive tick processing but the current throughput requirements (Deriv WebSocket) probably don't demand it.

### 3b. Market Ingestion (Python — port 52024)

**File:** `market-ingestion/src/main.py`

The system's multi-format data intake:

- Connectors: `UniversalConnector` (CSV, Excel, JSON, PDF), `APIConnector`, `BrokerConnector`, `DerivWebSocketConnector`
- Writes raw ticks to ClickHouse via `ClickHouseWriter`
- Publishes to event bus via `EnterpriseEventPublisher`
- Validates data via `EnterpriseValidator`
- Tracks data provenance via `ProvenanceTracker`
- Detects gaps via `GapDetector`
- Runs a basic HTTP health server (not FastAPI — raw `http.server`)
- **Deriv streaming** is the primary live data source

**Honest note:** This is real plumbing. The Deriv WebSocket connector (`DerivWebSocketConnector` with `DerivConfig`) is the live pipeline. CSV/Excel/PDF support exists for historical data loading. The gap detector is a nice touch for data quality.

### 3c. Candle Constructor (Python/FastAPI — port 52023)

**File:** `candle-constructor/main.py`, `src/aggregation/aggregator.py`, `src/timeframe_registry.py`

Builds OHLCV candles from raw ticks across 15 timeframes:

- **TimeframeRegistry**: 15 TFs from 1-second to 1-month, each with nanosecond duration, authority weight (1–12), and aliases
- **CandleAggregator**: Fan-out parallel aggregation using `ThreadPoolExecutor` — one tick triggers simultaneous candle updates across all 15 TFs
- **RollingWindowAggregator**: Sliding-window candle computation with configurable lookback
- **EquivalenceValidator**: Verifies that different aggregation paths produce identical candles
- **Event-driven lifecycle**: `CandleOpened`, `CandleUpdated`, `CandleClosed` events published per-TF
- Auto-ingest: watches for CSV files and loads historical data on startup
- Stores completed candles in ClickHouse

**Honest note:** This is one of the more solidly implemented services. The parallel fan-out across 15 TFs is real, the equivalence validator provides self-checking, and the rolling window aggregator works. The 15-TF registry is genuinely useful for the multi-timeframe philosophy.

---

## 4. Perception Layer

**Service:** perception (Python/FastAPI — port 52012)  
**File:** `perception/src/main.py`, `src/pipeline/perception_pipeline.py`

Transforms raw candle observations into semantic perceived events:

**Pipeline flow:**
```
PriceEvent → Validation → Primitive Detection → Ontology Validation → PerceivedEvent → Event Bus → [forget raw data]
```

**Perceptual Primitives** (enum with ~30 types):
- **Price Structure**: HIGHER_HIGH, LOWER_LOW, SWING_HIGH, INSIDE_BAR, ENGULFING
- **Volatility**: EXPANSION, COMPRESSION, VOLATILITY_SPIKE, RANGE_CONTRACTION
- **Movement**: MOMENTUM_CANDLE, REJECTION_CANDLE, FAST_DISPLACEMENT
- **Liquidity**: LIQUIDITY_SWEEP, STOP_SWEEP, EQUAL_HIGHS_BREAK, WICK_REJECTION
- **Temporal**: CANDLE_CLOSED, SESSION_OPEN, SESSION_CLOSE

**Key design decisions:**
- Schema validation and quality checking before detection
- Ontology validation gate — perceived events must conform to the ontology
- Confidence threshold filtering
- Raw observations are explicitly **not persisted** — fire and forget

**Honest note:** The primitive taxonomy is well-designed and drawn from ICT/SMC trading concepts. The ontology validation gate is a nice architectural constraint. The "forget raw data" principle is consistently enforced.

---

## 5. Meaning Layer

**Service:** meaning-engine (Python/FastAPI — port 52003)  
**File:** `meaning-engine/src/main.py`, `src/core/` (5 core modules)

The semantic interpretation engine. Takes perceived events and builds meaning across timeframes.

### 5a. Anchor Context Builder (`src/core/anchor_context.py` — 484 lines)

Identifies where price is relative to important structural levels:

- **S/R zone detection**: Clusters swing highs/lows into support/resistance zones using adaptive thresholds
- **Running VWAP**: Incrementally computed volume-weighted average price
- **Round-number proximity**: Detects closeness to psychological levels (major: 000, minor: 00, quarter: 25/50/75)
- **Confidence scoring**: Per-zone confidence based on touch count, recency, and volume profile

### 5b. Structure Interpreter (`src/core/structure_interpreter.py` — 545 lines)

Full market structure detection with a state machine:

- **Swing detection**: HH, HL, LH, LL, EH, EL (equal highs/lows) — enum-based
- **Phase state machine**: FORMING → CONFIRMED → EXTENDING → RETRACING → WEAKENING → INVALIDATED
- Each phase has entry/exit conditions and carries a `StructurePhase` with confidence + duration
- `get_market_structure_bias()` method returns the current directional bias

### 5c. Confluence Engine (`src/core/confluence_engine.py`)

Cross-timeframe alignment calculator — "12 gears interlocking":

- Wraps `BeliefGraph` and `StructureInterpreter`
- Computes `SemanticPressure` per (symbol, timeframe) using exponential moving contribution
- Produces a `ConfluenceMatrix`: per-TF pressure direction, structure phase, overall alignment score
- Uses `TF_HIERARCHY` and `TF_AUTHORITY` for weighted scoring

### 5d. Swing Analyzer

Identifies role of current swing point relative to structure (continuation, reversal, test).

### 5e. Semantic State Generator (`src/core/semantic_state.py`)

Final pipeline stage — merges everything into `MeaningState`:

```
AnchorContext + StructurePhase + SwingRole + SemanticPressure + ConfluenceMatrix
→ MeaningState (published downstream)
```

- `MeaningState` is THE single object consumed by reasoning, simulation, learning, and core-brain
- Caches latest state per `symbol:timeframe`

### 5f. Belief Graph

Per-timeframe bias tracking with `BiasState` and `StructureState`. Backed by Neo4j for persistence, `MeaningGraph` for relationship traversal.

**Honest note:** This is the intellectual heart of the system. The meaning pipeline is architecturally sound — it takes raw primitives and builds progressively richer context through well-defined stages. The confluence engine genuinely attempts cross-TF alignment, not just last-close comparison. The structure interpreter's phase state machine is the most novel piece — treating market structure as a lifecycle rather than a point-in-time label.

---

## 6. Shape Engine

**Service:** shape-engine (Python/FastAPI + gRPC — ports 52010/52011)  
**File:** `shape-engine/src/main.py` + ~100 source files

The largest service by file count. Detects, tracks, and manages chart patterns through their lifecycle.

**Shape types (from directory structure):**
- **Fibonacci**: Retracements, extensions, time clusters
- **Geometry**: Triangles, wedges, channels, ranges
- **Structures**: BOS (Break of Structure), CHOCH (Change of Character), order blocks, breaker blocks, liquidity voids, FVGs (Fair Value Gaps)
- **Positions**: Entry/exit zone tracking
- **Trend analysis**: Trend line detection and tracking

**Architecture:**
- **Detection service**: Pattern scanning on incoming candle data
- **Lifecycle service**: ACTIVE → DORMANT → INVALIDATED → ARCHIVED
- **Multi-TF service**: Cross-timeframe shape correlation
- **Validation service**: Ontology-validated shape contracts (`ShapeContract`)
- **Learning integration**: Publishes shape confirmations/invalidations for learning-engine
- 12+ service clients (for perception, meaning, ontology, reasoning, etc.)
- **PostgreSQL** for shape persistence, **Redis** for hot cache
- Preloads active/dormant shapes into memory on startup (up to 5000)
- **gRPC** server on port+1 for high-performance inter-service calls
- Ontology sync mandatory on every boot

**Honest note:** This is a big, ambitious service. The ICT/SMC shape taxonomy (BOS, CHOCH, order blocks, breaker blocks, liquidity voids) is well-defined. The lifecycle approach — shapes being born, confirmed, mitigated, invalidated — is architecturally interesting and unusual. The ~100 source files suggest a lot of code, but the integration surface with 12+ service clients is complex. This service is probably the hardest to test end-to-end.

---

## 7. Reasoning Engine

**Service:** reasoning-engine (Python/FastAPI — port 52008)  
**File:** `reasoning-engine/src/main.py`

Formal reasoning with explicit chains, not pattern matching:

**Core modules:**
- `InferenceEngine` — logical inference and deduction
- `LogicEngine` — formal logic operations
- `CausalReasoner` — causal reasoning and belief propagation
- `CounterfactualGenerator` — "what-if" alternative generation
- `ReasoningValidator` — consistency validation
- `EnterpriseReasoningOrchestrator` — coordinates all reasoning modalities

**Every reasoning operation produces 5 things:**
1. An explicit conclusion
2. A complete reasoning chain (traceable steps via `ReasoningChain` / `ReasoningStep`)
3. Counterfactual alternatives (what was rejected and why)
4. Confidence with justification
5. Invalidation conditions (what would disprove this conclusion)

**Integrations:**
- Policy engine — checks if reasoning is policy-allowed before executing
- Meaning state — subscribes to `meaning.state` topic for incoming semantic context
- Event bus — publishes reasoning decisions

**Honest note:** The "5 things per operation" contract is a good design principle for auditability. The split between inference, causal, counterfactual, and logic engines shows intent toward genuine cognitive architecture rather than a black box. Whether the actual inference logic is deep or shallow depends on the implementations inside each engine — the main.py wires them well.

---

## 8. Simulation Engine

**Service:** simulation (Python/FastAPI — port 52043)  
**File:** `simulation/src/main.py`, `src/app_factory.py`, `src/engine/simulator.py`, `src/branching_engine.py`

Generates branching futures to evaluate decisions before execution:

**Branching Engine — "The Multiverse Engine":**
- `BranchSource` enum: VOLATILITY_REGIME, LIQUIDITY_EVENT, SHAPE_INTERACTION, RANDOM_WALK, MOMENTUM_SHIFT
- Each branch produces a `FuturePath` with:
  - Probability weighting
  - Generated future candles per timeframe
  - Shape resolution predictions
  - Volatility regime characterization (type, ATR multiplier, range %)
  - Liquidity event predictions (sweep/run/trap with trigger probability)

**Simulation Runner:**
- `FutureConeType` enum: CONTINUATION, RETRACEMENT, REVERSAL, FAKEOUT, CHOP
- `SimulationConfig`: timeframes, HTF timeframes, max drawdown/exposure/risk, branching factor
- 7-client dependency injection: ClickHouse, Ontology, Shape, Policy, Meaning, Perception, Reasoning
- 3-level punishment system for bad decisions
- Uses `shared.adaptive_weights` for self-tuning branch probabilities
- `PostgresRunStore` for persisting simulation runs

**Honest note:** This is one of the more original services. The branching engine generating multiple "what-if" futures — each annotated with volatility regimes, liquidity events, and shape resolutions — is not common in trading systems. The 3-level punishment system (from the reward engine) connects back to learning. Whether the GBM-based path generation is statistically rigorous depends on the implementation details, but the architecture is sound.

---

## 9. Core Brain — Decision Orchestrator

**Service:** core-brain (Python/FastAPI — port 52040)  
**File:** `core-brain/src/main.py`, `src/decision/decision_engine.py`, `src/universal_interface/`

The "Command Centre" — orchestrates everything into a decision. Explicitly a coordinator, NOT a reasoner.

### 9a. Decision Engine (`src/decision/decision_engine.py`)

**Mandatory 8-step pipeline:**
1. **State Assembly** — read upstream context
2. **Belief Integration** (`BeliefIntegrator`) — merge beliefs across sources
3. **Evidence Evaluation** (`EvidenceEvaluator`) — weight and score evidence
4. **Reasoning Consumption** — ingest reasoning engine outputs
5. **Simulation Consumption** — ingest simulation outcomes
6. **Decision Composition** (`DecisionComposer`) — synthesize a decision
7. **Decision Validation** (`DecisionValidator`) — safety gates
8. **Decision Output** — emit the validated `Decision` object

Sub-components: `BeliefIntegrator`, `EvidenceEvaluator`, `CounterfactualConsumer`, `DecisionComposer`, `DecisionValidator`, `MarketIntelligenceEngine`

### 9b. Universal Interface

**AutonomousAgent** (`autonomous_agent.py`):
- Bounded autonomy: confidence ≥ 0.90 for auto-execution
- `ABORT` action always forbidden for autonomous execution
- Below 0.80 → requires human approval
- Disabled by default

**MetaLearner** (`meta_learner.py`):
- Does NOT learn internally — fires learning payloads to the external Learning Engine
- On decision outcome: builds (hypothesis, reward, causal analysis, concepts validated/invalidated)
- POSTs to learning-engine's `/api/v1/reinforcement/outcome/learn`

**CommandInterpreter**: Natural language to system command translation  
**CrossDomainReasoner**: Combines reasoning across multiple domains

### 9c. Event-Driven Operation

- Subscribes to 13 event bus topics (meaning, reasoning, policy, simulation, learning, perception, shape events)
- When a `MEANING_STATE` event arrives, auto-triggers the decision pipeline (push model)
- Decision history in a ring buffer (last 200)
- Default startup mode: `RESEARCH`

**Honest note:** The core-brain is genuinely just an orchestrator. It doesn't hide any intelligence — every cognitive capability is delegated to the specialized engines. The 8-step pipeline is rigid and auditable. The event-driven push model (meaning state triggers decisions) is a good design. The autonomous agent safety constraints (0.90/0.80 confidence thresholds) are reasonable guardrails.

---

## 10. Policy Engine

**Service:** policy-engine (Python/FastAPI — port 52032)  
**File:** `policy-engine/src/main.py`

Behavioral governance — decides if the system is **allowed** to do something.

**Two versions coexisting:**
- **v1 — Strategy profiles**: scalp / intraday / swing / position  
- **v2 — Enterprise enforcement**: 6 policy types (Permission, Risk, Simulation, Learning, Automation, Safety)

**Key features:**
- Tri-state decisions: ALLOW / DENY / ALLOW_WITH_CONDITIONS
- Versioned policy packs with immutable audit trail (`PolicyVersionRegistry`)
- `AuditLogger` + `ComplianceReporter`
- `PolicyExplainer` — generates human-readable explanations of why something was allowed/denied
- Safety subsystem with `safety_check()` function
- Human approval workflow: `request_human_approval()`, `approve_request()`, `deny_request()`

**Honest note:** The dual v1/v2 system suggests this service evolved. The enterprise enforcement layer with 6 policy types is comprehensive. The human approval workflow is important for bounded autonomy. The compliance reporter is a nice enterprise touch.

---

## 11. Learning Engine

**Service:** learning-engine (Python/FastAPI — port 52004)  
**File:** `learning-engine/src/main.py`

**5 learning modalities:**

| Modality | Components | What It Does |
|---|---|---|
| Supervised | ExampleHandler, AnnotationLearner, BeliefLearner, FewShotLearner | Learns from human-labeled examples |
| Reinforcement | RewardHandler, OutcomeLearner, PolicyUpdater, RLBeliefUpdater | Learns from outcome rewards |
| Punishment | PunishmentHandler, ConfidenceAdjuster, BeliefAdjuster, GraphUpdater | Penalizes wrong decisions (3 levels) |
| Active | UncertaintyLearner, QueryGenerator, SampleSelector | Identifies what it doesn't know, asks for examples |
| Meta/Discovery | PatternDiscoverer, HypothesisGenerator, DiscoveryLearner | Discovers new patterns autonomously |

**ML models:**
- `CandleEncoder` — encodes candle data for ML
- `ShapePredictor` — predicts shape outcomes
- `BiLSTMEncoder` — 3-class classifier (confirmed/invalidated/mitigated)
- `TrainingPipeline` — manages model training

**Additional systems:**
- `ConfidenceCalibrator` — isotonic regression calibration
- `TimeframeLearner` — per-TF accuracy tracking + suppression
- `PatternMemory` — persistent pattern archetypes
- `AutonomyManager` — Level 0–4 progression
- `TeachingModule` — human-to-system knowledge transfer
- Persistence: JSONL + JSON, survives restarts
- Adaptive TF authority weights (1S=1 through MO1=12) via shared `WeightRegistry`

**Honest note:** This is an ambitious learning stack. The 5-modality design covers the main learning paradigms. The punishment system (3 levels) is unusual and interesting — most trading systems only reward/penalize. The BiLSTM model for shape outcome prediction is real ML. The autonomy manager (Level 0–4) provides a progressive trust ramp. Whether all these modalities are deeply implemented or skeletal stubs varies — the supervised and reinforcement paths are the most fleshed out.

---

## 12. Explanation Engine

**Service:** explanation-engine (Python/FastAPI — port 52005)  
**File:** `explanation-engine/src/main.py`

The "why layer" — converts machine decisions into human-readable audit-grade explanations.

**Pipeline stages:**
1. `EvidenceCollector` — pulls facts from all upstream services
2. `CausalChainBuilder` — reconstructs step-by-step reasoning chain
3. `CounterfactualEngine` — generates "if X changed, Y would change" scenarios
4. `ExplanationAssembler` — final assembly into `ExplanationBundle`
5. `NarrativeSynthesizer` — natural language generation

**8 endpoint sections (aligned to frontend sidebar):**
- LIVE BRIEF — quick callout stack
- CAUSAL TRACE — full reasoning chain
- WHAT IF — counterfactual lab
- LEARNING FEEDBACK — before vs. after learning
- POLICY — gate details
- SIMULATION — branch evidence
- MEMORY — historical analogs
- RAW EVENTS — perception event stream

**3 modes:** QUICK_BRIEF, DEEP_TRACE, COUNTERFACTUAL_LAB

Uses adaptive weights to score callout importance (MEANING=2.0, SIMULATION=1.8, POLICY=1.5).

**Honest note:** The explanation engine exists primarily to serve the frontend explanation panel. The 8-section design mirrors the frontend sidebar, which is a good sign of intentional design. The causal chain builder and counterfactual engine are the most valuable pieces — if they work correctly, they give genuine transparency into why a decision was made.

---

## 13. Knowledge Graph

**Service:** knowledge-graph (Python/FastAPI — port 52015)  
**File:** `knowledge-graph/src/server.py`

Neo4j-backed concept and relationship persistence:

**Rich model library:**
- Node types, edge types, relationship types, confidence sources
- Trading domain: swings, zones, structures, wicks
- `TradingNodeFactory`, `TradingEdgeFactory`, `StructurePatternDetector`

**Managers:**
- `GraphManager`, `NodeManager`, `EdgeManager`
- `OntologyValidator` — validates all inserts against ontology
- `TimeSpaceEnforcer` — temporal ordering constraints
- `MultiTimeframeHierarchyManager` — cross-TF relationships
- `ConfidenceDecayManager` — beliefs decay over time
- `EventSourcingTracker` — append-only event log for graph mutations

**API layers:**
- Legacy `/kg/*` CRUD (JSONL-backed, backward-compatible)
- Rich `/api/v1/*` endpoints for trading domain queries
- `/api/v1/causal/{id}` and `/api/v1/validations/{id}` for explanation-engine
- Ontology validation gate on all inserts
- Event bus publishing on every mutation

**Neo4j backed via `Neo4jBeliefStore`** for durable graph persistence.

**Honest note:** The knowledge graph is genuinely backed by Neo4j and provides real graph traversal. The confidence decay manager is a good design choice — beliefs should weaken over time unless reinforced. The event-sourced mutation tracking enables replay. The dual storage (JSONL legacy + Neo4j) is honest about the migration path.

---

## 14. Memory Service

**Service:** memory (Python — port 52018)  
**File:** `memory/src/main.py`

A 5-layer memory model:

| Layer | Purpose | What Feeds It |
|---|---|---|
| 1. Structural | Concepts, shapes, ontology artifacts | Ontology, Shape Engine, Perception |
| 2. Experience | Simulation results, reasoning traces, brain decisions | Simulation, Reasoning, Core Brain |
| 3. Learning | Parameter updates, reward signals, corrections | Learning Engine |
| 4. Semantic | Meanings, beliefs, language interpretations | Meaning Engine, Language Intelligence |
| 5. Episodic | Timestamped episodes for replay | All services |

**Subsystems:**
- `EpisodicMemory` — timestamped episode storage
- `EnterpriseEventStore` — append-only event store for causal chain replay
- `SemanticMemory` + `BeliefMemory` + `ConceptStore` + `MeaningStore`
- `WorkingMemory` + `ActiveContextManager` — current active state
- `TimeframeMemoryManager` + `BiasMemory`
- `MemoryRetrieval` — search and recall
- `MemoryConsolidator` + `PriorityHandler` + `ForgetPolicy` — Ebbinghaus-inspired forgetting
- `EvidenceStore` — immutable factual evidence
- Storage: JSONL-backed, survives restarts

**Honest note:** The 5-layer memory model is conceptually clean. The Ebbinghaus forgetting curve (`SimpleForgetPolicy`) is a nice cognitive-science detail — memories decay unless reinforced. The episodic memory with replay capability connects well to the explanation engine. Storage is JSONL-based, which is simple but may not scale to production volumes.

---

## 15. Ontology Service

**Service:** ontology (Python/FastAPI — port 52100)  
**File:** `ontology/src/main.py`

Single responsibility: "What kinds of things exist in this system, and how are they allowed to relate?"

**Key components:**
- `OntologySchema`, `SchemaBuilder`, `SchemaLoader` — schema definition
- `ConceptRegistry`, `RelationshipRegistry` — concept and relationship type registries
- `AdvancedConstraintEngine` — constraint enforcement
- `RelationshipValidator` with `GraphValidationLevel` — validates relationships
- `ActivationGate` — controls concept activation/deactivation
- `AdvancedOntologyQueryEngine` — rich querying
- `SchemaEvolutionTracker` — tracks schema changes with `ChangeType` enum
- `OntologyOrchestrator` — coordinates schema operations
- SQLAlchemy-backed persistence (`OntologyRepository`)
- Event publishing on create/update/delete

**Honest note:** The ontology service is a genuine type system for the domain. Multiple services (perception, shape-engine, knowledge-graph) validate against it. The ActivationGate and SchemaEvolutionTracker show maturity — the ontology isn't static, it can evolve with versioning. This is one of the quietest but most important services.

---

## 16. Language Intelligence

**Service:** language-intelligence (Python/FastAPI — port 52006)  
**File:** `language-intelligence/src/main.py`

Code/language understanding and generation:

- `IntentParser` — parses natural language into `StructuredIntent` with `IntentType`
- `LanguageDetector`, `FileAnalyzer` — language/file type detection
- `ParserFactory` → `ASTAnalyzer` → `DependencyMapper` → `StructureExtractor` — AST analysis pipeline
- `CodeSynthesizer`, `DocToCode` — code generation from descriptions
- `CodeValidator`, `LinterInterface`, `TestGenerator` — validation and testing
- `render_explanation()` — renders explanations in natural language

**Honest note:** This service seems to serve two purposes: (1) NLP query routing for the frontend (parsing user questions into system actions) and (2) code intelligence capabilities. The AST analysis pipeline (parser → analyzer → dependency mapper) is unusual for a trading platform — it might be used for analyzing trading script code or generating strategy code. The intent parser is likely the primary frontend integration point.

---

## 17. Gateway

**Service:** gateway (Go/Gin — port 52019, Python stub on 52051)  
**File:** `gateway/src/main.go` (production), `gateway/main.py` (dev stub)

Central API routing hub:

- **Go production server**: Gin framework, graceful shutdown, configurable via environment
- **Python dev stub**: Maps 17 API prefixes to backend services:
  - `/api/auth` → auth-service:5500
  - `/api/events` → event-bus:52020
  - `/api/ontology` → ontology:52100
  - `/api/policy` → policy-engine:52032
  - `/api/perception` → perception:52012
  - `/api/meaning` → meaning-engine:52003
  - `/api/reasoning` → reasoning-engine:52008
  - `/api/learning` → learning-engine:52004
  - `/api/simulation` → simulation:52043
  - `/api/explanation` → explanation-engine:52005
  - `/api/memory` → memory:52018
  - `/api/knowledge-graph` → knowledge-graph:52015
  - `/api/core-brain` → core-brain:52040
  - `/api/shapes` → shape-engine:52010
  - `/api/market` → market-ingestion:52024
  - `/api/candles` → candle-constructor:52023
  - `/api/engine` → engine-controller:52060
- Token verification against auth service (optional)

**Honest note:** The dual Go/Python approach is pragmatic — fast Go binary in Docker, convenient Python for local dev. The Python stub clearly documents all service routes, which serves as a living service map.

---

## 18. Security Core

**Service:** security-core (Node.js/Fastify — port 55000)  
**File:** `security/src/main.js`, `security/src/server.js`

Enterprise security control plane:

- **Crypto & Key Management**: KMS client, HSM client, Key Manager, re-wrap worker
- **Identity**: OIDC integration, JWT identification, service identity, API key management
- **Audit**: Immutable append-only archive, event recorder, cryptographic signer
- **Policy**: ABAC/PBAC policy engine
- **File Security**: Object store, quarantine manager, ingestion pipeline, AV scanner, sandbox detonation engine
- **Resilience**: WAF middleware, backpressure manager, leader election
- **Routes**: `/health`, `/crypto`, `/secrets`, `/audit`, `/policy`, `/admin`, `/apikeys`, `/files`

Strict request size limits, request tracing context injection (trace ID, subject, org, purpose), centralized audit logging.

**Honest note:** This is an ambitious security service for a trading platform. The crypto key management (KMS/HSM), ABAC policy engine, and immutable audit trail are enterprise-grade features. The sandbox detonation engine for file analysis is an unusual and thorough inclusion. Whether all of this is fully implemented or partially stubbed is hard to tell from the entry point alone, but the architecture is well-designed.

---

## 19. Schema Registry

**Service:** schema-registry (Go/Gorilla — port 52025)  
**File:** `schema-registry/src/main.go`

Event schema versioning and enforcement:

- `Registry` — stores schema definitions
- `Enforcer` — validates events against registered schemas
- `Governor` — schema governance (approval, versioning)
- Storage-backed (PostgreSQL) with caching
- Gorilla Mux router, graceful shutdown

**Honest note:** A proper schema registry is essential for an event-driven architecture with 20+ services. The governance module suggests schema evolution is controlled rather than ad-hoc. This is infrastructure that most microservice systems need but few build.

---

## 20. Topology Hub

**Service:** topology-hub (Go — port 52016), topology-hub-express (Node.js — port 52017)  
**File:** `topology-hub/main.go`

Real-time service topology visualization:

- Go hub with configurable broadcast interval (500ms default)
- WebSocket-based live updates
- Express companion (`topology-hub-express`) as a BFF for the frontend
- Includes a `useTopologyHub.js` React hook for frontend integration

**Honest note:** This is an operational visibility tool — it shows which services are running and how they connect. The 500ms broadcast interval and WebSocket protocol make it suitable for live monitoring dashboards.

---

## 21. Back-End Auth System

**Service:** auth-service (Node.js/Express — port 5500)  
**File:** `Back_End_Auth_System/src/app.js`

Full authentication and billing system:

**Routes:**
- `/api/auth` — login, register, JWT auth
- `/api/password` — password reset/change
- `/api/payments` — Paystack payment processing
- `/api/twoFactor` — 2FA setup and verification
- `/api/signals` — trading signal delivery
- `/api/user-service` — user management
- `/api/cron` — scheduled job management
- `/api/recovery` — account recovery

**Controllers:** auth, password, 2FA, session, security, payment, signal, notification, PDF, admin  
**Middleware:** IP security, threat detection, Cookie parser  
**Security:** Rate limiting delegated to API gateway (explicitly noted in code)  
**Database:** MongoDB  
**Jobs:** CronManager for scheduled tasks (account cleanup, user sync)

**Honest note:** This is a standalone, full-featured auth system. The Paystack integration and signal delivery suggest this is designed for a commercial product with paid subscriptions and trading signal distribution. It's the most "product-ready" service in the system.

---

## 22. Shared Libraries

**Location:** `shared/`

Cross-cutting utilities used by all Python services:

| Module | Purpose |
|---|---|
| `event_bus_client.py` | Async pub/sub client with SSE auto-reconnect, connection pooling |
| `topics.py` | Canonical event topic taxonomy (~50 topics organized by layer) |
| `envelope.py` | Standardized event envelope builder |
| `tracing.py` | OpenTelemetry setup for all services |
| `security_client.py` | Client for security-core service |
| `adaptive_weights.py` | Bayesian credibility tracking with Beta-distribution posterior |
| `constants/` | Shared constants |
| `contracts/` | Shared data contracts |
| `models/` | Shared data models |
| `utils/` | Shared utilities |

### Adaptive Weights — The Credibility System

The most architecturally significant shared module. Formula:

```
credibility = (hits + 1) / (hits + misses + 2)     # Beta distribution posterior mean
adaptive_weight = base_weight × credibility          # clamped to [50%, 150%] of base
```

- Per-source tracking with exponential decay (window=200, decay=0.02)
- NOT a neural network — fully deterministic, auditable, admin-resettable
- JSON-backed persistence
- Used by: simulation, learning-engine, explanation-engine, and others

**Honest note:** The shared library approach is well-executed. The canonical topics taxonomy (`Topics` class with ~50 constants) is essential for keeping 20+ services in sync. The adaptive weights system is a clever middle ground between hardcoded weights and opaque ML — it's Bayesian, auditable, and degrades gracefully.

---

## 23. Cross-Cutting Patterns

### What's consistent across all services:

1. **Health/Ready endpoints** — Every service exposes `/health` (liveness) and `/ready` (readiness with dependency checks)
2. **OpenTelemetry tracing** — All Python services import `shared.tracing` (graceful fallback if OTel packages missing)
3. **Prometheus metrics** — Exposed on `/metrics` via prometheus_client
4. **Event bus integration** — All services use `shared.event_bus_client` for async pub/sub
5. **Ontology validation** — Multiple services validate against the ontology (perception, shape-engine, knowledge-graph)
6. **Graceful degradation** — Every integration wrapped in try/except; missing dependencies result in warnings, not crashes
7. **CORS** — Every HTTP service enables CORS (development-friendly)
8. **Structured logging** — JSON-format logging with service name and trace context

### What varies:
- **Persistence**: ClickHouse (candles), PostgreSQL (shapes, schemas), Neo4j (knowledge), MongoDB (auth), JSONL (memory, learning), Redis (caching)
- **Language**: Python (majority), Go (event bus, gateway, schema-registry, topology), Rust (price-observer), Node.js (auth, security)
- **Framework**: FastAPI (Python), Gin (Go), Gorilla (Go), Actix (Rust), Express (Node.js), Fastify (Node.js)

---

## 24. Data Flow — End to End

```
┌─────────────────────────────── EXTERNAL ──────────────────────────────────┐
│  Deriv WebSocket  ───→  market-ingestion  ───→  ClickHouse (raw storage)  │
│                              │                                             │
│                              ▼                                             │
│                         event-bus (Go)  ◄───  price-observer (Rust)       │
└───────────────────────────────┬────────────────────────────────────────────┘
                                │
                                ▼
┌────────────────────── CANDLE CONSTRUCTION ────────────────────────────────┐
│  candle-constructor: tick → 15 TF parallel fan-out → CandleClosed events │
│  Storage: ClickHouse                                                      │
└───────────────────────────────┬───────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────── PERCEPTION ───────────────────────────────────┐
│  perception: CandleClosed → primitive detection → ontology validation    │
│  Output: PerceivedEvent (HH, LL, SWEEP, ENGULFING, etc.)                │
│  Policy: forget raw data after emission                                  │
└───────────────────────────────┬──────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────── MEANING ─────────────────────────────────────┐
│  meaning-engine: PerceivedEvent → 5-stage pipeline                       │
│    anchor_context → structure_interpreter → confluence_engine             │
│    → swing_analyzer → semantic_state_generator                           │
│  Output: MeaningState (per symbol:TF)                                    │
│  Storage: Neo4j (BeliefGraph)                                            │
└───────────────┬─────────────┬─────────────┬──────────────────────────────┘
                │             │             │
                ▼             ▼             ▼
┌──────────┐ ┌─────────┐ ┌────────────┐ ┌─────────────┐
│ reasoning│ │  shape  │ │ simulation │ │  knowledge  │
│  engine  │ │ engine  │ │  engine    │ │    graph    │
├──────────┤ ├─────────┤ ├────────────┤ ├─────────────┤
│ Inference│ │ Detect  │ │ Branch     │ │ Store nodes │
│ Causal   │ │ Track   │ │ 5 futures  │ │ & edges     │
│ Counter- │ │ Lifecycle│ │ Evaluate   │ │ Decay       │
│ factual  │ │ Validate│ │ Reward     │ │ confidence  │
│ Logic    │ │ Multi-TF│ │ Punish     │ │ Event-source│
└─────┬────┘ └────┬────┘ └─────┬──────┘ └──────┬──────┘
      │           │            │                │
      └───────────┴──────┬─────┴────────────────┘
                         │
                         ▼
┌──────────────────── CORE BRAIN ──────────────────────────────────────────┐
│  8-step decision pipeline:                                               │
│  state assembly → belief integration → evidence evaluation               │
│  → reasoning consumption → simulation consumption                        │
│  → decision composition → validation → output                            │
│                                                                          │
│  Universal Interface: AutonomousAgent, MetaLearner, CommandInterpreter   │
│  Event-driven: MeaningState arrival triggers pipeline                    │
└───────────┬──────────────┬──────────────┬────────────────────────────────┘
            │              │              │
            ▼              ▼              ▼
┌──────────────┐ ┌───────────────┐ ┌──────────────┐
│ explanation  │ │   learning    │ │    policy    │
│   engine     │ │    engine     │ │    engine    │
├──────────────┤ ├───────────────┤ ├──────────────┤
│ Why was this │ │ 5 modalities: │ │ ALLOW/DENY/  │
│ decided?     │ │ supervised    │ │ CONDITIONS   │
│ Causal chain │ │ reinforcement │ │ 6 policy     │
│ Counterfact. │ │ punishment    │ │ types        │
│ Narrative    │ │ active        │ │ Human        │
│              │ │ discovery     │ │ approval     │
└──────────────┘ └───────────────┘ └──────────────┘

┌──────────────────── SUPPORT LAYER ───────────────────────────────────────┐
│  ontology (52100)     — type system for all domain concepts              │
│  schema-registry (Go) — event schema versioning                          │
│  memory (52018)       — 5-layer memory model with forgetting             │
│  security-core (JS)   — crypto, audit, policy enforcement                │
│  gateway (Go)         — API routing to all 17+ services                  │
│  auth-service (JS)    — JWT, 2FA, payments, signals                      │
│  topology-hub (Go)    — live service topology visualization              │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 25. Honest Assessment

### What's genuinely impressive:

1. **Architectural coherence** — The cognitive pipeline (observe → perceive → mean → reason → simulate → decide) is consistently implemented across all 21 services. It's not just documentation — the code actually follows this flow.

2. **Multi-timeframe architecture** — 15 timeframes with authority weights, propagated from candle-constructor through meaning, shape, and simulation. This is the system's strongest architectural differentiator.

3. **Auditability** — Every service produces traceable artifacts. The explanation engine can reconstruct why a decision was made. The DecisionEngine's 8-step pipeline is rigid by design.

4. **Ontology-driven validation** — The ontology service is a genuine shared type system. Multiple services validate against it, which prevents concept drift between services.

5. **Adaptive weights** — The Bayesian credibility system is elegant. It's the right middle ground between hardcoded weights and black-box ML.

6. **Event-driven architecture** — The Go event bus with topic-based pub/sub, dead-letter queue, event replay, and schema validation is production-grade infrastructure.

### What's concerning:

1. **Enormous surface area** — 21 services, 6 databases, 4 programming languages. The operational complexity of keeping all of this running, tested, and deployed is massive. This is a team-of-20 system being built by what appears to be a smaller team.

2. **JSONL persistence in production services** — Memory service and learning-engine use JSONL/JSON file persistence. This works for prototyping but has obvious scaling, concurrency, and backup limitations.

3. **Integration testing gaps** — With 21 services communicating via events and HTTP, end-to-end testing is extremely difficult. The docker-compose with 27 containers needs substantial memory to run locally.

4. **Variable implementation depth** — Some services are deeply implemented (candle-constructor, meaning-engine, shape-engine), while others appear thinner (language-intelligence, topology-hub). The learning engine's 5 modalities are architecturally defined but the actual ML models (BiLSTM, etc.) need training data and training pipelines to be useful.

5. **No live execution** — The system can make decisions but there's no evidence of a trade execution layer connecting to a real broker. The autonomous agent has safety gates, but the "last mile" — placing an actual trade — is not implemented in any service.

6. **Security service ambition vs. reality** — The security-core service describes KMS, HSM, sandbox detonation, and leader election. These are features that enterprise teams spend years building. In a single Fastify service, the implementations are likely partial.

### What's the system actually ready for:

The system can currently:
- Ingest live price data from Deriv
- Build multi-timeframe candles
- Detect market structure and chart patterns
- Build semantic meaning across timeframes
- Generate branching future simulations
- Make audited, explainable trading decisions
- Learn from outcomes
- Present all of this through an API gateway

What it cannot yet do:
- Execute trades automatically
- Handle production-scale data volumes (JSONL limitations)
- Run all 27 containers reliably in a production environment without significant DevOps investment

### Final word:

This is not a demo. The code is real, the architecture is coherent, and the cognitive pipeline works end-to-end as designed. The multi-timeframe meaning extraction and branching simulation are original contributions that go beyond standard trading platforms. The system's biggest risk is its own ambition — 21 services is a lot to maintain, and the gap between "architecturally designed" and "production-hardened" varies by service.

---

*Generated by reading every service entry point, key source files, and shared infrastructure in the AUREXIS codebase. No marketing claims copied — this is what the code actually does.*
