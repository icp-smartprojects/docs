# AUREXIS Event Bus - The Nervous System

## Overview

The Event Bus is the **nervous system** of AUREXIS. It is **not** a brain, not a database, not a processor—it is pure **signal transport**.

Every meaningful action in AUREXIS flows through events. No service talks to another service directly. No state is queried. Only events.

## Core Philosophy

### What the Event Bus IS
- **Signal Transport**: Takes events, timestamps them, routes them
- **Decoupler**: Services don't know about each other
- **Time Keeper**: Events establish causality and order
- **Observable**: Every action becomes a traceable signal

### What the Event Bus is NOT
- ❌ A database (events are transient by default)
- ❌ A processor (no logic here)
- ❌ A workflow engine (no decisions)
- ❌ A brain (no intelligence)

## The Golden Rule

> **If something didn't happen as an event, it didn't happen at all.**

No side effects. No hidden state. No silent knowledge. Everything is observable.

## Event Layers

Events flow through 6 layers:

### 1. External Layer
**Source**: Outside the system (market data, user commands)
- `PriceObserved` - Market tick
- `CandleClosed` - Candle completed
- `SystemClock` - Time signal
- `UserCommand` - Human input

### 2. Perceptual Layer
**Source**: Perception engine (price-observer, perception)
- `StructureDetected` - Market structure found
- `VolatilityShift` - Volatility change
- `RangeDetected` - Price range identified
- `PatternMatched` - Pattern recognized

### 3. Cognitive Layer
**Source**: Meaning engine, Reasoning engine
- `HypothesisGenerated` - Hypothesis formed
- `ScenarioActivated` - Scenario triggered
- `PlanProposed` - Plan created
- `InterpretationMade` - Meaning assigned

### 4. Decision Layer
**Source**: Core brain, Reasoning engine
- `DecisionCommitted` - Decision made
- `EntrySignalFired` - Enter signal
- `ExitSignalFired` - Exit signal
- `HoldDecided` - Hold position

### 5. Outcome Layer
**Source**: Market, Execution
- `OutcomeObserved` - Trade result
- `TradeFilledFull` - Complete fill
- `StopHit` - Stop loss hit
- `TargetHit` - Target reached
- `TimeoutExceeded` - Position timed out

### 6. Learning Layer
**Source**: Learning engine
- `RewardIssued` - Reward signal
- `PenaltyIssued` - Punishment signal
- `BeliefUpdated` - Belief changed
- `PatternLearned` - Pattern discovered

## Event Flow Through AUREXIS

```
Market Ticks
    ↓
[Price Observer] → PriceObserved events
    ↓
[Perception] → StructureDetected events
    ↓
[Meaning Engine] → HypothesisGenerated events
    ↓
[Reasoning Engine] → DecisionCommitted events
    ↓
[Execution Engine] → OrderExecuted
    ↓
[Market] → OutcomeObserved
    ↓
[Learning Engine] → RewardIssued/PenaltyIssued
    ↓
[Memory] - Listening to ALL of the above
```

## Who Publishes, Who Listens

### Publishers
- **Price Observer**: Market data → `PriceObserved`, `CandleClosed`
- **Perception**: Structures → `StructureDetected`
- **Meaning Engine**: Interpretations → `HypothesisGenerated`
- **Reasoning Engine**: Plans → `PlanProposed`, `DecisionCommitted`
- **Execution Engine**: Orders → Trade outcomes
- **Learning Engine**: Reward/penalty → `RewardIssued`, `PenaltyIssued`

### Listeners
- **Memory**: Listens to EVERYTHING important
  - Extracts meaning
  - Stores compressed traces
  - Forgets raw events
- **Learning Engine**: Listens to outcomes
  - Calculates reward
  - Updates beliefs
  - Improves future decisions
- **Explanation Engine**: Listens to all events
  - Builds causal chains
  - Explains decisions
- **Observability**: Listens for metrics
- **Frontend**: Read-only listening

## Topics in AUREXIS

### External Topics
- `price.observations` - Price ticks
- `candles` - Closed candles
- `system.clock` - Clock ticks
- `user.commands` - User input

### Perceptual Topics
- `structures.detected` - Structures found
- `volatility.shifts` - Volatility changes
- `range.detections` - Ranges identified
- `pattern.matches` - Patterns found

### Cognitive Topics
- `hypotheses` - Hypotheses generated
- `scenarios` - Scenarios activated
- `plans` - Plans proposed
- `interpretations` - Interpretations made

### Decision Topics
- `decisions` - Decisions committed
- `entry.signals` - Entry signals
- `exit.signals` - Exit signals
- `hold.signals` - Hold signals

### Outcome Topics
- `trade.outcomes` - All trade outcomes
- `fills` - Trade fills
- `stops` - Stops hit
- `targets` - Targets hit

### Learning Topics
- `rewards` - Rewards issued
- `penalties` - Penalties issued
- `belief.updates` - Belief updates

## Event Structure

Every event in AUREXIS has this structure:

```go
{
  "event_id": "unique-id",
  "event_type": "price.observed",
  "layer": "external",
  "timestamp": "2026-01-13T19:17:46Z",
  "sequence": 12345,
  "source": "price-observer",
  "service_id": "po-1",
  "trace_id": "trace-123",
  "span_id": "span-456",
  "parent_id": "event-111",
  "correlation_id": "corr-789",
  "payload": { ... },
  "metadata": { ... },
  "schema_version": "1.0.0",
  "partition_key": "EUR/USD",
  "ordering_key": "EUR/USD:M5",
  "ttl": "5m",
  "persistent": false
}
```

### Key Fields

- **event_id**: Unique identifier (auto-generated)
- **event_type**: What happened (enum)
- **layer**: Which layer produced it (external, perceptual, etc.)
- **timestamp**: When it happened (UTC)
- **sequence**: Monotonic ordering number
- **source**: Service that produced it
- **parent_id**: The event that caused this
- **correlation_id**: Groups related events
- **payload**: Event-specific data
- **partition_key**: For ordered delivery (e.g., symbol)
- **ttl**: How long to keep the event

## Guarantees

The Event Bus provides:

### 1. Ordering Guarantee
Events for the same partition key arrive in order.
```
EUR/USD events arrive 1, 2, 3, 4, 5 (never 2, 1, 3)
GBP/USD events arrive independently 1, 2, 3, 4 (never interleaved)
```

### 2. Durability (Optional)
In study/training mode, events are persisted temporarily.
In live mode, events are transient.

### 3. Decoupling
Publishers don't know who's listening.
Listeners don't know who's publishing.
Only the Event Bus knows.

### 4. Time Awareness
Every event is timestamped.
Every event has a sequence number.
Causality is preserved.

## Persistence Modes

### Live Mode (Default)
- Events are transient
- Consumed once
- Forgotten immediately after distribution
- No storage overhead
- Maximum speed

### Study/Training Mode
- Events temporarily persisted
- Replayable for learning
- Deleted after learning stabilizes
- Optional storage
- Learning focused

## No Logic Rule

The Event Bus does ONLY these things:

1. **Receive** events
2. **Timestamp** them
3. **Validate** them
4. **Route** them to subscribers
5. **Guarantee** order (per partition)
6. **Optionally persist** temporarily

It does NOT:
- ❌ Transform events (that's Consumer's job)
- ❌ Filter by intelligence (that's Consumer's job)
- ❌ Enrich events (that's Consumer's job)
- ❌ Make decisions (that's brain's job)
- ❌ Store data (that's Memory's job)

## Failure Behavior

If a service crashes:
- ✅ Events keep flowing
- ✅ No global failure
- ✅ Memory still accumulates
- ✅ Learning still sees outcomes
- ✅ Other services keep running

Failures are **isolated**, not **cascading**.

## How to Use

### Publishing an Event

```go
event := &Event{
    EventType: "price.observed",
    Layer: "external",
    Source: "price-observer",
    Topic: "price.observations",
    Payload: map[string]interface{}{
        "symbol": "EUR/USD",
        "price": 1.0950,
        "timeframe": "M5",
    },
    PartitionKey: "EUR/USD",
    OrderingKey: "EUR/USD:M5",
}

publisher.Publish(ctx, event)
```

### Subscribing to Events

```go
subscriber.Subscribe(ctx, "structures.detected", func(event *Event) {
    // Process structure
    // Don't call other services directly
    // Emit your own events instead
    
    // WRONG: orderService.CreateOrder(...)
    // RIGHT: publisher.Publish(ctx, decisionEvent)
})
```

## Architecture Principles

1. **Forward Flow Only**
   - Events flow forward in time
   - Never circular
   - Acyclic graph

2. **No Direct Calls**
   - Services never call each other
   - All communication through events
   - This enables true independence

3. **Memory Listening**
   - Memory listens to important events
   - Extracts patterns
   - Compresses traces
   - Forgets raw data

4. **Punishment and Reward**
   - Learning engine issues rewards/penalties
   - Beliefs updated via events
   - Future decisions affected
   - All observable

5. **Time Awareness**
   - Every event has timestamp
   - Sequence maintained
   - Causality traceable
   - Dreams (simulations) replayable

## Example: A Complete Flow

```
1. Market tick arrives → PriceObserved event
   source: price-observer
   
2. Perception sees price → StructureDetected event
   source: perception
   parent_id: (PriceObserved)
   
3. Meaning engine sees structure → HypothesisGenerated event
   source: meaning-engine
   parent_id: (StructureDetected)
   
4. Reasoning engine sees hypothesis → DecisionCommitted event
   source: reasoning-engine
   parent_id: (HypothesisGenerated)
   
5. Execution sees decision → Trade fills → OutcomeObserved event
   source: execution-engine
   parent_id: (DecisionCommitted)
   
6. Learning engine sees outcome → RewardIssued event
   source: learning-engine
   parent_id: (OutcomeObserved)
   
7. Memory sees all of these → Updates internal state
   (Doesn't update beliefs—that's learning engine's job)
```

## Observability

Every event is observable:
- Trace ID: Follow across services
- Span ID: Identify the action
- Parent ID: See what caused it
- Correlation ID: Group related events
- Timestamp: Know when it happened
- Sequence: Know the order

## Summary

> **The Event Bus is how AUREXIS experiences time without confusion.**

It enables:
- ✅ Time awareness
- ✅ Consequence tracking
- ✅ Clean punishment loops
- ✅ Replayable dreams
- ✅ Truthful explanations
- ✅ Independent services
- ✅ Isolated failures
- ✅ Real learning

Without it, intelligence is theatre.
