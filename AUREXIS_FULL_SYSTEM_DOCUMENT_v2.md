# AUREXIS — Full System Document v2

**Author**: Muriu Mwangi  
**Date**: February 28, 2026  
**Version**: 2.0  
**Classification**: Internal — Technical Audit, Architecture & Honest Assessment  
**Inspection Method**: Automated deep scan of every source file, Dockerfile, config, port mapping, test directory, import graph, and syntax check across all 26 repositories.

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Repository Inventory — All 26 Services](#2-repository-inventory--all-26-services)
3. [Source Code Size by Service](#3-source-code-size-by-service)
4. [Language Breakdown](#4-language-breakdown)
5. [Docker Compose — Full Stack Map](#5-docker-compose--full-stack-map)
6. [Port Assignments](#6-port-assignments)
7. [Shared Library](#7-shared-library)
8. [Event Bus Integration Map](#8-event-bus-integration-map)
9. [Test Coverage](#9-test-coverage)
10. [Health Endpoints](#10-health-endpoints)
11. [Dockerfile & K8s/Helm Status](#11-dockerfile--k8shelm-status)
12. [Known Defects](#12-known-defects)
13. [Service-by-Service Assessment](#13-service-by-service-assessment)
14. [Infrastructure Dependencies](#14-infrastructure-dependencies)
15. [What Does Not Exist Yet](#15-what-does-not-exist-yet)
16. [Honest Summary](#16-honest-summary)

---

## 1. System Overview

AUREXIS is a cognitive intelligence platform built as 26 independent microservices. Each service has its own Git repository under the `AUREXIS-A` GitHub organization. There is no monorepo — the root directory is an untracked workspace folder that holds all 26 service directories side by side, plus a docker-compose.yml that orchestrates them.

**What it is designed to do**: Process raw market data through a cognitive pipeline — perception → shape recognition → meaning extraction → reasoning → decision → explanation → learning feedback. Forex is the first domain; the architecture claims domain-agnostic capability.

**What it actually does today**: The code exists. Services compile (with one exception noted below). Docker images can be built. The cognitive pipeline is wired end-to-end in code. But no service has been started and validated against live data in this audit. No end-to-end integration test exists. No broker connection exists.

**Total source code**: ~341,000 lines across 26 repositories (excluding tests, venvs, node_modules, and build artifacts).

---

## 2. Repository Inventory — All 26 Services

| # | Service | Language | GitHub Remote | Role |
|---|---------|----------|---------------|------|
| 1 | Back_End_Auth_System | Node.js (Express) | AUREXIS-A/Back_End_Auth_System | Authentication, 2FA, OAuth, payments |
| 2 | candle-constructor | Python (FastAPI) | AUREXIS-A/candle-constructor | Builds OHLCV candles from raw ticks |
| 3 | core-brain | Python (FastAPI) | AUREXIS-A/core-brain- | Central orchestrator, cognitive pipeline coordinator |
| 4 | event-bus | Go (Gin) | AUREXIS-A/event-bus | Message broker abstraction (NATS/Redis/Kafka) |
| 5 | explanation-engine | Python (FastAPI) | AUREXIS-A/explanation-engine | Generates human-readable explanations for decisions |
| 6 | frontend | TypeScript (React) | AUREXIS-A/frontend | Trading dashboard, charts, cognitive state display |
| 7 | gateway | Go | AUREXIS-A/gateway | API gateway, routing, rate limiting, auth proxy |
| 8 | knowledge-graph | Python (FastAPI) | AUREXIS-A/knowledge-graph | Neo4j-backed knowledge store, pattern relationships |
| 9 | Landing_Page | TypeScript (React) | AUREXIS-A/Landing_Page | Public marketing site, 8 intelligence domains |
| 10 | language-intelligence | Python (FastAPI) | AUREXIS-A/language-intelligence | NLP, sentiment analysis, news processing |
| 11 | learning-engine | Python (FastAPI) | AUREXIS-A/learning-engine | Punishment/reward loops, model retraining |
| 12 | lightweight-charts | TypeScript | AUREXIS-A/lightweight-charts | Fork of TradingView lightweight-charts library |
| 13 | market-ingestion | Python (FastAPI) | AUREXIS-A/market-ingestion | Raw data intake: CSV, Excel, JSON, PDF, APIs |
| 14 | meaning-engine | Python (FastAPI) | AUREXIS-A/meaning-engine | Extracts semantic meaning from recognized patterns |
| 15 | memory | Python (FastAPI) | AUREXIS-A/memory | Short/long-term memory, pattern recall |
| 16 | ontology | Python (FastAPI) | AUREXIS-A/ontology- | Domain ontology definitions, concept hierarchies |
| 17 | perception | Python (FastAPI) | AUREXIS-A/perception- | First cognitive layer: raw signal → structured perception |
| 18 | policy-engine | Python (FastAPI) | AUREXIS-A/policy-engine | Risk rules, permission enforcement, compliance |
| 19 | price-observer | Rust (Actix) | AUREXIS-A/price-observer | Real-time price feed listener |
| 20 | reasoning-engine | Python (FastAPI) | AUREXIS-A/reasoning-engine | Formal reasoning, decision logic |
| 21 | schema-registry | Go | AUREXIS-A/schema-registry | Event schema validation, versioning |
| 22 | security | Node.js (Express) | AUREXIS-A/Security | Encryption, secrets, HSM, audit logging, WAF |
| 23 | shape-engine | Python (FastAPI) | AUREXIS-A/shape-engine | Candlestick pattern recognition, shape classification |
| 24 | shared | Python (library) | AUREXIS-A/shared | Common models, utils, event bus client, tracing |
| 25 | simulation | Python (FastAPI) | AUREXIS-A/simulation | Backtesting, Monte Carlo, strategy simulation |
| 26 | topology-hub | Go (Gin) | AUREXIS-A/topology-hub | Service discovery, topology registration |
| — | topology-hub-express | Node.js (Express) | AUREXIS-A/topology-hub-express | Thin Node.js companion for topology-hub |

**Note**: Three repos have a trailing dash in GitHub: `core-brain-`, `ontology-`, `perception-`. This is a naming inconsistency.

---

## 3. Source Code Size by Service

Lines of source code (*.py, *.go, *.rs, *.js, *.ts, *.tsx), excluding tests, venvs, node_modules, and build artifacts:

| Service | Lines | Language |
|---------|------:|----------|
| frontend | 58,478 | TypeScript/React |
| security | 25,754 | JavaScript/Node |
| shape-engine | 24,642 | Python |
| learning-engine | 18,774 | Python |
| Back_End_Auth_System | 18,584 | JavaScript/Node |
| ontology | 16,772 | Python |
| knowledge-graph | 15,203 | Python |
| simulation | 15,117 | Python |
| Landing_Page | 13,423 | TypeScript/React |
| perception | 13,083 | Python |
| core-brain | 12,698 | Python |
| language-intelligence | 11,854 | Python |
| memory | 11,706 | Python |
| meaning-engine | 11,142 | Python |
| explanation-engine | 11,066 | Python |
| reasoning-engine | 10,864 | Python |
| event-bus | 9,574 | Go |
| price-observer | 7,947 | Rust |
| gateway | 6,987 | Go |
| candle-constructor | 6,660 | Python |
| market-ingestion | 6,022 | Python |
| schema-registry | 4,280 | Go |
| shared | 3,615 | Python |
| policy-engine | 3,580 | Python |
| topology-hub | 2,496 | Go |
| topology-hub-express | 844 | JavaScript/Node |
| **Total** | **~341,000** | |

---

## 4. Language Breakdown

| Language | Services | Total Lines |
|----------|----------|-------------|
| Python | 15 services + shared library | ~196,000 |
| TypeScript/React | 2 (frontend, Landing_Page) + lightweight-charts (fork) | ~72,000 |
| Go | 4 (event-bus, gateway, schema-registry, topology-hub) | ~23,300 |
| JavaScript/Node | 3 (Back_End_Auth_System, security, topology-hub-express) | ~45,200 |
| Rust | 1 (price-observer) | ~7,900 |

All 15 Python services use FastAPI. All 4 Go services use Go 1.21. The 3 Node.js services use Express.

---

## 5. Docker Compose — Full Stack Map

The root `docker-compose.yml` defines **31 containers**:

**Application Services (24):**
auth-service (Back_End_Auth_System), candle-constructor, core-brain, event-bus, explanation-engine, frontend, gateway, knowledge-graph, language-intelligence, learning-engine, market-ingestion, meaning-engine, memory, ontology, perception, policy-engine, price-observer, reasoning-engine, schema-registry, security-core, shape-engine, simulation, topology-hub, topology-hub-express

**Infrastructure (7):**
- PostgreSQL 16 — port 5432
- Redis 7 — port 6380 (host-remapped from 6379)
- MongoDB 7 — port 27018 (host-remapped from 27017, used by auth)
- ClickHouse 23.12 — port 8124 (host-remapped from 8123)
- Prometheus — port 9090
- Jaeger (all-in-one) — ports 16686, 14268, 14250, 5775, 6831, 6832, 5778, 9411
- Neo4j — ports 7474, 7687

**NOT in docker-compose**: Landing_Page, lightweight-charts (fork, reference only), shared (library, not a running service)

**All 24 application containers** have `restart: unless-stopped` and are on the `aurexis-network` bridge.

---

## 6. Port Assignments

| Service | Container Port | Host Port | Notes |
|---------|---------------|-----------|-------|
| frontend | 80 | 80, 3001 | Nginx serves on 80, dual host mapping |
| gateway | 52031 | 52051 | Host-remapped to avoid conflict |
| price-observer | 52002 | 52002 | |
| meaning-engine | 52003 | 52003 | |
| learning-engine | 52004 | 52004 | |
| explanation-engine | 52005 | 52005 | |
| language-intelligence | 52006 | 52006 | |
| reasoning-engine | 52008 | 52008 | |
| shape-engine | 52010, 52011 | 52010, 52011 | Two ports |
| perception | 52012 | 52012 | |
| knowledge-graph | 52015 | 52015 | |
| memory | 52018 | 52018 (Note: same as event-bus default) | Potential conflict with event-bus |
| event-bus | 52020 | 52020 | |
| candle-constructor | 52023 | 52023 | |
| market-ingestion | 52010 | 52024 | Host-remapped — container internally uses 52010, same as shape-engine |
| schema-registry | 52025 | 52025 | |
| policy-engine | 52032 | 52032 | |
| core-brain | 52040 | 52040 | |
| simulation | 52043 | 52043 | |
| ontology | 52100 | 52100 | |
| topology-hub | 8080 | 52016 | Host-remapped |
| topology-hub-express | 3000 | 52017 | Host-remapped |
| auth-service | 5500 | 5500 | |
| security-core | 55000, 9090 | 55000, 55090 | Prometheus metrics on 9090→55090 |

**Port concern**: market-ingestion's container port is 52010, which is the same as shape-engine's container port. The docker-compose remaps it to 52024 on the host — so there is no collision on the host — but if any service tries to reach market-ingestion by its internal port on the docker network, it will work correctly because Docker isolates container ports per container. This is fine but confusing.

---

## 7. Shared Library

The `shared/` repository (2,477 lines in 21 source files) provides:

| Module | Lines | Purpose |
|--------|------:|---------|
| event_bus_client.py | 270 | EventBusClient for publishing/subscribing to events |
| tracing.py | 203 | OpenTelemetry/Jaeger tracing setup |
| envelope.py | 88 | Standard message envelope format |
| topics.py | 106 | Event topic name constants |
| constants/ | — | Timeframes, cognitive states |
| models/ | 733 | CommonTypes, Identifiers, Timestamps |
| utils/ | 897 | Logger, validators, errors, healthcheck |
| contracts/ | — | ServiceInterface, EventSchema |

### Shared Library Adoption

| Status | Services |
|--------|----------|
| **Imports shared** | candle-constructor, core-brain, explanation-engine, knowledge-graph, language-intelligence, learning-engine, market-ingestion, meaning-engine, ontology, perception, policy-engine, reasoning-engine, shape-engine, simulation |
| **Does NOT import shared** | memory |

**memory** is the only Python service that does not import the shared library at all. It operates independently.

### EventBusClient Usage

| Status | Services |
|--------|----------|
| **Uses EventBusClient** | candle-constructor (6 imports), core-brain (4), explanation-engine (4), meaning-engine (4), perception (8), policy-engine (4), reasoning-engine (2), language-intelligence (4), learning-engine (3) |
| **Does NOT use EventBusClient** | market-ingestion, shape-engine, simulation, knowledge-graph, memory, ontology |

Six Python services are not wired into the event bus. Whether this is intentional design or incomplete integration depends on the intended architecture. For a cognitive pipeline that flows through events, having shape-engine and market-ingestion disconnected from the event bus means they would need to be called via direct HTTP, which breaks the event-driven pattern.

---

## 8. Event Bus Integration Map

The event-bus service (Go/Gin, 9,574 lines) provides pub/sub messaging. The cognitive pipeline is supposed to flow:

```
price-observer → market-ingestion → candle-constructor → perception → shape-engine → meaning-engine → reasoning-engine → learning-engine → explanation-engine
                                                                                                    ↕
                                                                                              core-brain (orchestrator)
```

**Actually wired via EventBusClient**: price-observer (Rust, own impl) → candle-constructor ✓ → perception ✓ → meaning-engine ✓ → reasoning-engine ✓ → learning-engine ✓ → explanation-engine ✓ → core-brain ✓

**NOT wired**: market-ingestion, shape-engine, knowledge-graph, memory, ontology, simulation

This means the pipeline has gaps. shape-engine in particular sits between perception and meaning-engine in the cognitive flow, but has no event bus integration — it would need to be invoked by direct HTTP call from perception or core-brain.

---

## 9. Test Coverage

Test files per service (in `tests/` directory only, excluding venv/node_modules):

| Service | Test Files | Assessment |
|---------|----------:|------------|
| shape-engine | 50 | Substantial |
| perception | 12 | Moderate |
| simulation | 11 | Moderate |
| security | 6 | Light |
| gateway | 6 | Light |
| candle-constructor | 6 | Light |
| core-brain | 3 | Minimal |
| event-bus | 3 | Minimal |
| explanation-engine | 3 | Minimal |
| knowledge-graph | 3 | Minimal |
| language-intelligence | 3 | Minimal |
| learning-engine | 3 | Minimal |
| market-ingestion | 3 | Minimal |
| meaning-engine | 3 | Minimal |
| memory | 3 | Minimal |
| ontology | 3 | Minimal |
| policy-engine | 3 | Minimal |
| reasoning-engine | 3 | Minimal |
| price-observer | 1 | Negligible |
| Back_End_Auth_System | 0 | None |
| frontend | 0 | None |
| Landing_Page | 0 | None |
| schema-registry | 0 | None |
| shared | 0 | None |
| topology-hub | 0 | None |
| topology-hub-express | 0 | None |

**7 services have zero tests.** Of the remaining 19, most have exactly 3 test files — likely boilerplate conftest + 2 basic test files. Only shape-engine (50), perception (12), and simulation (11) have test suites that suggest meaningful coverage.

No integration tests exist at the system level. There is no end-to-end test that validates the cognitive pipeline from raw data to decision output.

---

## 10. Health Endpoints

| Service | Health Endpoint | Status |
|---------|----------------|--------|
| candle-constructor | `/health` (http.server fallback in root main.py) | Exists in src/main.py via healthcheck util |
| core-brain | `GET /health` (FastAPI response_model) | ✓ Proper |
| event-bus | `GET /health` (Gin handler) | ✓ Proper |
| explanation-engine | `GET /health` | ✓ |
| gateway | `GET /health` (Go handler) | ✓ Proper |
| knowledge-graph | `GET /health` | ✓ |
| language-intelligence | `GET /health` | ✓ |
| learning-engine | `GET /health` | ✓ |
| market-ingestion | `/health` (http.server in root main.py AND src/main.py) | ✓ |
| meaning-engine | `GET /health` | ✓ |
| memory | `GET /health` | ✓ |
| ontology | `GET {prefix}/health` (prefixed) | ✓ Different pattern |
| perception | `GET /api/v1/health` (prefixed) | ✓ Different pattern |
| policy-engine | `GET /health` | ✓ |
| reasoning-engine | `GET /health` | ✓ |
| schema-registry | Assumed (Go service) | Not verified in src |
| security | Express routes | Assumed via health.routes.js |
| shape-engine | `GET /health` | ✓ |
| simulation | Uses HealthFramework utility | ✓ Via framework, not in main.py directly |
| topology-hub | Go service | Not verified |
| topology-hub-express | Node service | Not verified |
| Back_End_Auth_System | Express service | Not verified |

**Inconsistency**: Most services use `/health`. Ontology uses `{prefix}/health`. Perception uses `/api/v1/health`. This inconsistency means the docker-compose healthcheck commands cannot use a uniform pattern.

---

## 11. Dockerfile & K8s/Helm Status

### Dockerfiles

| Status | Services |
|--------|----------|
| **Has Dockerfile** | All 23 running services (everything except Landing_Page, lightweight-charts, shared) |
| **Missing Dockerfile** | Landing_Page, lightweight-charts, shared |

`shared` is a library — no Dockerfile needed. `lightweight-charts` is a reference fork — no Dockerfile needed. **Landing_Page** is a real user-facing service that should have a Dockerfile and does not.

### K8s / Helm Charts

| Status | Services |
|--------|----------|
| **Has k8s/ and/or helm/** | 22 services |
| **Missing k8s/helm** | Landing_Page, lightweight-charts, shared, topology-hub-express |

topology-hub-express is a running service without Kubernetes deployment manifests.

---

## 12. Known Defects

### 12.1 Syntax Error — policy-engine

**File**: `policy-engine/src/enforcement/policy_engine.py`, line 215  
**Error**: `SyntaxError: unmatched ')'`

```python
                        decision.violated_rules.append(ViolatedRule(
                            rule_name="FORBIDDEN_CONTEXT_PRESENT",
                            policy_type=PolicyType.PERMISSION,
                            severity=Severity.CRITICAL,
                            message=f"Forbidden context '{forbidden_key}' is present",
                        ))
                ))   # ← This line is the problem. Extra unmatched '))'
```

This file will not import. The policy-engine service **cannot start** in its current state. This is a production-blocking defect.

### 12.2 Stub main.py Files

Three Python services have a root-level `main.py` that is a simple `http.server` stub (not FastAPI):
- `perception/main.py`
- `language-intelligence/main.py`
- `market-ingestion/main.py`

All three have a proper `src/main.py` with FastAPI. The Dockerfiles reference `src.main`, so the stub files are not used in Docker. They exist as manual fallbacks — if someone runs `python main.py` directly, they get a basic health-only HTTP server instead of the real service. This is not a defect, but it is confusing.

### 12.3 Local venv Directories

Three services have local `venv/` directories on disk:

| Service | venv Size | In .gitignore? | Git-tracked? |
|---------|-----------|----------------|--------------|
| meaning-engine | 7.2 GB | **No** | No (untracked) |
| language-intelligence | 27 MB | Yes | No |
| ontology | 95 MB | Yes | No |

meaning-engine's `.gitignore` does **not** exclude `venv/`. It is currently untracked only because it has never been `git add`-ed. If someone runs `git add .` in meaning-engine, they will commit 7.2 GB of Python packages to GitHub.

### 12.4 Missing .gitignore Entry

**meaning-engine/.gitignore** does not include `venv/` or `.venv`. All other Python services that have local venvs properly exclude them.

### 12.5 memory Service — No Shared Integration

The `memory` service (11,706 lines) does not import the shared library at all. It operates with its own internal utilities. Whether this is intentional isolation or an oversight is unknown.

### 12.6 GitHub Naming Inconsistency

Three repos have trailing dashes in their GitHub names:
- `core-brain-` (repo name) vs `core-brain` (directory name)
- `ontology-` vs `ontology`
- `perception-` vs `perception`

This has no functional impact but creates confusion when referencing repos.

---

## 13. Service-by-Service Assessment

### Cognitive Pipeline Services (the brain)

**price-observer** (Rust, 7,947 lines)  
Real-time price feed listener. Rust/Actix. Has Dockerfile, K8s manifests, 1 test file. This is the sensory input — the ear of the system. It listens and forwards. The code is structurally present. Without a live broker connection, it has nothing to listen to.

**market-ingestion** (Python, 6,022 lines)  
Reads CSV/Excel/JSON/PDF/API data, normalizes it, forwards it. Does NOT use EventBusClient — forwards via direct HTTP or internal queuing. Has a stub root main.py plus a proper src/main.py. 3 test files. 38 requirements.txt entries. Functional structure present.

**candle-constructor** (Python, 6,660 lines)  
Builds OHLCV candles from raw ticks. Uses EventBusClient (6 imports). Depends on ClickHouse. 6 test files. 16 requirements.txt entries. Lean and focused.

**perception** (Python, 13,083 lines)  
First cognitive layer. Heavy EventBusClient usage (8 imports). Has stub root main.py. 12 test files. Health endpoint at `/api/v1/health` (non-standard prefix). 42 requirements.

**shape-engine** (Python, 24,642 lines)  
Largest Python service. Candlestick pattern recognition, shape classification. 50 test files — the best-tested service. Does NOT use EventBusClient. 56 requirements. This is a substantial body of pattern recognition code.

**meaning-engine** (Python, 11,142 lines)  
Extracts semantic meaning from recognized patterns. Uses EventBusClient (4 imports). 3 test files. 74 requirements (heavy — includes spaCy, sklearn, networkx, sympy). Has 7.2 GB local venv. `.gitignore` missing venv exclusion.

**reasoning-engine** (Python, 10,864 lines)  
Formal reasoning, decision logic. Uses EventBusClient (2 imports). 3 test files. 44 requirements.

**learning-engine** (Python, 18,774 lines)  
Punishment/reward loops, model retraining. Uses EventBusClient (3 imports). 3 test files. 59 requirements. Second-largest Python backend service.

**explanation-engine** (Python, 11,066 lines)  
Generates human-readable explanations. Uses EventBusClient (4 imports). 3 test files. 63 requirements.

**core-brain** (Python, 12,698 lines)  
Central orchestrator. Uses EventBusClient (4 imports). 3 test files. 55 requirements. This is supposed to coordinate the entire pipeline. Its health endpoint is properly typed with `response_model=HealthResponse`.

### Support Services

**knowledge-graph** (Python, 15,203 lines)  
Neo4j-backed. Does NOT use EventBusClient. 3 test files. 119 requirements (largest dependency set — includes neo4j, spacy, transformers, torch, sklearn). Heavy.

**memory** (Python, 11,706 lines)  
Short/long-term memory. Does NOT import shared library at all. 3 test files. 32 requirements. Operates in isolation.

**ontology** (Python, 16,772 lines)  
Domain concepts, hierarchies. Does NOT use EventBusClient. 3 test files. 43 requirements. Has local venv (95 MB, gitignored).

**policy-engine** (Python, 3,580 lines)  
Smallest Python service. Uses EventBusClient (4 imports). 3 test files. 10 requirements. **HAS A SYNTAX ERROR** — cannot start. See Known Defects §12.1.

**simulation** (Python, 15,117 lines)  
Backtesting, Monte Carlo. Does NOT use EventBusClient. 11 test files. 45 requirements. Uses HealthFramework utility instead of inline health endpoint. No `/health` endpoint found directly in `src/main.py` — relies on `health_framework.py` utility to register it.

**language-intelligence** (Python, 11,854 lines)  
NLP, sentiment. Uses EventBusClient (4 imports). Has stub root main.py. 3 test files. 51 requirements. Has local venv (27 MB, gitignored).

### Infrastructure / Routing Services

**event-bus** (Go, 9,574 lines)  
Gin-based pub/sub. 3 test files. Proper health handler. The backbone of the event-driven architecture. Services that don't use EventBusClient bypass this entirely.

**gateway** (Go, 6,987 lines)  
API gateway. 6 test files. Has health handler, validation middleware, rate limiting. Routes to all backend services. Proper Go project structure with handlers/, middleware/, models/, config/.

**schema-registry** (Go, 4,280 lines)  
Event schema validation. 0 test files. No tests at all for a schema validation service.

**topology-hub** (Go, 2,496 lines)  
Service discovery. Flat structure (no src/ — just *.go files at root). 0 test files (hub_test.go exists but is counted separately). Has client examples in Python and Rust.

**topology-hub-express** (Node.js, 844 lines)  
Thin Node.js companion. 0 test files. No K8s/Helm. Just `server.js` (Express) + `client.js` + `useTopologyHub.js` (React hook). This is the thinnest service—essentially a bridge.

### Auth / Security / Frontend

**Back_End_Auth_System** (Node.js, 18,584 lines)  
Express. 2FA, OAuth, Paystack payments, email verification, session management. 0 test files. 27 npm dependencies. Uses MongoDB (auth-mongo container). Comprehensive auth code but completely untested.

**security** (Node.js, 25,754 lines)  
The second-largest non-frontend service. Encryption, HSM, audit, WAF, secrets management, compliance checks, military-grade claims. 6 test files for 25K+ lines. 14 npm dependencies. 93 source files across crypto/, identity/, compliance/, audit/, resilience/, ingestion/, secrets/, admin/, api/. Large surface area with thin test coverage.

**frontend** (TypeScript/React, 58,478 lines)  
Largest repository. Trading dashboard. 29 npm dependencies, 17 devDependencies. 0 test files. Zero. The largest codebase in the system has no tests.

**Landing_Page** (TypeScript/React, 13,423 lines)  
Marketing site. 51 npm dependencies (more than the frontend). 0 test files. No Dockerfile. No K8s.

**lightweight-charts** (TypeScript)  
Fork of TradingView's lightweight-charts. Not an AUREXIS-authored service. Included as a dependency reference. No Dockerfile, no tests relevant to AUREXIS.

**shared** (Python, 3,615 lines / 2,477 source lines)  
Common library. Provides EventBusClient, tracing, envelope, models, utils, constants. 0 test files. Used by 14 of 15 Python services. This is the connective tissue of the system and it has no tests.

---

## 14. Infrastructure Dependencies

| Infrastructure | Version | Used By |
|----------------|---------|---------|
| PostgreSQL | 16 | Most Python services (primary datastore) |
| Redis | 7 | Caching, session, event-bus backend |
| MongoDB | 7 | Back_End_Auth_System only |
| ClickHouse | 23.12 | candle-constructor (OHLCV storage) |
| Neo4j | (latest) | knowledge-graph |
| Prometheus | (latest) | Metrics collection |
| Jaeger | (all-in-one) | Distributed tracing |

All infrastructure runs as Docker containers in the same compose stack. No managed cloud services — everything is self-hosted.

---

## 15. What Does Not Exist Yet

These are absent from the codebase — not partially implemented, but entirely nonexistent:

1. **Live broker connection** — No Deriv, OANDA, or any broker API integration. price-observer has the framework but no actual broker adapter.
2. **Order execution service** — No service places trades. The system can analyze and decide, but cannot act.
3. **Client portfolio tracker** — No portfolio management, P&L tracking, or position monitoring.
4. **KYC / Identity verification** — No ID upload, no facial recognition, no document verification.
5. **Deposit / withdrawal flow** — No bank integration beyond Paystack's one-time application fee.
6. **End-to-end integration tests** — No test validates the full cognitive pipeline from data ingestion to decision output.
7. **CI/CD pipeline** — The `.github/` workflows were archived. No automated build, test, or deploy pipeline exists.
8. **Monitoring dashboards** — Prometheus collects metrics but there is no visualization layer (Grafana was intentionally removed).
9. **Live data feed** — No websocket connection to any live market data source.
10. **User notification system** — No push notifications, no SMS, no real-time alerts to users.

---

## 16. Honest Summary

**What is real:**
- 26 repositories with ~341,000 lines of source code across 5 languages
- A coherent cognitive pipeline architecture (perception → shape → meaning → reasoning → learning → explanation)
- Docker Compose orchestration for 31 containers
- Every service has a README, most have Dockerfiles, K8s manifests, and health endpoints
- The shared library provides genuine connective tissue between Python services
- 9 of 15 Python services are properly wired to the event bus
- shape-engine has substantial pattern recognition code with 50 test files

**What is fragile:**
- policy-engine has a syntax error and cannot start
- 7 services have zero tests (including the frontend at 58K lines and the shared library)
- Most services with tests have exactly 3 files — likely minimal boilerplate
- The event bus integration has gaps: 6 Python services are not connected
- meaning-engine has a 7.2 GB venv without .gitignore protection
- No end-to-end test validates that the pipeline actually works when services communicate
- health endpoint paths are inconsistent across services

**What is absent:**
- No live data connection, no broker, no order execution
- No integration tests
- No CI/CD
- No KYC, no portfolio tracking, no deposit/withdrawal

**The system is a codebase, not a running product.** The architecture is designed and the code is written, but nothing has been validated end-to-end against real data or in a live environment. The cognitive pipeline exists in code; whether it produces correct outputs when all services are running and communicating is unverified.

---

*Document generated from automated deep scan of all 26 repositories. All line counts, file counts, port mappings, and defect reports are derived from direct file system inspection — not from documentation or assumptions.*
