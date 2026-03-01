# PRICE OBSERVER - QUICK START

## What Changed

### VIOLATIONS REMOVED ❌→✅
- ~~Shape detection modules~~ → **DISABLED** (belongs in Perception/Shape Engine)
- ~~No time ordering~~ → **Time ordering validator added**
- ~~No anomaly events~~ → **Anomaly detector added**
- ~~No ontology validation~~ → **Ontology validator added**

### ENTERPRISE FEATURES ADDED ✅

1. **Monotonic Time Enforcement** - No out-of-order ticks, no future leakage
2. **Sequence Numbering** - Every event has deterministic sequence number
3. **Anomaly Detection** - Gap, latency, feed quality monitoring
4. **Ontology Validation** - All ticks validated against canonical concepts
5. **Deterministic Replay** - Same input → same output + sequence

---

## Usage

### Basic Tick Processing

```rust
use price_observer::observation::price_observer_enterprise::PriceObserver;

let observer = PriceObserver::new(config, event_bus);

let tick = json!({
    "instrument": "BTCUSD",
    "price": 50000.0,
    "volume": 1.5,
    "timestamp": "2024-01-01T12:00:00Z",
    "source": "exchange1"
});

let result = observer.process_tick(tick).await?;
// Result includes sequence number
```

### Events Emitted

**Normal Flow**:
1. Tick received → validated → sequenced
2. Candle aggregated → emitted with sequence
3. State forgotten

**Anomaly Flow**:
- Out-of-order tick → `OutOfOrderDetected` event
- Gap detected → `GapDetected` event
- High latency → `LatencyViolationDetected` event
- Duplicate tick → `FeedAnomalyDetected` event

### Statistics

```rust
let stats = observer.get_stats().await;

println!("Processed: {}", stats.total_ticks_processed);
println!("Sequence: {}", stats.current_sequence);
println!("Violations: {}", stats.time_violations);
println!("Anomalies: {}", stats.anomalies_detected);
```

---

## API Changes

### PriceEvent (Output)

**NEW FIELD**:
```rust
pub struct PriceEvent {
    // ... existing fields ...
    pub sequence: Option<u64>,  // ← NEW
}
```

### ObserverStats

**NEW FIELDS**:
```rust
pub struct ObserverStats {
    // ... existing fields ...
    pub current_sequence: u64,              // ← NEW
    pub time_violations: u64,               // ← NEW
    pub anomalies_detected: u64,            // ← NEW
    pub ontology_validation_failures: u64,  // ← NEW
}
```

### Config

**NEW FIELD**:
```rust
pub struct Config {
    // ... existing fields ...
    pub ontology_endpoint: Option<String>,  // ← NEW
}
```

**ENV VAR**: `ONTOLOGY_ENDPOINT=http://ontology:8080`

---

## Event Types

### 1. CandleClose (Primary Output)
```json
{
  "event_type": "CANDLE_CLOSE",
  "instrument": "BTCUSD",
  "timeframe": "5M",
  "open": 50000.0,
  "high": 50100.0,
  "low": 49900.0,
  "close": 50050.0,
  "volume": 1234.56,
  "timestamp": "2024-01-01T12:00:00Z",
  "source": "exchange1",
  "sequence": 12345
}
```

### 2. OutOfOrderDetected (Time Violation)
```json
{
  "sequence": 12346,
  "timestamp": "2024-01-01T11:59:00Z",
  "violation_type": "OutOfOrder",
  "message": "Timestamp is before last timestamp"
}
```

### 3. GapDetected (Missing Ticks)
```json
{
  "instrument": "BTCUSD",
  "timeframe": "5M",
  "gap_start": "2024-01-01T12:00:00Z",
  "gap_end": "2024-01-01T12:05:00Z",
  "expected_ticks": 300,
  "actual_ticks": 0,
  "severity": "Major"
}
```

### 4. LatencyViolationDetected (Slow Feed)
```json
{
  "instrument": "BTCUSD",
  "source": "exchange1",
  "event_time": "2024-01-01T12:00:00Z",
  "receipt_time": "2024-01-01T12:00:05Z",
  "latency_ms": 5000,
  "threshold_ms": 1000,
  "severity": "Major"
}
```

### 5. FeedAnomalyDetected (Quality Issue)
```json
{
  "instrument": "BTCUSD",
  "source": "exchange1",
  "anomaly_type": "DuplicateTick",
  "timestamp": "2024-01-01T12:00:00Z",
  "details": "Duplicate tick detected",
  "severity": "Minor"
}
```

---

## Migration

### From Legacy

**BEFORE**:
```rust
use price_observer::observation::price_observer::PriceObserver;
```

**AFTER**:
```rust
use price_observer::observation::price_observer_enterprise::PriceObserver;
```

**That's it!** Same API, enhanced behavior.

---

## Testing

Run all tests:
```bash
cargo test
```

Specific module tests:
```bash
cargo test time_ordering
cargo test anomaly
cargo test ontology
```

---

## Monitoring

### Key Metrics

- `price_observer.ticks_processed` - Total ticks processed
- `price_observer.candles_emitted` - Total candles emitted
- `price_observer.current_sequence` - Current sequence number
- `price_observer.time_violations` - Out-of-order rejections
- `price_observer.anomalies_detected` - Feed quality issues
- `price_observer.processing_time_us` - Average latency

### Alerts

**CRITICAL**:
- Time violations > 0 (out-of-order data)
- Ontology validation failures > 0 (invalid instruments)

**WARNING**:
- Latency violations > 10/min (slow feed)
- Gaps detected > 5/min (missing data)

**INFO**:
- Feed anomalies (duplicates, stale data)

---

## FAQ

**Q: Why were shape detection modules disabled?**  
A: Price Observer is sensory only. Shape detection is interpretation, which belongs in Perception/Shape Engine. "The eye sees. The eye does not interpret."

**Q: What's the sequence number for?**  
A: Deterministic replay. Given same input stream, output events will have same sequence numbers. Critical for legal defense and audit trails.

**Q: Will old events break?**  
A: No. `sequence` field is optional (`Option<u64>`). Old consumers can ignore it.

**Q: Why validate against ontology?**  
A: Ontology defines canonical concepts (what a "price" is, what a "timeframe" is). Price Observer must conform to these definitions to prevent hallucination.

**Q: What happens if ontology is down?**  
A: Ticks are rejected with `OntologyValidationError`. Feed will pause until ontology recovers. Better to pause than hallucinate.

---

## Constitutional Guarantee

✅ **Price Observer observes. It does not think.**

- Accurate
- Deterministic  
- Time-correct
- Non-opinionated
- Audit-safe
- Ephemeral

**If Price Observer lies, the entire system hallucinates.**

---

## Files Created/Modified

**NEW**:
- `src/time_ordering/mod.rs` - Monotonic time enforcement
- `src/anomaly/mod.rs` - Anomaly module
- `src/anomaly/detector.rs` - Gap/latency/feed detection
- `src/ontology/mod.rs` - Ontology module
- `src/ontology/validator.rs` - Concept validation
- `src/observation/price_observer_enterprise.rs` - Enterprise implementation
- `ENTERPRISE_IMPLEMENTATION.md` - This documentation

**MODIFIED**:
- `src/lib.rs` - Disabled violation modules, added enterprise exports
- `src/models/mod.rs` - Added enterprise stats fields
- `src/models/price_event.rs` - Added sequence field
- `src/config/config.rs` - Added ontology_endpoint field

---

## Support

Issues? Check:
1. Ontology service is running (`ONTOLOGY_ENDPOINT`)
2. Event bus is accessible (`EVENT_BUS_URL`)
3. Timeframes are canonical (1M, 5M, 15M, 1H, 4H, 1D)
4. Timestamps are not in the future

Logs will show:
- `✅ ENTERPRISE Price Observer initialized` - Startup success
- `📊 Received tick` - Tick processing
- `📤 Emitted candle [seq=...]` - Candle emission
- `🚨 Anomaly detected` - Quality issues
- `⏰ Time ordering violation` - Out-of-order data
