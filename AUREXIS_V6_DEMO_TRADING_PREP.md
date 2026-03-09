# AUREXIS V6 — Demo Trading Readiness Report

> Generated: $(date) | Session: V6 Comprehensive Upgrade

---

## 1. Executive Summary

AUREXIS is **read-only production-ready** for live market data. The Deriv WebSocket connector streams ticks, builds candles (M1→MN1), persists to ClickHouse, applies intelligent validation (spike/gap/spread/stale/market-hours), and uses checkpoint recovery across Docker restarts.

**Trading execution does NOT exist yet.** The core-brain produces `TradeAction.LONG/SHORT/WAIT` decisions, but there is no bridge from decision → Deriv broker execution. This report documents everything needed to close that gap.

---

## 2. Current State — What Works

| Component | Status | Details |
|---|---|---|
| Deriv WS Connection | ✅ LIVE | `wss://ws.derivws.com/websockets/v3?app_id=1089` |
| Authentication | ✅ Working | Token: `5QHG5pWqNmTlhuR`, Account: CR10211540 |
| Tick Streaming | ✅ Working | R_25, 1HZ25V, CRASH600, frxXAUUSD confirmed |
| Candle Aggregation | ✅ Working | All 11 TFs: M1,M2,M3,M5,M15,M30,H1,H4,D1,W1,MN1 |
| ClickHouse Persistence | ✅ Wired | Buffered batch inserts (100 ticks), candle-on-complete |
| Tick Intelligence | ✅ Active | 6 adaptive gates (spike, spread, stale, gap, market-hours, zero) |
| Checkpoint/Recovery | ✅ Active | Atomic JSON saves every 500 ticks |
| Event Bus Publishing | ✅ Working | `market.tick`, `market.candle.*` events |
| Decision Engine | ✅ Working | Core-brain outputs LONG/SHORT/WAIT decisions |
| **Trade Execution** | ❌ **Missing** | **No buy/sell code exists anywhere** |

---

## 3. Critical Safety Warning

> **⚠️ The current account (CR10211540) is a REAL-MONEY account.**
>
> Account prefix `CR` = "Cashier Real". Any `buy` message sent through this token would spend **real money**.
>
> **BEFORE ANY TRADING CODE IS WRITTEN:**
> 1. Create a VRTC (virtual/demo) account on app.deriv.com
> 2. Generate a new API token with **Trade** scope (current token may be read-only)
> 3. Add `DERIV_REQUIRE_VIRTUAL=true` safety guard
> 4. Test EXCLUSIVELY on the virtual account first

---

## 4. What Needs to Be Built

### Phase 1: Prerequisites (Before Writing Any Trading Code)
- [ ] Create Deriv VRTC demo account (app.deriv.com)
- [ ] Generate API token with `Trade` scope enabled
- [ ] Add `.env` vars: `DERIV_TRADE_TOKEN`, `DERIV_TRADE_ENABLED=false`, `DERIV_REQUIRE_VIRTUAL=true`
- [ ] Verify `is_virtual` flag from authorize response (hard-block if not virtual)

### Phase 2: Trading Connector (~500 lines)
New file: `market-ingestion/src/connectors/deriv_trade_connector.py`

| Function | Deriv API Message | Purpose |
|---|---|---|
| `get_contracts_for(symbol)` | `{"contracts_for": "R_25"}` | Discover contract types |
| `request_proposal(...)` | `{"proposal": 1, ...}` | Get live price quote |
| `buy_contract(proposal_id)` | `{"buy": "<id>", "price": N}` | Execute purchase |
| `sell_contract(contract_id)` | `{"sell": <id>, "price": 0}` | Exit early |
| `get_portfolio()` | `{"portfolio": 1}` | Open positions |
| `get_balance()` | `{"balance": 1, "subscribe": 1}` | Live balance |
| `get_profit_table()` | `{"profit_table": 1}` | Trade history |

### Phase 3: Execution Bridge (~300 lines)
Connect core-brain decisions to Deriv trading:

```
CoreBrain Decision → Event Bus (trade.signal) → TradeConnector → Deriv API
                                                       ↓
                                              Event Bus (trade.executed)
                                                       ↓
                                              ClickHouse persistence
```

### Phase 4: Risk Management (~200 lines)
- Virtual-only guard (assert `is_virtual == 1`)
- Max stake per trade ($1-$10 for demo)
- Daily loss limit (-$100 halt)
- Max concurrent positions (3)
- Rate limiting (5 proposals/sec max)
- Full audit logging through SecurityClient

---

## 5. Deriv Contract Types Available

### Synthetics (R_25, 1HZ25V, CRASH600) — 24/7
| Contract | Type | Duration |
|---|---|---|
| Rise/Fall | `CALL` / `PUT` | 1 tick to 365 days |
| Higher/Lower | `CALL` / `PUT` (barrier-based) | 5 ticks to 365 days |
| Touch/No Touch | `ONETOUCH` / `NOTOUCH` | 5 ticks to 365 days |
| Digit Match/Differ | `DIGITEVEN` / `DIGITODD` etc. | 1–10 ticks |

### Forex (frxXAUUSD) — Mon-Fri
| Contract | Type | Duration |
|---|---|---|
| Rise/Fall | `CALL` / `PUT` | 5 ticks to 365 days |
| Multipliers | `MULTUP` / `MULTDOWN` | Open-ended (SL/TP) |

### Recommended for Testing
**R_25 Rise/Fall** — simplest, 24/7 available, 1-minute duration, lowest risk.

---

## 6. Estimated Effort

| Phase | Lines | Time |
|---|---|---|
| Phase 1: Prerequisites | Config only | 30 min |
| Phase 2: Trading Connector | ~500 | 3-4 hours |
| Phase 3: Execution Bridge | ~300 | 2-3 hours |
| Phase 4: Risk Management | ~200 | 1-2 hours |
| Testing & Validation | — | 2-3 hours |
| **Total** | **~1000 lines** | **~10 hours** |

---

## 7. Quick-Start Demo Path

The fastest path to a working demo:

1. **Get VRTC account + trade token** (5 min)
2. **Add `request_proposal` + `buy` to existing connector** (extend `_message_loop` to handle 2 new msg types)
3. **Manual trigger via REST endpoint**: `POST /api/v1/trade/buy {"symbol": "R_25", "amount": 1, "duration": 1, "duration_unit": "m"}`
4. **Watch P&L via balance subscription**

This gets a working demo in ~2 hours without the full execution bridge.

---

## 8. V6 Session Deliverables Summary

All upgrades completed in this session:

| # | Feature | Status | Files Modified |
|---|---|---|---|
| 1 | Timeframes M1→MN1 (all 11) | ✅ | deriv_ws_connector.py, .env |
| 2 | ClickHouse streaming | ✅ | deriv_ws_connector.py, main.py |
| 3 | Checkpoint/recovery | ✅ | deriv_ws_connector.py (StreamCheckpoint) |
| 4 | Tick intelligence (6 gates) | ✅ | deriv_ws_connector.py (TickIntelligence) |
| 5 | Market hours awareness | ✅ | deriv_ws_connector.py |
| 6 | Calendar-aware buckets (W1/MN1) | ✅ | deriv_ws_connector.py |
| 7 | Dynamic weight consensus | ✅ | shared/adaptive_weights.py + 2 engines |
| 8 | Explanation fluency | ✅ | narrative_synthesizer.py + bundle |
| 9 | Skeleton mode (multi-TF, bias, EH/EL) | ✅ | SkeletonLayer.ts, WebGLRenderer.ts |
| 10 | Database & .env audit | ✅ | All 25 .env files reviewed |
| 11 | E2E test suite | ✅ | test_e2e_v6.py (99 endpoints) |
| 12 | Postman collections updated | ✅ | +3 adaptive weight, +3 market-ingestion |
| 13 | Demo trading prep | ✅ | This report |

**Total files created/modified: 13**  
**New Postman endpoints: 6**
