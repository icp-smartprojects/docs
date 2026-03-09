# AUREXIS FUSION ARCHITECTURE — FULL GAP ANALYSIS

**Date:** 2026-03-09  
**Scope:** 9 Chapters of the Fusion & Parallel Processing Architecture Document  
**Method:** Line-by-line codebase audit of every claim  
**Verdict:** 43 claims audited — **15 Implemented, 15 Partial, 13 Not Implemented**

---

## TABLE OF CONTENTS

1. [Executive Summary](#1-executive-summary)
2. [Scorecard Overview](#2-scorecard-overview)
3. [Ch02 — Parallel TF Construction (5 gaps)](#3-ch02--parallel-tf-construction)
4. [Ch03 — 256-D TimeSpace Vector (5 gaps)](#4-ch03--256-d-timespace-vector)
5. [Ch04 — 6-Stage Meaning Pipeline (4 gaps)](#5-ch04--6-stage-meaning-pipeline)
6. [Ch05 — Confluence Formula (3 gaps)](#6-ch05--confluence-formula)
7. [Ch06 — SSE Parallel Mesh (1 gap)](#7-ch06--sse-parallel-mesh)
8. [Ch07 — Belief Graph (4 gaps)](#8-ch07--belief-graph)
9. [Ch08 — World State Fusion (2 gaps)](#9-ch08--world-state-fusion)
10. [Ch09 — End-to-End Timeline (4 gaps)](#10-ch09--end-to-end-timeline)
11. [Full Gap Registry (28 items)](#11-full-gap-registry)
12. [Service Impact Map](#12-service-impact-map)
13. [Effort Estimation](#13-effort-estimation)
14. [Priority Tiers](#14-priority-tiers)

---

## 1. EXECUTIVE SUMMARY

The Fusion Architecture Document describes a highly parallel, cross-timeframe intelligence system. After auditing every claim against the actual codebase:

| Verdict | Count | % |
|---------|-------|---|
| ✅ Implemented as described | 15 | 35% |
| ⚠️ Partial / Different from doc | 15 | 35% |
| ❌ Not implemented at all | 13 | 30% |

**The core skeleton is real.** The 256-D vector exists (256 enforced), the Event Bus streams SSE, the 6-stage meaning pipeline runs, the 10-step decision pipeline produces decisions, SHA-256 audit hashing works, GBM simulation cones fire.

**What's missing is the cross-service intelligence wiring.** The LTF/HTF vector dimensions are stubs (always 0.0), candle construction is sequential not parallel, the belief graph lifecycle states differ from the document, the evidence weighting formula measures quality dimensions not service origins, and there's no pipeline timing enforcement.

**Total gaps (❌ + ⚠️): 28 items across 10 services.**

---

## 2. SCORECARD OVERVIEW

| Chapter | ✅ | ⚠️ | ❌ | Total |
|---------|-----|-----|-----|-------|
| Ch02 — Parallel TF Construction | 0 | 0 | 5 | 5 |
| Ch03 — 256-D Vector | 2 | 1 | 3 | 6 |
| Ch04 — 6-Stage Meaning Pipeline | 2 | 3 | 0 | 5 |
| Ch05 — Confluence Formula | 2 | 2 | 1 | 5 |
| Ch06 — SSE Parallel Mesh | 4 | 1 | 1 | 6 |
| Ch07 — Belief Graph | 2 | 3 | 2 | 7 |
| Ch08 — World State Fusion | 4 | 2 | 1 | 7 |
| Ch09 — End-to-End Timeline | 0 | 3 | 1 | 4 (extra beyond Ch01-08 overlap removed) |
| **TOTAL** | **15** | **15** | **13** | **43** |

---

## 3. CH02 — PARALLEL TF CONSTRUCTION

### What the doc says
> "AUREXIS builds 15 timeframes simultaneously, each published to Event Bus on its own topic, using rolling windows per TF, reading from ClickHouse V25_1S table."

### What the code actually does
Sequential for-loop over 13 timeframes, time-bucket aggregation, all candles published to a single `"candles"` topic.

---

### GAP 2.1 — Timeframe Count (13 not 15) ❌

| Field | Detail |
|-------|--------|
| **Doc claim** | 15 timeframes: S1, S2, S5, S15, M1, M5, M15, M30, H1, H4, D1, W1, MO1 |
| **Code reality** | 13 timeframes: S1, S2, M1, M2, M3, M5, M15, M30, H1, H4, D1, W1, MO1 |
| **Missing** | `S5` (5-second) and `S15` (15-second) do not exist |
| **Extra in code** | `M2` (2-minute) and `M3` (3-minute) exist but are NOT in the doc |
| **Where** | `candle-constructor/src/timeframe_registry.py` — `Timeframe` enum (lines 22-35) |
| **Service to fix** | `candle-constructor` |
| **What it would take** | Add S5 and S15 to the `Timeframe` enum and `ALL_TIMEFRAMES`, add aggregation bucket logic for 5s and 15s intervals |
| **Effort** | Small (1-2 hours) |

---

### GAP 2.2 — Per-TF Event Bus Topics ❌

| Field | Detail |
|-------|--------|
| **Doc claim** | "Each aggregated candle published to Event Bus on its own topic" (e.g. `candles.M5`, `candles.H1`) |
| **Code reality** | ALL candle events go to a single `"candles"` topic regardless of timeframe |
| **Where** | `candle-constructor/src/eventbus/client.py` — topic resolution at line 43-49, always returns `"candles"` |
| **Service to fix** | `candle-constructor` (publisher) + `event-bus` (topic registration) + all subscribers (topic filters) |
| **What it would take** | Change topic resolution to `f"candles.{timeframe}"`, register 13+ topics in Event Bus, update all downstream subscribers to subscribe to specific TF topics or wildcard |
| **Effort** | Medium (4-6 hours) — cascading change across multiple subscribers |

---

### GAP 2.3 — Parallel Construction ❌

| Field | Detail |
|-------|--------|
| **Doc claim** | "Builds 15 timeframes simultaneously" — implies concurrent/parallel processing |
| **Code reality** | `CandleAggregator.add_tick()` iterates `ALL_TIMEFRAMES` in a **sequential for-loop** |
| **Where** | `candle-constructor/src/aggregation/aggregator.py` — lines 68-93 (`for target_tf in ALL_TIMEFRAMES:`) |
| **Concurrency found** | Zero. No `asyncio.gather`, no `ThreadPoolExecutor`, no `ProcessPoolExecutor` in the aggregation path. The only `asyncio.gather` in the service is for health checks. |
| **Service to fix** | `candle-constructor` |
| **What it would take** | Refactor aggregation to use `asyncio.gather()` or `concurrent.futures` for parallel TF processing. Each TF's bucket state would need its own lock. |
| **Effort** | Medium (4-6 hours) — concurrency + state isolation + testing |
| **Note** | For 13 timeframes with simple arithmetic, parallel overhead may actually be slower than sequential. This is a design debate, not necessarily a bug. |

---

### GAP 2.4 — Rolling Windows ❌

| Field | Detail |
|-------|--------|
| **Doc claim** | "Rolling window per TF" |
| **Code reality** | Time-bucket alignment: `bucket_start = (timestamp // nanos) * nanos`. Candles flush when `current_time >= bucket_end`. This is standard OHLC bucketing. |
| **Where** | `candle-constructor/src/timeframe_registry.py` — line 237 |
| **Service to fix** | `candle-constructor` |
| **What it would take** | Implement sliding/rolling window aggregation alongside bucket aggregation. Each window would overlap with the previous, producing more candles per unit time. |
| **Effort** | Medium-Large (6-10 hours) — fundamental change to aggregation semantics |
| **Note** | Rolling windows produce overlapping candles which may not be desired for downstream consumers. Doc claim may be a misnomer for "running buffer." |

---

### GAP 2.5 — V25_1S Table Description ❌

| Field | Detail |
|-------|--------|
| **Doc claim** | "Reads from ClickHouse V25_1S table at 1s granularity" |
| **Code reality** | `V25_1S` is a **symbol name** (normalized from "Volatility 25 (1s) Index"), not a table. The table is `aurexis.candles` — all symbols and TFs share it. Live path reads from Event Bus SSE, not ClickHouse directly. |
| **Where** | `candle-constructor/src/ingestor.py` — line 83-85 (symbol), line 118-137 (table schema) |
| **Service to fix** | Documentation only — the code is correct |
| **Effort** | Trivial (doc correction) |

---

## 4. CH03 — 256-D TIMESPACE VECTOR

### What the doc says
> "256-D vector with 6 encoding groups: Raw Values (1-8), Derived Features (9-28), Lower TF Context (29-78), Same TF History (79-178), Higher TF Context (179-228), Metadata (229-256)."

### What the code actually does
256-D vector with 4 encoding groups: Geometric(0-63), Temporal(64-127), Contextual(128-191), Semantic(192-255). Cross-TF dimensions are single-float stubs.

---

### GAP 3.1 — Encoding Group Layout ❌

| Field | Detail |
|-------|--------|
| **Doc claim** | 6 groups: Raw Values (8D), Derived Features (20D), LTF Context (50D), Same-TF History (100D), HTF Context (50D), Metadata (28D) |
| **Code reality** | 4 groups, each 64D: Geometric, Temporal, Contextual, Semantic |
| **Where** | `perception/src/models/timespace_vector.py` (lines 48-52), `perception/src/encoding/timespace_encoder.py` (lines 93-97) |
| **Mismatch** | Completely different dimension allocation, group names, and group count. The code's 4×64D layout is a clean design; the doc's 6-group layout with variable sizes is a different schema entirely. |
| **Service to fix** | `perception` |
| **What it would take** | Complete rewrite of all 3 encoders (GeometricEncoder, TemporalEncoder, SemanticEncoder) to match the doc's 6-group layout. Would also need new encoders for Raw Values, Derived Features, and Metadata groups. |
| **Effort** | **Very Large (3-5 days)** — fundamental encoder architecture change |
| **Note** | Current 4×64D design is arguably cleaner. The doc's layout is more feature-engineering-oriented. This is a design philosophy choice. |

---

### GAP 3.2 — LTF Context Dimensions (29-78) ❌ CRITICAL

| Field | Detail |
|-------|--------|
| **Doc claim** | Dims 29-78 (50D) populated with "sub-TF micro state, expansion velocity, order flow" from lower timeframes |
| **Code reality** | **1 single float** (`lower_tf_momentum`) in `ContextualFeatures._compute_multi_scale_features()`. Defaults to 0.0. No service ever populates this field. |
| **Where** | `perception/src/encoding/semantic_encoder.py` — lines 157-170 |
| **Service to fix** | `perception` (consumer) + `candle-constructor` or `meaning-engine` (producer) |
| **What it would take** | (1) A service needs to compute and publish LTF features per instrument/timeframe. (2) Perception needs to receive and decode them into 50 vector dimensions. (3) Cross-service event plumbing for LTF data. |
| **Effort** | **Large (2-3 days)** — cross-service feature engineering + event wiring |
| **Impact** | This is the single biggest intelligence gap. Without real cross-TF data, the 256-D vector is blind to multi-timeframe context. |

---

### GAP 3.3 — HTF Context Dimensions (179-228) ❌ CRITICAL

| Field | Detail |
|-------|--------|
| **Doc claim** | Dims 179-228 (50D) populated with "higher TF trend, structure integrity, volatility regime" |
| **Code reality** | **1 single float** (`higher_tf_alignment` = -1/0/+1) in `ContextualFeatures._compute_multi_scale_features()`. Defaults to 0.0. No service populates it. |
| **Where** | `perception/src/encoding/semantic_encoder.py` — lines 160-165 |
| **Service to fix** | `perception` (consumer) + `meaning-engine` or `core-brain` (producer) |
| **What it would take** | Same as GAP 3.2 but for higher timeframes. Need HTF feature computation, event publishing, and 50D encoding in the vector. |
| **Effort** | **Large (2-3 days)** — mirrors GAP 3.2 |
| **Impact** | Combined with GAP 3.2, **100 of 256 dimensions (39%) are non-functional stubs.** |

---

### GAP 3.4 — Same-TF History (100D rolling) ⚠️

| Field | Detail |
|-------|--------|
| **Doc claim** | Dims 79-178 (100D) from a 100-candle rolling window of same-TF history |
| **Code reality** | `TemporalEncoder` produces 64D (not 100D). Computes ~12 actual features (velocity, acceleration, momentum variants, ROC, volatility, ATR, trend direction/strength, periodicity). Lookback is 20 observations, not 100. Remaining dims are zero-padded. |
| **Where** | `perception/src/encoding/temporal_encoder.py` — lines 80-300, history_size=100 lookback=20 at lines 395-400 |
| **Service to fix** | `perception` |
| **What it would take** | Expand lookback from 20→100, add more temporal features to fill dims, or change to 100D output with richer feature extraction |
| **Effort** | Medium (4-8 hours) |

---

### GAP 3.5 — Vector Persistence to PostgreSQL ❌

| Field | Detail |
|-------|--------|
| **Doc claim** | "Stored in PostgreSQL `shapes.vector` table" |
| **Code reality** | Perception explicitly has **no persistence**: `"Forgets raw observations (no persistence)"` (main.py L11), `"note": "perception does not persist data"` (config.py L444). Vectors are fire-and-forget via Event Bus. |
| **Where** | `perception/src/main.py`, `perception/src/config/config.py` |
| **Service to fix** | `perception` (add persistence layer) or new persistence service |
| **What it would take** | Add PostgreSQL connection, create `shapes.vector` table (instrument, timeframe, timestamp, vector BYTEA/ARRAY, metadata JSONB), add write path after encoding. Also need cleanup/retention policy. |
| **Effort** | Medium (4-8 hours) — DB schema + write path + connection pooling |
| **Note** | Current fire-and-forget design may be intentional for latency. Persistence adds ~5-10ms per write. |

---

## 5. CH04 — 6-STAGE MEANING PIPELINE

### What the doc says
> "6 stages: Anchor Detection → Structure Recognition → Confluence Assessment → Belief Formation → Swing Detection → Semantic State Generation"

### What the code actually does
5 steps in the pipeline function. Belief Formation is embedded in Structure Interpreter as a state machine, not a standalone module.

---

### GAP 4.1 — Anchor Detection Missing S/R, VWAP, Round Numbers ⚠️

| Field | Detail |
|-------|--------|
| **Doc claim** | "Identifies significant price levels: support/resistance zones, VWAP, daily open/close, round numbers" |
| **Code reality** | `AnchorContextBuilder` (209 lines) builds candle context windows — body ratio, wick dominance, expansion velocity, shape proximity. **No S/R zone detection, no VWAP computation, no round-number identification.** |
| **Where** | `meaning-engine/src/core/anchor_context.py` — line 23 |
| **Service to fix** | `meaning-engine` |
| **What it would take** | Add S/R detection (swing high/low clustering), VWAP calculation (volume-weighted average price from candle data), round-number proximity scoring, daily open/close level tracking |
| **Effort** | Medium-Large (1-2 days) — real financial feature engineering |

---

### GAP 4.2 — Structure Recognition Doesn't Detect HH/HL ⚠️

| Field | Detail |
|-------|--------|
| **Doc claim** | "Detects market structure patterns (higher highs/higher lows, break of structure, change of character)" |
| **Code reality** | `StructureInterpreter` (298 lines) **interprets** BOS/CHOCH events from perception upstream — it doesn't **detect** higher-highs/higher-lows itself. Detection happens in the perception service. |
| **Where** | `meaning-engine/src/core/structure_interpreter.py` — line 33 |
| **Service to fix** | `meaning-engine` (or accept that perception does detection) |
| **What it would take** | Either (a) add HH/HL detection logic to meaning-engine, or (b) update doc to reflect that perception does detection and meaning-engine does interpretation |
| **Effort** | Small if doc correction, Medium (1 day) if adding detection logic |
| **Note** | The current split (perception detects, meaning interprets) is arguably better architecture |

---

### GAP 4.3 — Belief Formation Not Standalone ⚠️

| Field | Detail |
|-------|--------|
| **Doc claim** | "Stage 4: Belief Formation — converts confluence into directional beliefs" as a dedicated pipeline stage |
| **Code reality** | The FORMING→CONFIRMED→EXTENDING→RETRACING→WEAKENING→INVALIDATED lifecycle lives in `StructurePhase` enum within `meaning_trading.py`. It's embedded in `StructureInterpreter`, not a standalone module. |
| **Where** | `meaning-engine/src/models/meaning_trading.py` — lines 26-49, `meaning-engine/src/core/structure_interpreter.py` |
| **Service to fix** | `meaning-engine` |
| **What it would take** | Extract belief formation into its own class/module, wire it as a discrete pipeline stage between confluence and swing detection |
| **Effort** | Medium (4-8 hours) — refactoring, not new logic |
| **Note** | Code also uses `RETRACING` where doc says `RETRACTING` — minor naming discrepancy |

---

### GAP 4.4 — Anchor Confidence Scores ⚠️ (Minor)

| Field | Detail |
|-------|--------|
| **Doc claim** | "Outputs anchor points with confidence scores" |
| **Code reality** | Outputs `AnchorContext` objects with ratios and measurements but **no explicit confidence score per anchor** |
| **Where** | `meaning-engine/src/models/meaning_trading.py` — lines 81-165 |
| **Service to fix** | `meaning-engine` |
| **Effort** | Small (1-2 hours) |

---

## 6. CH05 — CONFLUENCE FORMULA

### What the doc says
> "WeightedConsensus = Σ(conf_i × auth_i) / Σ(auth_i), belief decay 0.01/hour multiplicative, min 3 TF for strong."

### What the code actually does
Different denominator, linear (not multiplicative) decay, threshold-based (not count-based) "strong" classification.

---

### GAP 5.1 — Confluence Denominator ⚠️

| Field | Detail |
|-------|--------|
| **Doc claim** | `WeightedConsensus = Σ(conf_i × auth_i) / Σ(auth_i)` — denominator is sum of raw authority weights |
| **Code reality** | `weight = (TF_AUTHORITY[tf] + 1) × state.confidence` — denominator is `Σ(weight for ALL TFs)` = `Σ(conf_i × auth_i)`, not `Σ(auth_i)` |
| **Where** | `meaning-engine/src/graph/belief_graph.py` — lines 309-317 |
| **Service to fix** | `meaning-engine` |
| **What it would take** | Change denominator from `total_weight` to `sum(TF_AUTHORITY.values())` |
| **Effort** | Trivial (10 minutes) — one-line change |
| **Note** | The current formula is arguably better (confidence-weighted denominator penalizes low-confidence TFs), but it doesn't match the doc |

---

### GAP 5.2 — Belief Decay Formula ⚠️

| Field | Detail |
|-------|--------|
| **Doc claim** | `new_conf = conf × (1 - decay_rate × hours_elapsed)` — **multiplicative** decay |
| **Code reality** | `new_conf = max(0.05, conf - 0.01 × hours_elapsed)` — **linear subtraction** with 0.05 floor |
| **Where** | `meaning-engine/src/graph/belief_graph.py` — lines 108-116 |
| **Service to fix** | `meaning-engine` |
| **What it would take** | Change `self.confidence - decay` to `self.confidence * (1 - decay)` |
| **Effort** | Trivial (10 minutes) — one-line change |
| **Note** | The 0.01 rate is correct. Linear vs multiplicative is a behavioral difference: linear decays faster at high confidence, multiplicative preserves proportional relationships. |

---

### GAP 5.3 — Min 3 TF Agreement for "Strong" ❌

| Field | Detail |
|-------|--------|
| **Doc claim** | "Minimum 3 TF agreement for strong confluence" — count-based threshold |
| **Code reality** | "Strong confluence" triggered by `confluence_score > 0.7` at `semantic_state.py` line 180 — **score threshold**, not TF count |
| **Where** | `meaning-engine/src/core/semantic_state.py` — line 180 |
| **Service to fix** | `meaning-engine` |
| **What it would take** | Add a `min_aligned_tfs` check: count how many TFs share the dominant bias, require ≥ 3 for "strong" in addition to score threshold |
| **Effort** | Small (1-2 hours) |

---

## 7. CH06 — SSE PARALLEL MESH

### What the doc says
> "40+ simultaneous SSE subscriptions, per-topic subscription format ?topics=candles,perception"

### What the code actually does
~65 topic subscriptions across ~10 services (actually MORE than claimed), but using singular `?topic=X` not plural.

---

### GAP 6.1 — Subscription Format ✅ RESOLVED

| Field | Detail |
|-------|--------|
| **Doc claim** | `/api/v1/stream?topics=candles,perception` — plural, comma-separated |
| **Code reality** | `/api/v1/stream?topic=candles` — **singular**, one SSE connection per topic |
| **Where** | `event-bus/src/main.go` — line 465: `topic := c.Query("topic")` |
| **Service to fix** | `event-bus` (Go) + `shared/event_bus_client.py` (Python) |
| **What it would take** | Parse comma-separated topics in Go handler, filter events by topic set. Update Python client to send `topics=a,b,c` instead of opening N connections. |
| **Effort** | Medium (4-6 hours) — Go handler change + Python client change + testing |
| **Note** | Current design (one connection per topic) is simpler and allows per-topic reconnection. Multi-topic connections reduce socket count but increase complexity. This is a design trade-off, not necessarily a bug. |

---

### GAP 6.2 — SSE Connection Count ⚠️ (Minor)

| Field | Detail |
|-------|--------|
| **Doc claim** | "40+ simultaneous subscriptions" |
| **Code reality** | **~65 topic subscriptions** across ~10 services — the doc actually **understates** the reality |
| **Where** | Across all service main.py files |
| **Service to fix** | Documentation only — code exceeds the claim |
| **Effort** | None |

---

## 8. CH07 — BELIEF GRAPH

### What the doc says
> "13 TF states, each with FORMING→CONFIRMED→EXTENDING→RETRACING→WEAKENING→INVALIDATED lifecycle, stored in knowledge-graph (PostgreSQL), belief decay multiplicative."

### What the code actually does
11 TF states, uses BiasState + StructureState (not lifecycle states), in-memory in meaning-engine, knowledge-graph uses Neo4j.

---

### GAP 7.1 — TF Count in Belief Graph ⚠️

| Field | Detail |
|-------|--------|
| **Doc claim** | 13 (or "15") timeframe states tracked |
| **Code reality** | **11 TFs** in `TF_HIERARCHY`: S1, S2, M1, M2, M3, M5, M15, M30, H1, H4, D1. Missing: W1 and MO1. |
| **Where** | `meaning-engine/src/graph/belief_graph.py` — lines 42-54 |
| **Service to fix** | `meaning-engine` |
| **What it would take** | Add W1 and MO1 to `TF_HIERARCHY` with appropriate authority values |
| **Effort** | Trivial (15 minutes) |

---

### GAP 7.2 — Belief Graph State Model ✅ RESOLVED

| Field | Detail |
|-------|--------|
| **Doc claim** | Each TF has lifecycle: FORMING → CONFIRMED → EXTENDING → RETRACING → WEAKENING → INVALIDATED |
| **Code reality** | `TimeframeState` in belief_graph.py uses **BiasState** (BULLISH, BEARISH, NEUTRAL, TRANSITIONING) + **StructureState** (BOS_UPWARD, BOS_DOWNWARD, CHOCH_BULLISH, CHOCH_BEARISH, CONSOLIDATION, UNDEFINED). These are **market states**, not lifecycle phases. |
| **Where** | `meaning-engine/src/graph/belief_graph.py` — lines 68-82 |
| **Distinction** | The FORMING→INVALIDATED lifecycle DOES exist — but in `StructurePhase` enum in `meaning_trading.py` (used by `StructureInterpreter`). The **belief graph** doesn't use it. |
| **Service to fix** | `meaning-engine` |
| **What it would take** | Either (a) add a `phase: StructurePhase` field to `TimeframeState` and wire lifecycle transitions, or (b) update doc to reflect the bias+structure model |
| **Effort** | Medium (4-8 hours) if adding lifecycle to belief graph |

---

### GAP 7.3 — Storage: Persisted to Neo4j ✅ RESOLVED

| Field | Detail |
|-------|--------|
| **Doc claim** | "Belief graph stored in knowledge-graph service (PostgreSQL)" |
| **Code reality** | Two errors: (1) Belief graph lives **in-memory** in `meaning-engine`, not knowledge-graph. KG is a downstream consumer via SSE. (2) Knowledge-graph uses **Neo4j** (graph DB), not PostgreSQL. |
| **Where** | `meaning-engine/src/graph/belief_graph.py` (in-memory dataclass), `knowledge-graph/src/server.py` line 628 (SSE consumer), Neo4j URI in knowledge-graph config |
| **Service to fix** | `knowledge-graph` (add persistence path) or `meaning-engine` (add write-through) |
| **What it would take** | Option A: meaning-engine writes belief state to knowledge-graph via API/event on each update. Option B: knowledge-graph's existing SSE consumer already ingests meaning.state events — add Neo4j persistence for belief nodes. |
| **Effort** | Medium (4-8 hours) — persistence layer + schema |
| **Note** | The doc's claim of PostgreSQL is wrong regardless — the knowledge-graph is Neo4j-based. The question is whether to persist belief state to Neo4j (matching actual infra) or add PostgreSQL (matching doc). |

---

### GAP 7.4 — Market Conviction Metric Naming ✅ RESOLVED

| Field | Detail |
|-------|--------|
| **Doc claim** | "Market conviction metric aggregated across all TFs" |
| **Code reality** | `confluence_score` — functionally equivalent (authority-weighted cross-TF confidence alignment), but named "confluence" not "conviction" |
| **Where** | `meaning-engine/src/graph/belief_graph.py` — lines 310-319 |
| **Service to fix** | Naming/alias only |
| **Effort** | Trivial |

---

### GAP 7.5 — Belief Decay Formula (Same as GAP 5.2) ⚠️

Already covered in Ch05. Linear subtraction instead of multiplicative.

---

## 9. CH08 — WORLD STATE FUSION (CORE BRAIN)

### What the doc says
> "7 concurrent fetches via asyncio.gather(), evidence weighting 40% meaning / 20% shape / 20% reasoning / 20% simulation, 10-step pipeline, SHA-256 hashing."

### What the code actually does
7 sequential fetches (not concurrent), evidence weights measure quality dimensions (not service origins), 10-step pipeline exists, SHA-256 exists.

---

### GAP 8.1 — Sequential Not Concurrent Fetches ✅ RESOLVED

| Field | Detail |
|-------|--------|
| **Doc claim** | "7 concurrent service fetches via `asyncio.gather()`" |
| **Code reality** | 7 sequential `await` calls — each waits for the previous to complete before starting the next. No `asyncio.gather()` in the world state build path. |
| **Where** | `core-brain/src/orchestration/world_state.py` — lines 147-155 |
| **Also** | Service list differs: code fetches from **perception, meaning, shape, memory, knowledge_graph, policy, simulation**. Doc says **meaning, shape, learning, reasoning, simulation, knowledge-graph, policy**. Two services differ (perception+memory vs learning+reasoning). |
| **Service to fix** | `core-brain` |
| **What it would take** | Wrap the 7 fetch calls in `asyncio.gather()`. Each fetch already returns independently, so this is straightforward. Also decide if learning-engine and reasoning-engine should be fetched. |
| **Effort** | Small (2-4 hours) — refactor to gather + add missing service fetches |

---

### GAP 8.2 — Evidence Weighting Formula ✅ RESOLVED

| Field | Detail |
|-------|--------|
| **Doc claim** | Evidence weights: 40% meaning-engine, 20% shape-engine, 20% reasoning-engine, 20% simulation — per-service source weights |
| **Code reality** | `BASE_EVIDENCE_WEIGHTS` in `evidence_evaluator.py`: `SOURCE_RELIABILITY: 0.4, EVIDENCE_COUNT: 0.2, FRESHNESS: 0.2, CONFIDENCE: 0.2`. These weight **evidence quality dimensions**, NOT service sources. |
| **Where** | `core-brain/src/decision/evidence_evaluator.py` — lines 33-37 |
| **Service to fix** | `core-brain` |
| **What it would take** | Add a second weight layer: per-service origin weights (meaning=0.4, shape=0.2, reasoning=0.2, simulation=0.2) applied to beliefs based on their source service, in addition to quality dimension weights |
| **Effort** | Medium (4-6 hours) — belief source tracking + weight application |

---

### GAP 8.3 — GBM Projection Horizons ✅ RESOLVED

| Field | Detail |
|-------|--------|
| **Doc claim** | "GBM projected 15m/1h/4h/1D forward" — 4 specific horizons |
| **Code reality** | GBM + 5 cone types (CONTINUATION, RETRACEMENT, REVERSAL, FAKEOUT, CHOP) fully implemented. But horizons are `horizon_candles=50` on a configurable `base_timeframe=M5` — NOT the specific 15m/1h/4h/1D set. |
| **Where** | `simulation/src/branching_engine.py` — lines 346-395, `simulation/src/config/loader.py` — line 56 |
| **Service to fix** | `simulation` |
| **What it would take** | Add multi-horizon projection: run GBM at 15m, 1h, 4h, and 1D forward with appropriate candle counts for each. Currently single-horizon only. |
| **Effort** | Medium (4-6 hours) — 4 parallel GBM runs with different parameters |

---

## 10. CH09 — END-TO-END TIMELINE

### What the doc says
> "Full pipeline < 200ms, event-driven push, all latencies via Prometheus, circuit breakers on all calls."

### What the code actually does
200ms target in docs only, mixed push/pull, gateway has Prometheus/circuit breakers but core-brain doesn't.

---

### GAP 9.1 — 200ms Pipeline Budget ✅ RESOLVED

| Field | Detail |
|-------|--------|
| **Doc claim** | 9-step pipeline completes in < 200ms with per-step timing: tick(0ms) → aggregation(5ms) → vector(10ms) → meaning(30ms) → confluence(50ms) → belief(60ms) → world state(100ms) → decision(150ms) → audit+publish(200ms) |
| **Code reality** | The 200ms target appears in documentation only. `WorkflowOrchestrator` tracks per-step latency but does NOT enforce any budget. No circuit-break or timeout at 200ms. The per-step breakdown is not validated anywhere. |
| **Where** | `core-brain/src/orchestration/workflow_orchestrator.py` — line 48 (tracking exists), `gateway/docs/ARCHITECTURE.md` (target mentioned) |
| **Service to fix** | `core-brain`, possibly all pipeline services |
| **What it would take** | Add per-step timing instrumentation, total pipeline timeout at 200ms, per-step budget enforcement (e.g., cancel remaining steps if cumulative exceeds threshold). Ship as Prometheus histogram observations. |
| **Effort** | **Large (2-3 days)** — cross-service instrumentation + timeout logic + Prometheus metrics |

---

### GAP 9.2 — Core Brain Pipeline is Event-Driven ✅ RESOLVED

| Field | Detail |
|-------|--------|
| **Doc claim** | "Pipeline is event-driven (push, not poll)" |
| **Code reality** | Mixed: Event Bus has genuine SSE pub/sub (push). But core-brain's decision pipeline is **triggered by HTTP POST** to `/api/v1/decision/auto`, then makes **HTTP GET** calls to fetch world state. This is request/response, not event-driven. |
| **Where** | `core-brain/src/orchestration/auto_pipeline.py`, `core-brain/src/main.py` — line ~574 |
| **Service to fix** | `core-brain` |
| **What it would take** | Wire core-brain to trigger decisions automatically from SSE events (e.g., on new meaning.state event) rather than requiring an HTTP POST. The `WorldStateBuilder.ingest_event()` method exists but isn't fully wired. |
| **Effort** | Medium (4-8 hours) — event trigger wiring |

---

### GAP 9.3 — Pipeline-Level Prometheus Metrics ✅ RESOLVED

| Field | Detail |
|-------|--------|
| **Doc claim** | "All latencies measured and exposed via Prometheus metrics" |
| **Code reality** | Gateway has `http_request_duration_seconds` histograms (Go). All services expose `/metrics` via health framework. But **core-brain defines zero custom Prometheus metrics** for pipeline latency, decision duration, evidence quality, or per-step timing. The `/metrics` endpoint only serves default process metrics. |
| **Where** | `gateway/src/middleware/metrics.go` (gateway metrics), `core-brain/src/utils/health_framework.py` (endpoint only) |
| **Service to fix** | `core-brain` + optionally other pipeline services |
| **What it would take** | Add `prometheus_client.Histogram` observations for: total decision latency, per-step latency, evidence score distribution, confidence distribution. Wire into existing pipeline. |
| **Effort** | Medium (4-6 hours) — metric definition + instrumentation points |

---

### GAP 9.4 — Circuit Breakers on Inter-Service Calls ✅ RESOLVED

| Field | Detail |
|-------|--------|
| **Doc claim** | "Circuit breakers on all inter-service calls" |
| **Code reality** | Gateway has proper `gobreaker.CircuitBreaker` (Go). Core-brain uses `tenacity` for **retries with exponential backoff** — but tenacity is a retry library, NOT a circuit breaker. It doesn't track failure rates, open/close states, or do fast-fail. |
| **Where** | `gateway/src/services/circuitbreaker.go` (real CB), `core-brain/src/integration/service_client.py` lines 51-54 (retries only) |
| **Service to fix** | `core-brain` (+ any Python service using `ServiceClient`) |
| **What it would take** | Add `pybreaker` or similar circuit breaker library wrapping the `ServiceClient.get()`/`post()` methods. Configure failure thresholds, open duration, half-open probing. |
| **Effort** | Medium (4-6 hours) — library integration + per-service configuration |

---

## 11. FULL GAP REGISTRY

Complete list of all 28 gaps (13 ❌ + 15 ⚠️), ordered by severity:

### CRITICAL (❌ Not Implemented)

| ID | Gap | Service(s) | Effort |
|----|-----|-----------|--------|
| GAP-3.2 | LTF context dims (29-78) always 0.0 | `perception` + producer service | 2-3 days |
| GAP-3.3 | HTF context dims (179-228) always 0.0 | `perception` + producer service | 2-3 days |
| GAP-3.1 | Encoding groups layout (4 vs 6 groups) | `perception` | 3-5 days |
| GAP-8.2 | Evidence weighting per service origin | `core-brain` | 4-6 hours |
| GAP-7.3 | Belief graph not persisted (in-memory only) | `meaning-engine` / `knowledge-graph` | 4-8 hours |
| GAP-7.2 | Belief graph lifecycle states differ | `meaning-engine` | 4-8 hours |
| GAP-9.1 | 200ms pipeline budget not enforced | `core-brain` + all services | 2-3 days |
| GAP-3.5 | Vector not persisted to any DB | `perception` | 4-8 hours |
| GAP-5.3 | Min 3 TF count for "strong" confluence | `meaning-engine` | 1-2 hours |
| GAP-2.1 | 13 TFs not 15 (S5/S15 missing) | `candle-constructor` | 1-2 hours |
| GAP-2.2 | Single candle topic, not per-TF | `candle-constructor` + subscribers | 4-6 hours |
| GAP-2.3 | Sequential aggregation, not parallel | `candle-constructor` | 4-6 hours |
| GAP-6.1 | Subscription format singular not plural | `event-bus` + `shared` | 4-6 hours |

### PARTIAL (⚠️ Implemented Differently)

| ID | Gap | Service(s) | Effort |
|----|-----|-----------|--------|
| GAP-2.4 | Time-bucket not rolling window | `candle-constructor` | 6-10 hours |
| GAP-3.4 | Same-TF history 64D/20-lookback not 100D/100 | `perception` | 4-8 hours |
| GAP-4.1 | Anchor missing S/R, VWAP, round numbers | `meaning-engine` | 1-2 days |
| GAP-4.2 | Structure interprets, doesn't detect HH/HL | `meaning-engine` | 1 day |
| GAP-4.3 | Belief formation not standalone module | `meaning-engine` | 4-8 hours |
| GAP-4.4 | Anchor confidence scores missing | `meaning-engine` | 1-2 hours |
| GAP-5.1 | Confluence denominator differs | `meaning-engine` | 10 min |
| GAP-5.2 | Decay linear not multiplicative | `meaning-engine` | 10 min |
| GAP-7.1 | 11 TFs not 13 in belief graph | `meaning-engine` | 15 min |
| GAP-7.4 | "Conviction" vs "confluence" naming | `meaning-engine` | trivial |
| GAP-8.1 | Sequential fetches, not concurrent | `core-brain` | 2-4 hours |
| GAP-8.3 | GBM single horizon, not 4 specific | `simulation` | 4-6 hours |
| GAP-9.2 | Core-brain is request/response | `core-brain` | 4-8 hours |
| GAP-9.3 | No custom Prometheus pipeline metrics | `core-brain` | 4-6 hours |
| GAP-9.4 | Retries not circuit breakers | `core-brain` | 4-6 hours |

### DOC-ONLY (Inaccurate documentation, code is fine)

| ID | Gap | Issue |
|----|-----|-------|
| GAP-2.5 | V25_1S described as table, it's a symbol | Doc correction only |
| GAP-6.2 | "40+" understated — actually ~65 | Doc correction only |

---

## 12. SERVICE IMPACT MAP

Which services would need changes, and how many gaps hit each:

| Service | Gaps | IDs |
|---------|------|-----|
| **`meaning-engine`** | 11 | 4.1, 4.2, 4.3, 4.4, 5.1, 5.2, 5.3, 7.1, 7.2, 7.3, 7.4 |
| **`perception`** | 5 | 3.1, 3.2, 3.3, 3.4, 3.5 |
| **`core-brain`** | 6 | 8.1, 8.2, 9.1, 9.2, 9.3, 9.4 |
| **`candle-constructor`** | 4 | 2.1, 2.2, 2.3, 2.4 |
| **`event-bus`** | 2 | 2.2, 6.1 |
| **`simulation`** | 1 | 8.3 |
| **`knowledge-graph`** | 1 | 7.3 |
| **`shared/`** | 1 | 6.1 |

**Heaviest hit: `meaning-engine` (11 gaps), `core-brain` (6 gaps), `perception` (5 gaps).**

---

## 13. EFFORT ESTIMATION

### By Size

| Size | Count | Items | Estimated Time |
|------|-------|-------|----------------|
| Trivial (< 30 min) | 5 | 5.1, 5.2, 7.1, 7.4, 2.5 | ~2 hours |
| Small (1-4 hours) | 6 | 2.1, 4.4, 5.3, 8.1, 6.2 | ~12 hours |
| Medium (4-8 hours) | 12 | 2.2, 2.3, 3.4, 3.5, 4.3, 6.1, 7.2, 7.3, 8.2, 8.3, 9.3, 9.4 | ~72 hours |
| Large (1-3 days) | 4 | 4.1, 4.2, 9.2, 9.1 | ~40 hours |
| Very Large (3-5 days) | 3 | 3.1, 3.2, 3.3 | ~60 hours |

### Total Estimated Effort

| Category | Hours |
|----------|-------|
| Trivial + Small | ~14 hours |
| Medium | ~72 hours |
| Large + Very Large | ~100 hours |
| **TOTAL** | **~186 hours (~23 working days / ~5 weeks)** |

> **Reality check:** This is implementation time only. Testing, integration verification, and E2E regression would add 30-50% on top → **~7-8 weeks total** for the full gap closure.

---

## 14. PRIORITY TIERS

### TIER 1 — Quick Wins (Do First, < 1 Day Total)

These are trivial/small fixes that bring the code closer to the doc with minimal risk:

| ID | Gap | Time | Service |
|----|-----|------|---------|
| 5.1 | Fix confluence denominator | 10 min | meaning-engine |
| 5.2 | Fix decay to multiplicative | 10 min | meaning-engine |
| 7.1 | Add W1/MO1 to TF_HIERARCHY | 15 min | meaning-engine |
| 2.1 | Add S5/S15 timeframes | 1-2 hrs | candle-constructor |
| 5.3 | Add min 3 TF count check | 1-2 hrs | meaning-engine |
| 4.4 | Add anchor confidence scores | 1-2 hrs | meaning-engine |
| 8.1 | asyncio.gather() for world state | 2-4 hrs | core-brain |

**Subtotal: ~8 hours**

---

### TIER 2 — Structural Improvements (1-2 Weeks)

Medium-effort items that improve system architecture:

| ID | Gap | Time | Service |
|----|-----|------|---------|
| 7.2 | Wire lifecycle states into belief graph | 4-8 hrs | meaning-engine |
| 7.3 | Persist belief graph to Neo4j | 4-8 hrs | meaning-engine + knowledge-graph |
| 3.5 | Add vector persistence (PostgreSQL) | 4-8 hrs | perception |
| 8.2 | Add per-service evidence weighting | 4-6 hrs | core-brain |
| 8.3 | Multi-horizon GBM (15m/1h/4h/1D) | 4-6 hrs | simulation |
| 9.3 | Custom Prometheus pipeline metrics | 4-6 hrs | core-brain |
| 9.4 | Add circuit breakers (pybreaker) | 4-6 hrs | core-brain |
| 4.3 | Extract belief formation module | 4-8 hrs | meaning-engine |
| 2.2 | Per-TF Event Bus topics | 4-6 hrs | candle-constructor + event-bus |
| 6.1 | Multi-topic subscription format | 4-6 hrs | event-bus + shared |

**Subtotal: ~50 hours**

---

### TIER 3 — Deep Feature Work (3-5 Weeks)

Large items requiring significant engineering:

| ID | Gap | Time | Service |
|----|-----|------|---------|
| 3.2 | Real LTF cross-TF context (50D) | 2-3 days | perception + producer |
| 3.3 | Real HTF cross-TF context (50D) | 2-3 days | perception + producer |
| 4.1 | S/R detection, VWAP, round numbers | 1-2 days | meaning-engine |
| 4.2 | HH/HL detection in meaning-engine | 1 day | meaning-engine |
| 9.1 | 200ms pipeline budget enforcement | 2-3 days | core-brain + all |
| 9.2 | Event-driven decision trigger | 4-8 hrs | core-brain |
| 3.4 | Expand temporal history to 100D/100 | 4-8 hrs | perception |
| 2.3 | Parallel candle aggregation | 4-6 hrs | candle-constructor |
| 2.4 | Rolling window aggregation | 6-10 hrs | candle-constructor |

**Subtotal: ~128 hours**

---

### TIER 4 — Architecture Rethink (Decide, Don't Necessarily Implement)

| ID | Gap | Question to Answer |
|----|-----|-------------------|
| 3.1 | 6-group vs 4-group vector layout | Is the doc's 6-group layout actually better than the current clean 4×64D design? |
| 2.4 | Rolling vs bucket aggregation | Do downstream consumers actually need overlapping candles? |
| 2.3 | Parallel vs sequential aggregation | Is parallel faster for 13 simple arithmetic operations? Overhead may hurt. |
| 9.2 | Event-driven vs request/response | Request/response gives explicit control flow. Event-driven is harder to debug. |

These require design decisions before implementation.

---

## FINAL WORD

**35% of the architecture document is faithfully implemented. 35% exists in a different form. 30% is not implemented at all.**

The most impactful gap is the **cross-TF intelligence** (GAPs 3.2 + 3.3): 100 of the 256 vector dimensions are non-functional stubs. This means the "multi-timeframe fusion" that is the document's central thesis is architecturally present but **not actually flowing real data** between timeframes through the vector.

The decision pipeline is solid (10 steps, SHA-256 audit, confidence thresholds). The event mesh is more capable than documented (~65 subscriptions vs claimed 40+). The meaning pipeline runs all stages. These are real.

The question is whether to (a) update the document to match the code, (b) update the code to match the document, or (c) some mix of both. Several of the code's implementations are arguably **better** than what the doc describes (4×64D cleaner than 6-group variable-size, linear decay simpler than multiplicative, confidence-weighted denominator more robust).
