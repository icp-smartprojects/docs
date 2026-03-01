# Candle Constructor - Quick Start Guide

## 🚀 30-Second Startup

```bash
# 1. Navigate to service
cd /home/m8575/Meaning_X/AUREXIS/candle-constructor

# 2. Run unit tests (verify installation)
python -m pytest tests/unit/ -v

# 3. Process market data
python src/main.py --dir ../market-ingestion/data --limit 1000

# 4. Check results
tail -f .logs/candle_constructor.log
```

## 📋 What It Does

```
CSV Market Data (ticks)
         ↓
   Parse with CSVLoader
         ↓
Aggregate to all timeframes (1s→1M)
         ↓
Create OHLC candles with verification hash
         ↓
Publish to Event Bus
         ↓
Perception Engine consumes events
```

## 🔧 Common Commands

### Process single asset
```bash
python src/main.py --file ../market-ingestion/data/BTC/1m.csv --limit 100
```

### Process all assets with limit
```bash
python src/main.py --dir ../market-ingestion/data --limit 5000
```

### Run equivalence tests
```bash
python src/main.py --mode validate --dir ../market-ingestion/data
```

### Run unit tests
```bash
pytest tests/unit/ -v
# or
python src/main.py --mode test
```

## 📊 Expected Output

```
[2026-01-14T10:40:35] [INFO   ] Starting Candle Constructor
[2026-01-14T10:40:35] [INFO   ] Processing: ../market-ingestion/data/Volatility 10 Index/1m.csv
[2026-01-14T10:40:35] [INFO   ] [Process Volatility 10 Index] completed in 245.32ms

=== Aggregation Summary ===
Candles created:  450
Candles failed:   0
Ticks processed:  1000
Errors:           0
```

## 🎯 What Gets Created

- ✅ 10 timeframes of OHLC candles per asset
- ✅ SHA256 verification hash per candle
- ✅ Events published to Event Bus
- ✅ Logs written to `.logs/candle_constructor.log`
- ✅ No raw data stored (only aggregated candles)

## 🔍 Verify It Works

```bash
# Check logs
cat .logs/candle_constructor.log | head -20

# Run quick test
python -m pytest tests/unit/test_aggregator.py::TestCandle -v

# Check event schema
grep "OHLC_AGGREGATED" src/models/event_schema.py
```

## 📦 Installation Check

```bash
# Verify dependencies
pip list | grep -E "pytest|requests|dataclasses"

# Should show:
# dataclasses-json
# pytest
# requests

# If missing, install:
pip install -r requirements.txt
```

## 🚨 Troubleshooting

### Event Bus not available
```
Warning: Event Bus not available at http://localhost:8080
→ Service continues anyway (fail-silent design)
→ Check event-bus is running: ./hedge start event-bus
```

### CSV parsing errors
```
Warning: Skipping malformed row X
→ Service skips bad rows and continues
→ Check CSV format: head -5 data.csv
```

### Memory issues
```
ROW_LIMIT=100 python src/main.py --dir ../market-ingestion/data
→ Process in smaller batches
→ Streaming design handles large files
```

## ✅ Success Criteria

You know it's working when:

1. ✅ Tests pass: `pytest tests/unit/ -v` → 10/10 PASSED
2. ✅ Data processed: Output shows `Candles created: N`
3. ✅ No errors: Check `.logs/candle_constructor.log`
4. ✅ Deterministic: Running twice produces same candles
5. ✅ Hashes valid: SHA256 hashes included in events

## 🎓 Next Steps

1. **Integration**: Start the full system with `./hedge start`
2. **Monitoring**: Watch Event Bus for `OHLC_AGGREGATED` events
3. **Validation**: Run `./hedge validate` to check all services
4. **Learning**: Study the code in `src/aggregation/aggregator.py`

---

**That's it!** The Candle Constructor is production-ready and autonomous.

For detailed documentation, see:
- `README.md` - Complete reference
- `IMPLEMENTATION_SUMMARY.md` - Architecture details
- `VERIFICATION_REPORT.txt` - Quality assurance

