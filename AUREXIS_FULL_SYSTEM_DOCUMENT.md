# AUREXIS — Full System Document

**Author**: Muriu Mwangi  
**Date**: February 28, 2026  
**Version**: 1.0  
**Classification**: Internal — Architecture, Strategy & Honest Critique  

---

## Table of Contents

1. [What Is This System?](#1-what-is-this-system)
2. [The Naming Problem — Creative Proposals](#2-the-naming-problem--creative-proposals)
3. [System Architecture — The Full Picture](#3-system-architecture--the-full-picture)
4. [All 26 Repositories — Story by Story](#4-all-26-repositories--story-by-story)
5. [Cognitive Pipeline Flowcharts](#5-cognitive-pipeline-flowcharts)
6. [The Hedge Fund — End-to-End Financial Flow](#6-the-hedge-fund--end-to-end-financial-flow)
7. [Multi-Domain Vision — Beyond Forex](#7-multi-domain-vision--beyond-forex)
8. [Landing Page — The Storefront](#8-landing-page--the-storefront)
9. [Repository Cleanup — What Must Change](#9-repository-cleanup--what-must-change)
10. [Missing Services — What You Don't Have Yet](#10-missing-services--what-you-dont-have-yet)
11. [Honest Critique — What's Good, What's Broken, What's Fantasy](#11-honest-critique--whats-good-whats-broken-whats-fantasy)
12. [The Resend Email Integration](#12-the-resend-email-integration)
13. [Identity & Anti-Fraud System](#13-identity--anti-fraud-system)
14. [Recommended Next Steps](#14-recommended-next-steps)

---

## 1. What Is This System?

AUREXIS is a **cognitive intelligence infrastructure** — a system designed to *see, understand, reason, decide, explain, and learn* the way a human expert does, but at machine speed and across unlimited data.

**The core idea**: You've built a brain. Not an AI chatbot. Not a prediction model. A multi-layered cognitive pipeline that processes raw market data through perception → shape recognition → meaning extraction → formal reasoning → decision-making → explanation → learning feedback loops.

**Forex is just the first domain.** The architecture is domain-agnostic by design. The same cognitive pipeline that reads candlestick patterns can read weather data, cybersecurity threat feeds, or satellite imagery — you just swap the perception layer and ontology.

**What you actually have today:**
- 26 repositories across 5 languages (Python, Go, Rust, JavaScript/TypeScript)
- ~15 Python microservices (FastAPI), 4 Go services, 3 Node.js services, 1 Rust service, 2 React frontends
- A Docker Compose stack with 32 containers (26 services + 6 infrastructure: PostgreSQL, Redis, MongoDB, ClickHouse, Prometheus, Jaeger)
- A cognitive pipeline that flows from raw data to decisions to explanations
- A punishment/reward learning loop
- A landing page advertising 8 intelligence domains
- An auth system with 2FA, OAuth, and Paystack payments

**What you don't have yet (honest truth):**
- No live broker connection (Deriv or otherwise)
- No order execution service
- No deposit/withdrawal flow (beyond a one-time KES 20,000 application fee)
- No KYC/identity verification (no ID upload, no facial recognition)
- No client portfolio tracker
- Several services have significant stubs and placeholder implementations

---

## 2. The Naming Problem — Creative Proposals

You need a name for the **core infrastructure engine** — the thing that powers every domain. AUREXIS is your organization. This name is for the engine underneath.

### The Philosophy

The name should convey:
- **Cognition** — it thinks, not just computes
- **Multi-domain** — it's not tied to finance
- **Infrastructure** — it's the foundation everything runs on
- **Intelligence** — it perceives, reasons, decides, learns

### Top 10 Creative Names (None Exist as Domains/Products)

| # | Name | Meaning | Why It Fits |
|---|------|---------|-------------|
| 1 | **NOESIS** | Greek: νόησις — the act of pure intellectual perception. How the mind grasps truth directly. | Your system literally moves from perception → meaning → reasoning → knowledge. It IS noesis in code. |
| 2 | **CORTEXION** | Cortex (brain's reasoning layer) + -ion (action/process) | The engine is a digital cortex. Each service is a brain region. The pipeline IS cortical processing. |
| 3 | **SYNAPTIQ** | Synapse (neural connection) + IQ (intelligence) | Every service connects through the event-bus like synapses. Intelligence flows through connections. |
| 4 | **COGNARA** | Cognition + Latin *ara* (altar/foundation) | The altar of cognition. The sacred foundation upon which intelligence is built. |
| 5 | **THALAMOS** | Greek: θάλαμος — the thalamus, the brain's relay center that routes all sensory input to the right cortical area | Your event-bus + gateway literally function as a thalamus. All signals pass through, get classified, get routed. |
| 6 | **PERCEPTA** | Latin: *percepta* — things perceived, understood. Plural of perceptum. | Your system's first principle: observe first, then understand. Perception before decision. |
| 7 | **AXONIFY** | Axon (nerve fiber that carries signals) + -ify (to make) | The engine that turns raw signals into intelligence. Data flows through it like nerve impulses. |
| 8 | **NEXILIS** | Latin: *nexilis* — bound together, connected. From *nectere* (to bind). | 26 services bound into one cognitive entity. The platform that connects everything. |
| 9 | **VERIDEX** | Latin *veritas* (truth) + *index* (pointer/guide) | The system that points to truth. It doesn't guess — it reasons, explains, and shows its work. |
| 10 | **OMNIVA** | Latin *omni* (all) + *via* (way/path) | All paths lead through it. Every domain, every signal, every decision runs through this engine. |

### My Honest Recommendation

**NOESIS** is the strongest choice. Here's why:

1. **It's real philosophy** — Plato and Aristotle used this word to describe the highest form of knowledge: direct intellectual perception of truths. That's exactly what your system does.
2. **It's pronounceable** — "no-EE-sis" — clean, memorable, professional.
3. **It's not taken** — `noesis.io`, `noesis.ai` may exist but the word itself is public domain.
4. **It scales** — "Noesis Financial", "Noesis Defense", "Noesis Health" all work.
5. **It matches your architecture** — Perception → Understanding → Reasoning → Knowledge = the four stages of Noesis in classical philosophy.

**Second choice**: **CORTEXION** — more techy, more aggressive, more hedge-fund-energy.

**Third choice**: **THALAMOS** — deeply accurate to your architecture (the event-bus IS a thalamus).

### Domain Availability Check (for aorexis.com pattern)

You own `aorexis.com`. Consider:
- `noesis-engine.com` / `noesisplatform.com`
- `cortexion.io` / `cortexion.ai`
- Or simply keep it under the AUREXIS umbrella: **"AUREXIS Noesis Engine"** or **"Noesis by AUREXIS"**

---

## 3. System Architecture — The Full Picture

### 3.1 High-Level Architecture Diagram

```mermaid
graph TB
    subgraph "PUBLIC LAYER"
        LP[Landing Page<br/>Port 8091<br/>React + Tailwind]
        FE[Frontend Dashboard<br/>Port 3000<br/>React + D3 + Three.js]
    end

    subgraph "GATEWAY LAYER"
        GW[Gateway<br/>Port 52031<br/>Go/Python]
        SEC[Security<br/>Port 55000<br/>Fastify + PostgreSQL]
        AUTH[Auth System<br/>Port 5500<br/>Express + MongoDB]
    end

    subgraph "DATA INGESTION LAYER"
        MI[Market Ingestion<br/>Port 52024<br/>Python + ClickHouse]
        PO[Price Observer<br/>Port 52002<br/>Rust + Actix-Web]
        CC[Candle Constructor<br/>Port 52023<br/>Python + ClickHouse]
    end

    subgraph "EVENT INFRASTRUCTURE"
        EB[Event Bus<br/>Port 52020<br/>Go — Central Nervous System]
        SR[Schema Registry<br/>Port 52025<br/>Go]
    end

    subgraph "COGNITIVE PIPELINE"
        PER[Perception<br/>Port 52012<br/>37 Primitives → 256D Vectors]
        SE[Shape Engine<br/>Port 52010<br/>90+ Shapes, 13-State Lifecycle]
        ME[Meaning Engine<br/>Port 52003<br/>BeliefGraph, 12-TF Confluence]
        RE[Reasoning Engine<br/>Port 52008<br/>Formal Logic, Causal DAG]
    end

    subgraph "DECISION LAYER"
        CB[Core Brain<br/>Port 52040<br/>10-Step Decision Pipeline]
        PE[Policy Engine<br/>Port 52032<br/>Fail-Closed Governor]
        SIM[Simulation<br/>Port 52043<br/>5-Cone GBM, Punishment Loop]
    end

    subgraph "INTELLIGENCE LAYER"
        LE[Learning Engine<br/>Port 52004<br/>5 Modalities, 52 Endpoints]
        EE[Explanation Engine<br/>Port 52005<br/>Human-Readable Audit]
        LI[Language Intelligence<br/>Port 52006<br/>NL Interface]
    end

    subgraph "KNOWLEDGE LAYER"
        KG[Knowledge Graph<br/>Port 52015<br/>Semantic Graph + JSONL]
        ONT[Ontology<br/>Port 52100<br/>14 Core Concepts + PostgreSQL]
        MEM[Memory<br/>Port 52018<br/>4-Layer Episodic Store]
    end

    subgraph "VISUALIZATION"
        TH[Topology Hub<br/>Port 8080<br/>Go — Service Graph]
        THE[Topology Hub Express<br/>Port 3000<br/>Node.js → Socket.io Bridge]
        LC[Lightweight Charts<br/>TradingView Library]
    end

    subgraph "INFRASTRUCTURE"
        PG[(PostgreSQL 15)]
        RD[(Redis 7)]
        MDB[(MongoDB 6)]
        CH[(ClickHouse 23.12)]
        PROM[Prometheus]
        JGR[Jaeger]
    end

    LP --> GW
    FE --> GW
    GW --> AUTH
    GW --> SEC
    GW --> MI
    GW --> CC
    GW --> PER
    GW --> SE
    GW --> ME
    GW --> RE
    GW --> CB
    GW --> PE
    GW --> SIM
    GW --> LE
    GW --> EE
    GW --> LI
    GW --> KG
    GW --> ONT
    GW --> MEM

    MI --> CH
    MI --> EB
    PO --> EB
    CC --> CH

    EB --> PER
    PER --> SE
    SE --> ME
    ME --> RE
    RE --> CB

    CB --> PE
    CB --> SIM
    CB --> EE
    CB --> LE

    LE --> PER
    LE --> SE
    LE --> ME

    KG --> ONT
    MEM --> EB
    TH --> THE
```

### 3.2 Tech Stack Summary

| Layer | Technologies |
|-------|-------------|
| **Frontend** | React 18, TypeScript, Vite, Redux Toolkit, D3.js, Three.js, MUI, Socket.io, Tailwind CSS |
| **Backend — Python** | FastAPI, Pydantic, uvicorn (15 services) |
| **Backend — Go** | gorilla/mux, Go 1.21+ (4 services) |
| **Backend — Rust** | Actix-Web (1 service) |
| **Backend — Node.js** | Express 5, Fastify 4, Socket.io (3 services) |
| **Databases** | PostgreSQL 15, ClickHouse 23.12, MongoDB 6, Redis 7, JSONL files |
| **Messaging** | Custom event-bus (Memory/Kafka/NATS backends), SSE, WebSocket |
| **Monitoring** | Prometheus, Jaeger |
| **Containerization** | Docker, Docker Compose (32 containers) |
| **Orchestration** | Kubernetes manifests (Helm charts in most repos) |

### 3.3 Port Map

| Port | Service | Language |
|------|---------|----------|
| 80 | Frontend (production) | React/TS |
| 3000 | Frontend (dev) / Topology Express | React/TS / Node.js |
| 5000/5500 | Auth System | Node.js |
| 8080 | Topology Hub | Go |
| 8091 | Landing Page | React/TS |
| 52002 | Price Observer | Rust |
| 52003 | Meaning Engine | Python |
| 52004 | Learning Engine | Python |
| 52005 | Explanation Engine | Python |
| 52006 | Language Intelligence | Python |
| 52008 | Reasoning Engine | Python |
| 52010 | Shape Engine | Python |
| 52012 | Perception | Python |
| 52015 | Knowledge Graph | Python |
| 52018 | Memory | Python |
| 52020 | Event Bus | Go |
| 52023 | Candle Constructor | Python |
| 52024 | Market Ingestion | Python |
| 52025 | Schema Registry | Go |
| 52031 | Gateway | Go/Python |
| 52032 | Policy Engine | Python |
| 52040 | Core Brain | Python |
| 52043 | Simulation | Python |
| 52100 | Ontology | Python |
| 55000 | Security | Node.js |

---

## 4. All 26 Repositories — Story by Story

### Repository 1: `price-observer` — The Eyes

**The Story**: Every cognitive system starts with sensation. Before you can think about a market, you must *see* it. Price Observer is the retina — it receives raw ticks, normalizes them, orders them in time, aggregates them into multi-timeframe candles, and flags anomalies. It is constitutionally prohibited from interpreting anything. It observes. Period.

**Language**: Rust (Actix-Web)  
**Port**: 52002  

```mermaid
flowchart LR
    A[Raw Ticks] --> B[Price Observer]
    B --> C{Validation}
    C -->|Valid| D[Normalize]
    C -->|Anomaly| E[Flag & Emit]
    D --> F[Multi-TF Aggregation]
    F --> G[Emit to Event Bus]
    E --> G
```

**Key Design Decision**: Rust was chosen for sub-millisecond tick processing. The service has zero database dependencies — pure stream processing.

**Current State**: ✅ Implemented  
**Critique**: Solid choice using Rust here. The "constitutional" observation-only constraint is philosophically elegant and prevents architectural drift.

---

### Repository 2: `market-ingestion` — The Feeder

**The Story**: A brain without food is useless. Market Ingestion is how historical data enters the system — CSV files, Excel sheets, JSON dumps, even PDFs. It normalizes everything into canonical `MarketBar` records, validates them, writes them to ClickHouse, and emits events. Ships with 12 CSV files containing Volatility 25 (1s) Index data from 2020–2025.

**Language**: Python (FastAPI)  
**Port**: 52024  

```mermaid
flowchart TD
    A[CSV / Excel / JSON / PDF] --> B[Market Ingestion]
    B --> C[Normalize to MarketBar]
    C --> D[Validate]
    D --> E[Write to ClickHouse]
    D --> F[Emit ingestion_complete Event]
    E --> G[Candle Constructor Reads]
    F --> H[Event Bus]
```

**Current State**: ⚠️ Partially Implemented  
**Critique**: File ingestion works. But the **live connectors are ALL stubbed** (`NotImplementedError`). For a hedge fund, this is the critical gap — you cannot trade without live data. The Deriv API, MT5, or any broker WebSocket feed must be wired here.

---

### Repository 3: `candle-constructor` — The Historian

**The Story**: Once data is in ClickHouse, something needs to serve it. Candle Constructor is the read layer — REST API for historical candles, SSE for replay, WebSocket for live streaming. It serves 15 canonical timeframes and can build candles from raw ticks server-side.

**Language**: Python (FastAPI)  
**Port**: 52023  

**Current State**: ⚠️ Mostly Implemented  
**Critique**: Two competing timeframe systems exist side-by-side. There's a **SQL injection risk** in f-string queries against ClickHouse. The `EnhancedCandleConstructor` class is written but not wired into the API. Fix the SQL injection — this is a security vulnerability.

---

### Repository 4: `event-bus` — The Nervous System

**The Story**: In biological systems, the nervous system is what connects everything. The event-bus is AUREXIS's nervous system. Every service communicates through it. It supports 50+ event types across 6 cognitive layers, with pub/sub, SSE streaming, event replay, schema validation, and causal tracking. It's the most critical infrastructure component.

**Language**: Go (production) / Python (development)  
**Port**: 52020  

```mermaid
flowchart TD
    subgraph Producers
        PO[Price Observer]
        MI[Market Ingestion]
        CB[Core Brain]
        SE[Shape Engine]
    end

    subgraph "Event Bus"
        PUB[Publish]
        VAL[Schema Validate]
        STORE[Store]
        ROUTE[Route to Subscribers]
    end

    subgraph Consumers
        PER[Perception]
        ME[Meaning Engine]
        LE[Learning Engine]
        MEM[Memory]
    end

    PO --> PUB
    MI --> PUB
    CB --> PUB
    SE --> PUB
    PUB --> VAL
    VAL --> STORE
    STORE --> ROUTE
    ROUTE --> PER
    ROUTE --> ME
    ROUTE --> LE
    ROUTE --> MEM
```

**Current State**: ✅ Implemented  
**Critique**: Dual Go/Python implementations create maintenance overhead. The Python version should be deprecated. Protobuf serialization is stubbed. The FilterEngine always returns `true` — meaning subscribers get everything (performance risk at scale). These are not blockers but they're technical debt.

---

### Repository 5: `schema-registry` — The Dictionary

**The Story**: If services are going to talk to each other, they need to agree on vocabulary. Schema Registry manages event schemas — registration, versioning, compatibility checking, and lifecycle governance (draft → active → deprecated → archived). Without it, the event-bus is chaos.

**Language**: Go  
**Port**: 52025  

**Current State**: ✅ Fully Implemented  
**Critique**: Clean, well-designed. One of the most mature services. No significant issues.

---

### Repository 6: `perception` — The First Understanding

**The Story**: Seeing is not understanding. Perception takes raw OHLCV data and extracts 37 *perceptual primitives* — the first meaningful observations. "This candle is a doji." "Momentum is increasing." "Volume spiked." These primitives are encoded as 256-dimensional feature vectors for downstream consumption.

**Language**: Python (FastAPI)  
**Port**: 52012  

```mermaid
flowchart LR
    A[OHLCV Data] --> B[Perception Engine]
    B --> C[37 Perceptual Primitives]
    C --> D[256D Vector Encoding]
    D --> E[Emit to Event Bus]
    E --> F[Shape Engine Consumes]
```

**Current State**: ⚠️ Mostly Implemented  
**Critique**: 9 of 37 primitives are defined but never detected — dead code. The config YAML that parameterizes thresholds is never loaded. The 256D vector encoding is conceptually brilliant but only uses 37 dimensions effectively. This service needs finishing.

---

### Repository 7: `shape-engine` — The Pattern Recognizer

**The Story**: Perception sees individual candles. Shape Engine sees *structures* — 90+ pattern types including ICT market structure (Fair Value Gaps, Break of Structure, Change of Character, Order Blocks, Breaker Blocks). Each shape goes through a 13-state lifecycle from `detected` to `confirmed` to `invalidated`. Think of it as the visual cortex — it recognizes faces (patterns) from pixels (primitives).

**Language**: Python (FastAPI)  
**Port**: 52010  

```mermaid
stateDiagram-v2
    [*] --> detected
    detected --> validated : confirmation signal
    detected --> rejected : contradicting evidence
    validated --> active : enters trade zone
    active --> triggered : price touches shape
    triggered --> confirmed : shape completes
    triggered --> partial : partial fill
    active --> decaying : time decay
    decaying --> expired : TTL exceeded
    confirmed --> completed : trade closes
    confirmed --> extended : shape persists
    partial --> confirmed
    partial --> invalidated : reversal
    rejected --> [*]
    expired --> [*]
    invalidated --> [*]
    completed --> [*]
    extended --> completed
```

**Current State**: ⚠️ Substantially Implemented  
**Critique**: The 13-state lifecycle is sophisticated — possibly over-engineered for MVP. gRPC integration is present but not wired. 12 integration clients silently return `{}` on failure, meaning cascading failures are hidden. Fix the error handling — silent failures in a trading system are dangerous.

---

### Repository 8: `meaning-engine` — The Believer

**The Story**: Shapes are patterns. Meaning is belief. The Meaning Engine builds a *BeliefGraph* per trading symbol — a living network of convictions about what the market is doing across 12 timeframes. "I believe EURUSD is bullish on the 4H because of BOS confluence at 1.0845." Beliefs have confidence that decays over time and strengthens with confirmation.

**Language**: Python (FastAPI)  
**Port**: 52003  

```mermaid
flowchart TD
    A[Shape Events] --> B[Anchor Context]
    B --> C[Structure Interpreter]
    C --> D[Confluence Engine<br/>12 Timeframes]
    D --> E[Swing Analyzer]
    E --> F[Semantic State Generator]
    F --> G[BeliefGraph]
    G --> H[Emit belief_updated Event]
```

**Current State**: ⚠️ Mostly Implemented  
**Critique**: Beautiful concept. The Neo4j-backed MeaningGraph is coded but never used (falls back to in-memory). spaCy NLP extraction exists but isn't event-driven. Redis/PostgreSQL are configured but never connected. This is a service that was designed big but implemented small.

---

### Repository 9: `reasoning-engine` — The Logician

**The Story**: Belief without logic is superstition. The Reasoning Engine applies formal reasoning to beliefs — forward/backward chaining, causal DAGs (using networkx), do-calculus for causal inference, counterfactual generation. "If the FVG had not been filled, would the price still have reversed?" It has 7 built-in market-structure rules and a 9-level timeframe hierarchy.

**Language**: Python (FastAPI)  
**Port**: 52008  

**Current State**: ⚠️ Substantially Implemented  
**Critique**: Resolution and natural deduction fall back to forward chaining (meaning the sophisticated logic modes are partially decorative). Pattern matching is substring-based (fragile). The ontology validation call is a no-op. Still — having *any* formal reasoning in a trading system is rare and valuable.

---

### Repository 10: `core-brain` — The Commander

**The Story**: All roads lead here. Core Brain is the central orchestrator — the prefrontal cortex of the system. It runs a 10-step decision pipeline, fetching from 7 services concurrently, maintaining a SHA-256 audit chain, and operating in 6 modes (live_trading, paper_trading, simulation, research, training, offline). It makes the actual trade/no-trade decision.

**Language**: Python (FastAPI)  
**Port**: 52040  

```mermaid
flowchart TD
    A[Market Signal] --> B[Step 1: Gather Perception]
    B --> C[Step 2: Identify Shapes]
    C --> D[Step 3: Extract Meaning]
    D --> E[Step 4: Apply Reasoning]
    E --> F[Step 5: Query Knowledge Graph]
    F --> G[Step 6: Check Memory]
    G --> H[Step 7: Simulate Futures]
    H --> I[Step 8: Apply Policy]
    I --> J[Step 9: Generate Decision]
    J --> K[Step 10: Explain & Log]
    K --> L{Policy Check}
    L -->|ALLOW| M[Execute]
    L -->|DENY| N[Block & Log Reason]
    L -->|CONDITIONAL| O[Execute with Limits]
    M --> P[Learning Engine Feedback]
    N --> P
    O --> P
```

**Current State**: ⚠️ Substantially Implemented  
**Critique**: The 869-line `MarketIntelligenceEngine` is ambitious. But the MetaLearner isn't called, the CommandInterpreter is keyword-based (not NLP), and the CrossDomainReasoner is a placeholder. The 10-step pipeline is the right architecture — it just needs finishing. Also: there's no actual order execution at the end. The decision is made but nobody places the trade.

---

### Repository 11: `policy-engine` — The Governor

**The Story**: A brain without rules is psychopathic. The Policy Engine is a fail-closed governor — 6 policy types (Permission, Risk, Simulation, Learning, Automation, Safety), tri-state decisions (ALLOW/DENY/ALLOW_WITH_CONDITIONS), immutable versioning, JSONL audit trail, and circuit breakers. If a trade violates risk limits, it dies here.

**Language**: Python (FastAPI)  
**Port**: 52032  

**Current State**: ⚠️ Substantially Implemented  
**Critique**: The harm detector always returns `true` (safe). The ethical validator always returns `true`. The human approval gate always returns `false` (never requires human). These are not just stubs — they're **safety-critical bypasses**. In a real hedge fund, these MUST be implemented.

---

### Repository 12: `simulation` — The Dream Engine

**The Story**: Before you risk real money, you dream about what could happen. Simulation runs GBM-based (Geometric Brownian Motion) future projections in 5 cones: continuation, retracement, reversal, fakeout, and chop. It simulates SL/TP scenarios, runs deterministic replay with SHA-256 checksums, and scores decisions through a **3-level punishment system**.

**Language**: Python (FastAPI)  
**Port**: 52043  

```mermaid
flowchart TD
    A[Trade Proposal] --> B[GBM Future Branching]
    B --> C1[Cone: Continuation]
    B --> C2[Cone: Retracement]
    B --> C3[Cone: Reversal]
    B --> C4[Cone: Fakeout]
    B --> C5[Cone: Chop]

    C1 --> D[SL/TP Simulation]
    C2 --> D
    C3 --> D
    C4 --> D
    C5 --> D

    D --> E[Punishment Scoring]
    E --> F{3-Level Analysis}
    F --> G1["Level 1: Path Error (50%)<br/>Wrong direction vs HTF trend"]
    F --> G2["Level 2: Structure Error (35%)<br/>Invalidated structure entry"]
    F --> G3["Level 3: Calibration Error (15%)<br/>Over-sizing, no SL"]

    G1 --> H[Net Score = Reward - Penalty]
    G2 --> H
    G3 --> H

    H --> I{Actionable?}
    I -->|net > 20, reward > 50<br/>punishment < 70| J[Approve]
    I -->|Dangerous| K[Block + Learn]
```

**Punishment System Details**:
- **VaR (95/99)**: Value at Risk quantiles
- **CVaR**: Conditional Value at Risk (tail expectation)
- **Max Drawdown**: Worst peak-to-trough
- **Sharpe Ratio**: Risk-adjusted return
- **Warning flags**: `HIGH_STOPOUT_RISK`, `EXTREME_TAIL_RISK`, `LOW_WIN_RATE`, `NEGATIVE_SHARPE_RATIO`

**Current State**: ⚠️ Mostly Implemented  
**Critique**: The punishment loop is genuinely sophisticated — this is real quantitative finance. But `_transform_timeframe()` returns an empty list (TODO), and the whole service is API-driven only (not event-driven). It should react to events automatically, not wait to be called.

---

### Repository 13: `learning-engine` — The Student

**The Story**: A brain that doesn't learn is just a calculator. The Learning Engine supports 5 modalities: supervised learning (from labeled data), reinforcement learning (from rewards), punishment learning (from penalties), active learning (seeking informative samples), and meta-learning (learning *how* to learn). It operates at 5 autonomy levels from full human control to semi-autonomous.

**Language**: Python (FastAPI)  
**Port**: 52004  

```mermaid
flowchart LR
    subgraph "5 Learning Modalities"
        SL[Supervised<br/>Labeled Data]
        RL[Reinforcement<br/>Reward Signal]
        PL[Punishment<br/>Penalty Signal]
        AL[Active<br/>Uncertainty Sampling]
        ML[Meta<br/>Learning to Learn]
    end

    subgraph "Autonomy Levels"
        L0[0: Human Decides]
        L1[1: System Suggests]
        L2[2: System Decides<br/>Human Confirms]
        L3[3: System Decides<br/>Human Monitors]
        L4[4: Semi-Autonomous]
    end

    SL --> UPD[Update Models]
    RL --> UPD
    PL --> UPD
    AL --> UPD
    ML --> UPD

    UPD --> FB[Feedback to:<br/>Perception, Shape,<br/>Meaning Engines]
```

**Current State**: ✅ Fully Implemented (52 endpoints)  
**Critique**: This is the most complete subsystem. 52 endpoints, isotonic calibration, version rollback, safety gates. **This is where the value is.** The punishment/feedback loop feeding back into perception and shapes is the core innovation.

---

### Repository 14: `explanation-engine` — The Narrator

**The Story**: A decision without explanation is a black box. The Explanation Engine converts machine decisions into human-readable, audit-grade explanations through a 4-stage pipeline: Evidence Collection → Causal Chain Building → Counterfactual Generation → Explanation Assembly. It generates 8 sidebar panel types for the frontend.

**Language**: Python (FastAPI)  
**Port**: 52005  

**Current State**: ⚠️ Mostly Implemented  
**Critique**: Belief evolution and reasoning path endpoints return "not yet implemented." The concept is excellent — regulators want explainability. This service makes the system auditable.

---

### Repository 15: `knowledge-graph` — The Library

**The Story**: Memory is episodic. Knowledge is structural. The Knowledge Graph is an in-memory semantic graph (with JSONL persistence) that stores relationships between trading concepts — how FVGs relate to BOS, how timeframes nest, how symbols correlate. It validates everything against the Ontology before storing.

**Language**: Python (FastAPI)  
**Port**: 52015  

**Current State**: ✅ Fully Implemented  
**Critique**: Clean implementation. JSONL persistence is pragmatic for now but won't scale to millions of nodes. Plan for Neo4j integration eventually.

---

### Repository 16: `ontology` — The Vocabulary

**The Story**: Before you can know anything, you need to define what things *are*. Ontology defines 14 core trading concepts (Market, Candle, Tick, FVG, BOS, CHOCH, Order Block, etc.) with PostgreSQL-backed schema evolution and 45+ endpoints. It's the shared vocabulary that prevents services from disagreeing about what a "candlestick" means.

**Language**: Python (FastAPI)  
**Port**: 52100  

**Current State**: ✅ Fully Implemented  
**Critique**: Well-executed. The domain-specific ontology is what makes this system more than "just another trading bot." Scaling to new domains (weather, defense) will mean adding new ontology modules.

---

### Repository 17: `memory` — The Diary

**The Story**: Every experience is worth recording. Memory stores events in 4 layers: working memory (active context), episodic memory (specific events), semantic memory (general knowledge), and procedural memory (how-to patterns). Append-only, SHA-256 hashed, RBAC-filtered, with as-of temporal queries.

**Language**: Python (FastAPI)  
**Port**: 52018  

**Current State**: ✅ Fully Implemented  
**Critique**: Solid implementation. The 4-layer architecture mirrors cognitive science research accurately.

---

### Repository 18: `language-intelligence` — The Translator

**The Story**: Machines that can't speak human are useless to humans. Language Intelligence is the NL interface — it parses natural language queries, detects intent, orchestrates cross-service searches, and adapts its response for 4 audiences: trader, engineer, auditor, operator. Zero-hallucination enforcement.

**Language**: Python (FastAPI)  
**Port**: 52006  

**Current State**: ✅ Fully Implemented  
**Critique**: The zero-hallucination enforcement is the right policy for a financial system. The 4-audience adaptation is clever.

---

### Repository 19: `gateway` — The Gatekeeper

**The Story**: One entry point. One API surface. The Gateway is a centralized reverse proxy that verifies JWT tokens via the auth system, handles CORS, and routes requests to 17+ downstream services; a single frontend entry point.

**Language**: Go (production) / Python (development)  
**Port**: 52031  

**Current State**: ✅ Fully Implemented  
**Critique**: Same dual-language issue as event-bus. Standardize on Go for production.

---

### Repository 20: `security` — The Vault

**The Story**: A hedge fund that gets hacked is dead. Security provides military-grade protection: crypto-as-a-service, secrets management, ABAC (Attribute-Based Access Control), immutable audit logging, API key management, file quarantine, and WAF (Web Application Firewall).

**Language**: Node.js (Fastify 4 + PostgreSQL)  
**Port**: 55000  

**Current State**: ✅ Extensively Implemented  
**Critique**: Ambitious scope. The crypto-as-a-service layer is a differentiator. Ensure the secrets management is actually used by other services (not just available).

---

### Repository 21: `Back_End_Auth_System` — The Bouncer

**The Story**: Who are you? Prove it. The Auth System handles JWT authentication with refresh rotation, 2FA (TOTP), Google OAuth 2.0, password reset via Resend email, session management (Redis), RBAC, account locking. Paystack integration for payments.

**Language**: Node.js (Express 5 + MongoDB)  
**Port**: 5000/5500  

**Current State**: ✅ Production-Grade  
**Critique**: The most mature backend service. But it only supports a **one-time KES 20,000 application fee** — not recurring deposits/withdrawals. For a hedge fund, you need a full financial operations layer.

---

### Repository 22: `topology-hub` — The Map

**The Story**: 26 services need a map. Topology Hub is the authoritative service graph — it tracks which services exist, their health, their connections, their polygon geometry for visual representation, and broadcasts topology changes via WebSocket.

**Language**: Go  
**Port**: 8080  

**Current State**: ✅ Fully Implemented  

---

### Repository 23: `topology-hub-express` — The Bridge

**The Story**: The Go topology-hub speaks HTTP/WebSocket. The browser speaks Socket.io. This bridge translates between them — zero independent state, pure protocol translation.

**Language**: Node.js (Express + Socket.io)  
**Port**: 3000  

**Current State**: ✅ Fully Implemented  

---

### Repository 24: `shared` — The Common Language

**The Story**: 15 Python services need shared constants, contracts, models, and utilities. This installable package (`pip install -e ./shared`) provides cognitive state definitions, timeframe constants, event schemas, Vector256D, logging, validators.

**Language**: Python (library)  

**Current State**: ✅ Fully Implemented  

---

### Repository 25: `frontend` — The Command Center

**The Story**: The operator dashboard. 20+ pages including topology visualization (2D/3D), candlestick charting, market intelligence panels, signal management, engine control panels, auth flows, and deep-link modules for every service. Built with React 18, D3.js, Three.js, MUI, and Socket.io.

**Language**: React 18 + TypeScript (Vite)  
**Port**: 80 (prod) / 3000 (dev)  

**Current State**: ✅ Fully Implemented  
**Critique**: Rich dashboard but it's an *operator* console, not a *client* portal. You'll need a separate client-facing frontend for investor deposits/withdrawals/portfolio viewing.

---

### Repository 26: `Landing_Page` — The Storefront

**The Story**: The public face. Hedge-fund-style branding with live telemetry, 8 domain showcase (financial, healthcare, traffic, cybersecurity, defense, agriculture, robotics, weather), visitor counter, market snapshot, B2G/B2B/B2C.

**Language**: React + TypeScript (Vite, Tailwind, shadcn-ui)  
**Port**: 8091  

**Current State**: ✅ Fully Implemented  
**Critique**: Beautiful and ambitious. Some vestiges of a previous logistics product remain (parcel/shipment references in env vars — clean those up). The 8-domain vision is powerful but only finance has any backend implementation.

---

### Bonus: `lightweight-charts` — The Borrowed Tool

**This is NOT an AUREXIS service.** It's the TradingView Lightweight Charts™ library vendored into the repo. Apache 2.0 licensed. Should be an npm dependency, not committed source.

---

## 5. Cognitive Pipeline Flowcharts

### 5.1 End-to-End: From Raw Tick to Trade Decision

```mermaid
sequenceDiagram
    participant Market as Market (Deriv API)
    participant PO as Price Observer
    participant EB as Event Bus
    participant PER as Perception
    participant SE as Shape Engine
    participant ME as Meaning Engine
    participant RE as Reasoning Engine
    participant CB as Core Brain
    participant PE as Policy Engine
    participant SIM as Simulation
    participant EE as Explanation Engine
    participant LE as Learning Engine
    participant MEM as Memory

    Market->>PO: Raw tick stream
    PO->>EB: tick_normalized event
    EB->>PER: Route to perception
    PER->>PER: Detect 37 primitives
    PER->>EB: perception_completed (256D vector)
    EB->>SE: Route to shape engine
    SE->>SE: Match 90+ patterns
    SE->>EB: shape_detected (FVG/BOS/CHOCH)
    EB->>ME: Route to meaning engine
    ME->>ME: Update BeliefGraph
    ME->>ME: 12-TF confluence check
    ME->>EB: belief_updated event
    EB->>RE: Route to reasoning
    RE->>RE: Forward chain + causal DAG
    RE->>EB: reasoning_completed event
    EB->>CB: All signals arrive
    CB->>CB: 10-step decision pipeline
    CB->>PE: Policy check
    PE-->>CB: ALLOW/DENY/CONDITIONAL
    CB->>SIM: Simulate 5 cones
    SIM-->>CB: Punishment score + risk metrics
    CB->>CB: Final decision
    CB->>EE: Explain decision
    EE-->>CB: Human-readable explanation
    CB->>MEM: Store episode
    CB->>LE: Learning feedback
    LE->>PER: Update thresholds
    LE->>SE: Update confidence
    LE->>ME: Update beliefs
```

### 5.2 Punishment-Learning Feedback Loop

```mermaid
flowchart TD
    A[Trade Outcome<br/>Win or Loss] --> B[Simulation Scores it]
    B --> C[3-Level Punishment]
    C --> D1["Path Error (50%)<br/>Did we read the trend wrong?"]
    C --> D2["Structure Error (35%)<br/>Did we enter invalidated structure?"]
    C --> D3["Calibration Error (15%)<br/>Was sizing/SL wrong?"]

    D1 --> E[Net Score Calculated]
    D2 --> E
    D3 --> E

    E --> F[Learning Engine Receives]
    F --> G{Which modality?}

    G -->|Labeled outcome| H[Supervised Learning]
    G -->|Reward signal| I[Reinforcement Learning]
    G -->|Penalty signal| J[Punishment Learning]
    G -->|High uncertainty| K[Active Learning]
    G -->|Pattern in learning| L[Meta-Learning]

    H --> M[Model Update]
    I --> M
    J --> M
    K --> M
    L --> M

    M --> N[Feedback Propagation]
    N --> O1[Perception:<br/>Adjust detection thresholds]
    N --> O2[Shape Engine:<br/>Adjust confidence weights]
    N --> O3[Meaning Engine:<br/>Adjust belief decay rates]
    N --> O4[Policy Engine:<br/>Adjust risk limits]

    O1 --> P[Next Trade is Smarter]
    O2 --> P
    O3 --> P
    O4 --> P
```

### 5.3 Data Flow: File Upload to Candle Display

```mermaid
flowchart LR
    A[User Uploads CSV] --> B[Market Ingestion]
    B --> C[Parse & Normalize]
    C --> D[(ClickHouse)]
    D --> E[Candle Constructor]
    E --> F1[REST: /api/candles?symbol=V25&tf=1h]
    E --> F2[SSE: /api/stream/replay]
    E --> F3[WebSocket: /ws/live]
    F1 --> G[Frontend: Lightweight Charts]
    F2 --> G
    F3 --> G
```

---

## 6. The Hedge Fund — End-to-End Financial Flow

### 6.1 What You Need (and What's Missing)

For a fully operational hedge fund, here's the complete flow and what exists vs. what doesn't:

```mermaid
flowchart TD
    subgraph "CLIENT LAYER (Mostly Missing)"
        A1[Client Signs Up<br/>✅ Auth System]
        A2[KYC Verification<br/>❌ NOT BUILT]
        A3[Deposit Funds<br/>❌ NEEDS PAYMENT SERVICE]
        A4[View Portfolio<br/>❌ NO CLIENT PORTAL]
        A5[Request Withdrawal<br/>❌ NOT BUILT]
    end

    subgraph "FUND OPERATIONS (Missing)"
        B1[Pool Management<br/>❌ NOT BUILT]
        B2[Position Tracking<br/>❌ NOT BUILT]
        B3[P&L Accounting<br/>❌ NOT BUILT]
        B4[Compliance Reports<br/>❌ NOT BUILT]
    end

    subgraph "TRADING ENGINE (Partially Built)"
        C1[Market Data Feed<br/>⚠️ File only, no live]
        C2[Cognitive Pipeline<br/>✅ BUILT]
        C3[Decision Making<br/>✅ Core Brain]
        C4[Risk Management<br/>⚠️ Policy Engine - stubs]
        C5[Order Execution<br/>❌ NOT BUILT]
    end

    subgraph "BROKER LAYER (Not Built)"
        D1[Deriv API<br/>❌ NO INTEGRATION]
        D2[Order Placement<br/>❌ NOT BUILT]
        D3[Position Management<br/>❌ NOT BUILT]
        D4[Settlement<br/>❌ NOT BUILT]
    end

    A1 --> A2
    A2 --> A3
    A3 --> B1
    B1 --> C1
    C1 --> C2
    C2 --> C3
    C3 --> C4
    C4 --> C5
    C5 --> D1
    D1 --> D2
    D2 --> D3
    D3 --> D4
    D4 --> B2
    B2 --> B3
    B3 --> A4
    A4 --> A5
    A5 --> B1
```

### 6.2 New Services You Need

To make this a real hedge fund, you need **4-5 new services**:

| # | Service Name | Purpose | Priority |
|---|-------------|---------|----------|
| 1 | **trade-executor** | Connects to Deriv API (and future brokers). Places orders, manages positions, handles fills/rejects. The hands of the system. | 🔴 CRITICAL |
| 2 | **fund-manager** | Pool management, investor deposits/withdrawals, profit allocation, NAV calculation, payout scheduling. The financial backbone. | 🔴 CRITICAL |
| 3 | **kyc-verifier** | ID document upload + verification, facial recognition capture + hashing, liveness detection, one-person-one-account enforcement. The compliance gate. | 🟡 HIGH |
| 4 | **client-portal** | Investor-facing frontend (separate from operator dashboard). Deposit, view portfolio, request withdrawal, see performance. | 🟡 HIGH |
| 5 | **notification-hub** | Multi-channel notifications: email (Resend), SMS, push. Trade alerts, payout confirmations, KYC status updates. | 🟢 MEDIUM |

### 6.3 The Deposit → Trade → Payout Flow (Proposed)

```mermaid
sequenceDiagram
    participant Client
    participant Auth as Auth System
    participant KYC as KYC Verifier
    participant Fund as Fund Manager
    participant Pay as Payment (M-Pesa/Paystack)
    participant Brain as Core Brain
    participant Exec as Trade Executor
    participant Deriv as Deriv API
    participant Notif as Notification Hub

    Client->>Auth: Sign up (email + password + 2FA)
    Auth-->>Client: Account created
    Client->>KYC: Upload ID + selfie
    KYC->>KYC: Verify ID, hash face, check uniqueness
    KYC-->>Client: KYC approved
    Client->>Fund: Deposit KES 1,000 (minimum)
    Fund->>Pay: Initialize M-Pesa STK push
    Pay-->>Fund: Payment confirmed
    Fund->>Fund: Add to liquidity pool
    Fund->>Notif: Send deposit confirmation
    Notif-->>Client: Email + SMS confirmation

    Note over Brain,Deriv: Trading happens continuously
    Brain->>Brain: Cognitive pipeline produces decision
    Brain->>Exec: Trade signal (BUY V25 1s @ 1234.56)
    Exec->>Deriv: Place order via API
    Deriv-->>Exec: Order filled
    Exec->>Fund: Update P&L
    Fund->>Fund: Calculate investor shares

    Note over Client,Fund: After minimum holding period (e.g., 7 days)
    Client->>Fund: Request withdrawal
    Fund->>Fund: Check: holding period met? Funds available?
    Fund->>Pay: Initiate payout
    Pay-->>Client: KES sent to M-Pesa
    Fund->>Notif: Payout confirmation
    Notif-->>Client: Email + SMS confirmation
```

### 6.4 One-Person-One-Account Enforcement

```mermaid
flowchart TD
    A[New User Signs Up] --> B[Collect: Email + Phone + ID Number]
    B --> C{ID Number Already Used?}
    C -->|Yes| D[REJECT: Account exists for this ID]
    C -->|No| E[Upload: National ID Photo]
    E --> F[Upload: Live Selfie]
    F --> G[Extract Face from ID Photo]
    G --> H[Compare Selfie vs ID Face]
    H --> I{Match > 95%?}
    I -->|No| J[REJECT: Face mismatch]
    I -->|Yes| K[Hash Face Embedding]
    K --> L{Hash vs All Stored Hashes}
    L -->|Match Found| M[REJECT: Face already registered]
    L -->|Unique| N[✅ KYC APPROVED]
    N --> O[Store: ID hash + face hash + timestamp]
```

---

## 7. Multi-Domain Vision — Beyond Forex

### 7.1 How the Architecture Enables Multi-Domain

The genius of this architecture is domain-agnosticism. Here's how:

| Component | Financial Domain | Weather Domain | Cybersecurity Domain |
|-----------|-----------------|---------------|---------------------|
| **price-observer** | OHLCV ticks | Temperature/pressure readings | Network traffic packets |
| **perception** | Candlestick primitives | Weather pattern primitives | Threat signal primitives |
| **shape-engine** | FVG, BOS, CHOCH | Storm fronts, pressure systems | Attack patterns, kill chains |
| **meaning-engine** | Market beliefs | Climate beliefs | Threat beliefs |
| **reasoning-engine** | Trade logic | Weather prediction logic | Threat assessment logic |
| **ontology** | Trading concepts | Meteorological concepts | Security concepts |
| **core-brain** | Trade decision | Weather alert decision | Threat response decision |

### 7.2 Domain Activation Flow

```mermaid
flowchart TD
    A[Landing Page<br/>8 Domains Listed] --> B{Client Selects Domain}

    B --> C1[Financial Intelligence]
    B --> C2[Healthcare Intelligence]
    B --> C3[Cybersecurity Intelligence]
    B --> C4[Defense Intelligence]
    B --> C5[Agriculture Intelligence]
    B --> C6[Weather Intelligence]
    B --> C7[Traffic Intelligence]
    B --> C8[Robotics Intelligence]

    C1 --> D1[Active: Full Pipeline<br/>Forex via Deriv API]
    C2 --> D2[Future: Needs domain ontology<br/>+ medical data feeds]
    C3 --> D3[Future: Needs threat feeds<br/>+ SIEM integration]
    C4 --> D4[Future: Needs satellite/radar<br/>+ OSINT feeds]
    C5 --> D5[Future: Needs IoT sensor<br/>+ weather data feeds]
    C6 --> D6[Future: Needs NOAA/ECMWF<br/>+ station data feeds]
    C7 --> D7[Future: Needs traffic sensors<br/>+ GPS/transit feeds]
    C8 --> D8[Future: Needs ROS/sensor<br/>+ telemetry feeds]

    style D1 fill:#2d5a2d,color:#fff
    style D2 fill:#5a3a2d,color:#fff
    style D3 fill:#5a3a2d,color:#fff
    style D4 fill:#5a3a2d,color:#fff
    style D5 fill:#5a3a2d,color:#fff
    style D6 fill:#5a3a2d,color:#fff
    style D7 fill:#5a3a2d,color:#fff
    style D8 fill:#5a3a2d,color:#fff
```

### 7.3 Each Domain Has Its Own Customers

| Domain | B2C Customers | B2B Customers | B2G Customers |
|--------|---------------|---------------|---------------|
| **Financial** | Retail investors, day traders | Hedge funds, prop firms | Central banks, regulators |
| **Healthcare** | Patients (telemedicine) | Hospitals, insurers | Public health agencies |
| **Cybersecurity** | — | Enterprises, MSSPs | Defense ministries, CERTs |
| **Defense** | — | Defense contractors | Militaries, intelligence agencies |
| **Agriculture** | Smallholder farmers | Agribusinesses, commodities traders | Agriculture ministries |
| **Weather** | General public | Airlines, shipping, energy | Meteorological agencies |
| **Traffic** | Commuters | Logistics companies | City governments, transit authorities |
| **Robotics** | Hobbyists, makers | Manufacturers, warehouses | Military, space agencies |

---

## 8. Landing Page — The Storefront

The Landing Page at port 8091 currently advertises all 8 domains with:
- Live telemetry probes per domain
- Hedge-fund-style dark theme
- Market snapshot widget
- Visitor counter
- FAQs referencing all domains
- Individual domain pages (`/healthcare`, `/cybersecurity`, etc.)

### What Needs to Change

1. **Remove logistics vestiges** — env vars reference parcel/shipment URLs from a previous product
2. **Each domain page should link to its own sign-up/subscription flow**
3. **Financial domain should lead to the client portal** (once built)
4. **Other domains should show "Coming Soon" with email waitlist** (use Resend)

---

## 9. Repository Cleanup — What Must Change

### 9.1 Files That Must Move or Die

| File/Folder | Current Location | Action | Destination |
|-------------|-----------------|--------|-------------|
| `_collect_stats.py` | Root | **Move** | `scripts/` |
| `_collect_stats.sh` | Root | **Move** | `scripts/` |
| `_endpoints_deep.py` | Root | **Move** | `scripts/` |
| `_ports_check.py` | Root | **Move** | `scripts/` |
| `_ports_deep.py` | Root | **Move** | `scripts/` |
| `_scan_codebase.py` | Root | **Move** | `scripts/` |
| `generate_aurexis_doc_v1.py` | Root | **Move** | `scripts/doc-generators/` |
| `update_doc.py` | Root | **Move** | `scripts/doc-generators/` |
| `update_doc_v2_backup.py` | Root | **DELETE** | — (superseded by `update_doc.py`) |
| `script.txt` | Root | **DELETE** | — (duplicate of above with wrong extension) |
| `docker-compose.yml.bak` | Root | **DELETE** | — (git handles backups) |
| `scripts_root_tmp/` | Root | **DELETE** | — (contains 1 file duplicated in `scripts/`) |
| `config/prometheus/` | Root | **Move** | `infrastructure/prometheus/` |
| `lightweight-charts/` | Root | **DELETE** | — (use as npm dependency instead) |
| `AUREXIS_Architecture_Document.docx` | Root | **Move** | `docs/` |
| `.~lock.AUREXIS_Architecture_Document.docx#` | Root | **DELETE** | — (lock file from LibreOffice) |

### 9.2 What the Root Should Look Like After Cleanup

```
AUREXIS/
├── docker-compose.yml          # Orchestration
├── Makefile                    # Build/test/deploy commands
├── push_all.sh                 # Multi-repo git operations
├── start_and_observe.sh        # System launcher
├── .github/                    # CI/CD workflows
├── .gitignore
├── docs/                       # Architecture docs, PDFs, this document
├── infrastructure/             # Prometheus, Postgres init
├── scripts/                    # All utility/analysis scripts
├── tests/                      # Cross-service integration/load tests
│
├── Back_End_Auth_System/       # 🔐 Auth + Payments
├── candle-constructor/         # 📊 Candle serving
├── core-brain/                 # 🧠 Central orchestrator
├── event-bus/                  # ⚡ Message backbone
├── explanation-engine/         # 📝 Decision explainer
├── frontend/                   # 🖥️ Operator dashboard
├── gateway/                    # 🚪 API gateway
├── knowledge-graph/            # 📚 Semantic graph
├── Landing_Page/               # 🌐 Public website
├── language-intelligence/      # 🗣️ NL interface
├── learning-engine/            # 🎓 Adaptive learning
├── market-ingestion/           # 📥 Data ingestion
├── meaning-engine/             # 💡 Belief system
├── memory/                     # 🧬 Event store
├── ontology/                   # 📖 Concept schema
├── perception/                 # 👁️ Sensory processing
├── policy-engine/              # ⚖️ Risk governance
├── price-observer/             # 👀 Tick processing (Rust)
├── reasoning-engine/           # 🔬 Formal logic
├── schema-registry/            # 📋 Event schemas
├── security/                   # 🔒 Security control plane
├── shape-engine/               # 🔷 Pattern recognition
├── shared/                     # 📦 Shared Python library
├── simulation/                 # 🎯 Dream engine
├── topology-hub/               # 🗺️ Service graph (Go)
└── topology-hub-express/       # 🌉 Socket.io bridge
```

### 9.3 Each Repository Must Be Self-Contained

Every repo should have:
```
service-name/
├── Dockerfile
├── README.md                   # What it does, how to run, API docs
├── requirements.txt / go.mod / package.json
├── main.py / main.go / index.ts
├── src/                        # All source code
├── tests/                      # Unit + integration tests
├── config/                     # Service-specific config
├── docs/                       # Service-specific documentation
├── k8s/                        # Kubernetes manifests
└── helm/                       # Helm charts
```

---

## 10. Missing Services — What You Don't Have Yet

### CRITICAL (Cannot Operate Without)

#### 1. `trade-executor` — The Hands

```
Purpose: Connect to Deriv API (and future brokers), place orders, manage positions
Language: Python (FastAPI) — to match most services
Port: 52050
Key Features:
  - Deriv WebSocket API integration (deriv-api Python package)
  - Order types: market, limit, stop-loss, take-profit
  - Position lifecycle: open → modify → close
  - Multi-account support
  - Rate limiting and retry logic
  - Paper trading mode (simulate without real orders)
  - Event emissions: order_placed, order_filled, order_rejected, position_closed
```

#### 2. `fund-manager` — The Treasurer

```
Purpose: Manage the investment pool, track deposits/withdrawals, calculate NAV
Language: Python (FastAPI)
Port: 52055
Key Features:
  - M-Pesa STK push integration (Daraja API) for Kenyan users
  - Paystack for card payments
  - Deposit flow: verify payment → add to pool → allocate shares
  - Withdrawal flow: request → hold period check (7 days min) → approve → pay out
  - Minimum deposit: KES 1,000
  - NAV (Net Asset Value) calculation per investor
  - Profit/loss allocation proportional to share
  - Pool balance tracking
  - Regulatory reporting
```

### HIGH PRIORITY

#### 3. `kyc-verifier` — The ID Checker

```
Purpose: Verify identity, prevent duplicate accounts
Language: Python (FastAPI)
Port: 52060
Key Features:
  - National ID photo upload + OCR
  - Live selfie capture
  - Face comparison (ID photo vs selfie) — use DeepFace or similar
  - Face embedding hashing for uniqueness check
  - One-person-one-account enforcement
  - ID number deduplication
  - Hashed storage (never store raw biometric data)
  - GDPR/DPA compliance
```

#### 4. `client-portal` — The Investor Dashboard

```
Purpose: Client-facing frontend (separate from operator dashboard)
Language: React + TypeScript
Port: 8092
Key Features:
  - Sign up / log in / KYC flow
  - Deposit money (M-Pesa / card)
  - View portfolio: invested amount, current value, returns
  - Performance charts (daily/weekly/monthly)
  - Withdrawal request
  - Transaction history
  - Notification preferences
  - Mobile-responsive
```

### MEDIUM PRIORITY

#### 5. `notification-hub` — The Messenger

```
Purpose: Multi-channel notifications
Language: Python (FastAPI) or Node.js
Port: 52065
Key Features:
  - Email via Resend (you have the key)
  - SMS via Africa's Talking or Twilio
  - Push notifications
  - Template management
  - Delivery tracking
  - Preference management (per user, per channel)
```

---

## 11. Honest Critique — What's Good, What's Broken, What's Fantasy

### 🟢 What's Genuinely Good

1. **The cognitive pipeline is architecturally sound.** Perception → Shape → Meaning → Reasoning → Decision → Explanation → Learning is a legitimate cognitive science model implemented as microservices. This is not trivial.

2. **The punishment/learning loop is real quant finance.** VaR, CVaR, Sharpe ratio, 3-level structural punishment, 5 learning modalities with autonomy levels — this is beyond hobby-project quality.

3. **Polyglot architecture makes sense.** Rust for tick processing (speed), Go for infrastructure (concurrency), Python for ML/cognitive (ecosystem), Node.js for real-time (Socket.io). Each language serves its strength.

4. **The learning-engine is the crown jewel.** 52 endpoints, isotonic calibration, version rollback, safety gates, feedback propagation to upstream services. This is where the competitive moat is.

5. **The ontology-first approach is rare and correct.** Most trading systems hardcode assumptions. Yours defines concepts formally and validates against them. This is what enables multi-domain expansion.

6. **The landing page vision is compelling.** 8 intelligence domains from a single cognitive infrastructure — this is a venture-scale pitch.

7. **Auth system is production-ready.** 2FA, OAuth, JWT rotation, account locking, Paystack, Resend — this can handle real users.

### 🟡 What Needs Finishing

1. **market-ingestion live connectors are ALL stubbed.** You have 12 CSV files but zero real-time data feeds. For a hedge fund, this is like having a race car with no engine.

2. **perception has 9 dead primitives** and never loads its config YAML. Finish the detection pipeline.

3. **meaning-engine codes Neo4j but uses in-memory.** Either drop Neo4j or wire it.

4. **reasoning-engine's sophisticated modes fall back to simple forward chaining.** The resolution and natural deduction are decorative.

5. **core-brain's MetaLearner is never called.** The CommandInterpreter is keyword-only. The CrossDomainReasoner is a placeholder.

6. **policy-engine's safety gates are all `return True`.** The harm detector, ethical validator, and human approval gate are **critical safety bypasses** in a system that wants to handle real money.

7. **simulation's `_transform_timeframe()` returns empty list.** This breaks multi-TF simulation.

8. **shape-engine silently returns `{}` on 12 integration failures.** Silent failures in trading = hidden losses.

9. **candle-constructor has SQL injection via f-strings.** Fix immediately.

10. **explanation-engine's belief evolution endpoints are "not yet implemented."**

### 🔴 What's Fantasy Right Now (But Shouldn't Stay That Way)

1. **"Hedge fund" without broker connectivity.** You can't trade without a broker API. Not a single Deriv, MT5, or any broker integration exists.

2. **"Hedge fund" without order execution.** Core Brain makes decisions but nobody places trades.

3. **"Hedge fund" without fund management.** You have a KES 20,000 one-time fee, not a deposit/withdrawal/pool system.

4. **"8 intelligence domains" with only financial backend.** The landing page promises weather, defense, healthcare, etc. Zero backend work exists for any non-financial domain.

5. **"KYC verification" doesn't exist.** No ID upload. No facial recognition. No uniqueness check. For regulated financial services, this is a legal requirement.

6. **"Professional email tracking"** — Resend is configured but only used for password reset. Not for trade notifications, deposit confirmations, or marketing.

### ⚫ Hard Truths

1. **You have an impressive architecture but an incomplete product.** The chassis is built and beautiful. The engine is partly assembled. But the car doesn't drive yet.

2. **The gap between your landing page promises and your backend reality is dangerous.** If you launch the landing page as-is, you're advertising services you cannot deliver. Fix the landing page to say "Coming Soon" on non-financial domains, or build them.

3. **You're one developer managing 26 repos in 5 languages.** This is heroic but unsustainable. Prioritize ruthlessly. The financial domain alone is a 2-3 year full product.

4. **The dual Go/Python implementations (event-bus, gateway) create double maintenance.** Pick one per service and delete the other.

5. **Some services are over-engineered for MVP.** The shape-engine's 13-state lifecycle machine is sophisticated but you might ship faster with 5 states. The ontology's 45+ endpoints are complete but does anyone call all 45 yet?

---

## 12. The Resend Email Integration

### Current Configuration

| Setting | Value |
|---------|-------|
| **API Key** | `re_fnu8naZF_P2QvRrWnue4MWKFoaqtV4WWC` |
| **Domain** | `aorexis.com` |
| **Test Email** | `muriumwangi214@gmail.com` |
| **Current Usage** | Password reset only (Back_End_Auth_System) |
| **From Address** | Configurable via `FROM_EMAIL` env var |

### What Should Use Resend

| Use Case | Trigger | Template |
|----------|---------|----------|
| Welcome email | User signs up | Branded welcome + KYC instructions |
| KYC approved | KYC verification passes | Congratulations + deposit instructions |
| Deposit confirmed | Payment webhook fires | Amount + pool share + estimated returns |
| Trade executed | trade-executor places order | Symbol, direction, size, entry price |
| Trade closed | Position closed | P&L, reason, explanation link |
| Weekly report | Cron (every Monday) | Portfolio value, returns, top trades |
| Payout sent | Withdrawal processed | Amount sent, M-Pesa ref, remaining balance |
| Security alert | Suspicious login | IP, location, device — "Was this you?" |
| Domain waitlist | Non-financial domain interest | "Thanks for your interest in [Weather Intelligence]" |

### Required Setup on aorexis.com

1. DNS records for Resend domain verification (MX, TXT, DKIM)
2. SPF record to authorize Resend to send from `@aorexis.com`
3. DMARC record for email authentication
4. Configure `FROM_EMAIL=noreply@aorexis.com` in Back_End_Auth_System

---

## 13. Identity & Anti-Fraud System

### Proposed Architecture

```mermaid
flowchart TD
    A[User Registration] --> B[Collect Basic Info<br/>Name, Email, Phone, ID Number]
    B --> C{ID Number Check}
    C -->|Exists in DB| D[❌ REJECTED<br/>Account already exists]
    C -->|Unique| E[Upload National ID Photo]
    E --> F[OCR Extract:<br/>Name, ID Number, DOB]
    F --> G{OCR ID# = Entered ID#?}
    G -->|Mismatch| H[❌ REJECTED<br/>ID number doesn't match document]
    G -->|Match| I[Capture Live Selfie]
    I --> J[Liveness Detection<br/>Blink / Turn Head]
    J --> K{Human?}
    K -->|Fail| L[❌ REJECTED<br/>Liveness check failed]
    K -->|Pass| M[Extract Face Embedding<br/>from Selfie]
    M --> N[Extract Face Embedding<br/>from ID Photo]
    N --> O{Cosine Similarity > 0.95?}
    O -->|No| P[❌ REJECTED<br/>Face doesn't match ID photo]
    O -->|Yes| Q[Hash Face Embedding<br/>SHA-256 + Salt]
    Q --> R{Compare Hash vs<br/>All Stored Hashes}
    R -->|Collision Found| S[❌ REJECTED<br/>Face already registered<br/>under different account]
    R -->|Unique| T[✅ KYC APPROVED]
    T --> U[Store:<br/>• Hashed ID number<br/>• Hashed face embedding<br/>• Verification timestamp<br/>• IP address + device fingerprint]
```

### Technology Choices

| Component | Recommended Tool | Why |
|-----------|-----------------|-----|
| **Face Detection** | MediaPipe / MTCNN | Lightweight, runs on CPU |
| **Face Embedding** | DeepFace (with ArcFace backend) | State-of-the-art accuracy, MIT licensed |
| **Liveness Detection** | Silent Face Anti-Spoofing | Detects photo/video attacks |
| **OCR** | Tesseract / PaddleOCR | Free, handles Kenyan IDs |
| **Storage** | PostgreSQL (hashed data only) | Never store raw biometrics |

---

## 14. Recommended Next Steps

### Phase 1: Make It Work (Weeks 1-4)

| # | Task | Priority | Effort |
|---|------|----------|--------|
| 1 | **Wire Deriv API into market-ingestion** | 🔴 CRITICAL | 1 week |
| 2 | **Build trade-executor service** | 🔴 CRITICAL | 1 week |
| 3 | **Fix SQL injection in candle-constructor** | 🔴 CRITICAL | 1 day |
| 4 | **Fix policy-engine safety stubs** | 🔴 CRITICAL | 2 days |
| 5 | **Complete simulation's `_transform_timeframe()`** | 🟡 HIGH | 1 day |
| 6 | **Fix shape-engine silent failures** | 🟡 HIGH | 1 day |
| 7 | **Clean up root directory** (per Section 9) | 🟡 HIGH | 1 hour |
| 8 | **Wire core-brain's MetaLearner** | 🟡 HIGH | 2 days |

### Phase 2: Make It Real (Weeks 5-8)

| # | Task | Priority | Effort |
|---|------|----------|--------|
| 9 | **Build fund-manager service** | 🔴 CRITICAL | 2 weeks |
| 10 | **Build kyc-verifier service** | 🟡 HIGH | 1 week |
| 11 | **Build client-portal frontend** | 🟡 HIGH | 2 weeks |
| 12 | **Configure Resend email templates** | 🟡 HIGH | 2 days |
| 13 | **Wire simulation to event-bus** (event-driven) | 🟡 HIGH | 3 days |
| 14 | **Complete perception's 9 dead primitives** | 🟢 MEDIUM | 3 days |

### Phase 3: Make It Scale (Weeks 9-12)

| # | Task | Priority | Effort |
|---|------|----------|--------|
| 15 | **Build notification-hub service** | 🟢 MEDIUM | 1 week |
| 16 | **Wire Neo4j into meaning-engine** | 🟢 MEDIUM | 3 days |
| 17 | **Deprecate Python event-bus/gateway** (Go only) | 🟢 MEDIUM | 2 days |
| 18 | **Remove lightweight-charts** (npm dependency) | 🟢 MEDIUM | 1 day |
| 19 | **Kubernetes deployment** | 🟢 MEDIUM | 2 weeks |
| 20 | **Load testing with real data** | 🟢 MEDIUM | 1 week |

### Phase 4: Multi-Domain (Months 4+)

| # | Task | Domain |
|---|------|--------|
| 21 | Define weather ontology module | Weather |
| 22 | Define cybersecurity ontology module | Cybersecurity |
| 23 | Build weather perception adapter | Weather |
| 24 | Build threat perception adapter | Cybersecurity |
| 25 | Build domain-specific landing page flows | All |

---

## Appendix A: Organization Repository Map (GitHub — AUREXIS-A)

| # | Repository | Status | Language | Role |
|---|-----------|--------|----------|------|
| 1 | `Landing_Page` | ✅ Active | TypeScript | Public website |
| 2 | `gateway` | ✅ Active | Go | API gateway |
| 3 | `frontend` | ✅ Active | TypeScript | Operator dashboard |
| 4 | `candle-constructor` | ⚠️ Needs fixes | Python | Candle serving |
| 5 | `shape-engine` | ⚠️ Needs fixes | Python | Pattern recognition |
| 6 | `perception-` | ⚠️ Needs finishing | Python | Sensory processing |
| 7 | `meaning-engine` | ⚠️ Needs finishing | Python | Belief system |
| 8 | `market-ingestion` | ⚠️ Live feeds missing | Python | Data ingestion |
| 9 | `event-bus` | ✅ Active | Go | Message backbone |
| 10 | `core-brain-` | ⚠️ Needs finishing | Python | Central orchestrator |
| 11 | `shared` | ✅ Active | Python | Shared library |
| 12 | `topology-hub-express` | ✅ Active | JavaScript | Socket.io bridge |
| 13 | `topology-hub` | ✅ Active | Go | Service graph |
| 14 | `simulation` | ⚠️ Needs fixes | Python | Dream engine |
| 15 | `Security` | ✅ Active | JavaScript | Security control plane |
| 16 | `schema-registry` | ✅ Active | Go | Event schemas |
| 17 | `reasoning-engine` | ⚠️ Needs finishing | Python | Formal logic |
| 18 | `price-observer` | ✅ Active | Rust | Tick processing |
| 19 | `policy-engine` | ⚠️ Safety stubs | Python | Risk governance |
| 20 | `ontology-` | ✅ Active | Python | Concept schema |
| 21 | `memory` | ✅ Active | Python | Event store |
| 22 | `learning-engine` | ✅ Active | Python | Adaptive learning |
| 23 | `language-intelligence` | ✅ Active | Python | NL interface |
| 24 | `knowledge-graph` | ✅ Active | Python | Semantic graph |
| 25 | `explanation-engine` | ⚠️ Needs finishing | Python | Decision explainer |
| 26 | `Back_End_Auth_System` | ✅ Active | JavaScript | Auth + payments |

**NOT a repository (remove from workspace or convert to npm dependency):**
- `lightweight-charts` — vendored TradingView library

---

## Appendix B: Infrastructure Containers

| Container | Image | Port | Purpose |
|-----------|-------|------|---------|
| PostgreSQL | postgres:15 | 5432 | Ontology, security, shape-engine |
| Redis | redis:7 | 6379 | Auth sessions, caching |
| MongoDB | mongo:6 | 27017 | Auth user data |
| ClickHouse | clickhouse/clickhouse-server:23.12 | 8123/9000 | Time-series market data |
| Prometheus | prom/prometheus | 9090 | Metrics collection |
| Jaeger | jaegertracing/all-in-one | 16686 | Distributed tracing |

---

## Appendix C: The Name Decision

**My final recommendation for the core engine name:**

### **NOESIS** — *The Act of Pure Intellectual Perception*

> *"Noesis is the highest form of knowledge — direct intellectual apprehension of truth, beyond mere opinion or belief."*
> — Plato, *Republic* (Book VI, the Divided Line)

**Usage:**
- The platform: **AUREXIS**
- The engine: **Noesis**  
- Marketing: *"AUREXIS — Powered by the Noesis Engine"*
- Technical: *"Noesis Cognitive Infrastructure v1.0"*
- Domains: *"Noesis Financial" / "Noesis Defense" / "Noesis Weather"*
- Short: *"We built Noesis to see the way we see."*

**Alternatives if Noesis doesn't resonate:**
1. **CORTEXION** — more aggressive, more tech
2. **THALAMOS** — most architecturally accurate
3. **SYNAPTIQ** — most marketable
4. **VERIDEX** — most finance-appropriate

---

*End of Document*

*"The goal was to see the way I see." — Muriu Mwangi*
