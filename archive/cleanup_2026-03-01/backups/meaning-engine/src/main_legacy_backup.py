"""
Meaning Engine - FastAPI Application

Main application entry point providing REST API for semantic extraction.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional, List, Tuple
import structlog
import asyncio
import json
import os
from datetime import datetime, timezone
import hashlib
import uuid

from .config.config import settings
from .utils.logger import configure_logging
from .extraction import MeaningExtractor
from .models import Concept, Meaning
from .graph.belief_graph import BeliefGraph, BiasState, StructureState
from .models.decision_model import MeaningDecision, DecisionAction
from .utils.enterprise_decision_engine import EnterpriseDecisionEngine


# Configure logging
configure_logging(settings.LOG_LEVEL)
logger = structlog.get_logger(__name__)


# FastAPI app
app = FastAPI(
    title="Meaning Engine",
    description="Semantic intelligence infrastructure",
    version="1.0.0"
)


# CORS
_cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:80,http://localhost:3001").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response models
class ExtractionRequest(BaseModel):
    input_text: str
    context: Optional[Dict[str, Any]] = None


class ExtractionResponse(BaseModel):
    meaning_id: str
    primary_interpretation: str
    concepts: List[Dict[str, Any]]
    beliefs: List[Dict[str, Any]]
    overall_confidence: float


# Initialize extractor
extractor = MeaningExtractor()

# Initialize enterprise decision engine
enterprise_engine = None  # Will be initialized on startup

# Service URLs
EVENT_BUS_URL = os.getenv("EVENT_BUS_URL", "http://localhost:52020").rstrip("/")
PERCEPTION_URL = os.getenv("PERCEPTION_URL", "http://localhost:52012").rstrip("/")
SHAPE_ENGINE_URL = os.getenv("SHAPE_ENGINE_URL", "http://localhost:52010").rstrip("/")
MEMORY_URL = os.getenv("MEMORY_URL", "http://localhost:52018").rstrip("/")
POLICY_ENGINE_URL = os.getenv("POLICY_ENGINE_URL", "http://localhost:52032").rstrip("/")
ONTOLOGY_URL = os.getenv("ONTOLOGY_URL", "http://localhost:52100").rstrip("/")

MEANING_EVENT_TOPICS = [
    t.strip() for t in os.getenv(
        "MEANING_EVENT_TOPICS",
        "perception.events,shape_created,shape_updated,shape_invalidated,shape_confirmed,shape_touched,shape_expired,shape_vector_emitted,shape_learn_requested,shape_feedback_received,shape_deduplicated,learning.calibration",
    ).split(",") if t.strip()
]
MEANING_PUBLISH_ENABLED = os.getenv("MEANING_PUBLISH_ENABLED", "true").lower() in ("1", "true", "yes")
MEANING_PUBLISH_TOPIC = os.getenv("MEANING_PUBLISH_TOPIC", "meaning.state")
MEANING_DECISION_PUBLISH_ENABLED = os.getenv("MEANING_DECISION_PUBLISH_ENABLED", "true").lower() in ("1", "true", "yes")
MEANING_DECISION_TOPIC = os.getenv("MEANING_DECISION_TOPIC", "meaning.decisions")
MEANING_EVENT_HISTORY_SIZE = int(os.getenv("MEANING_EVENT_HISTORY_SIZE", "200"))
MEANING_POLICY_STRATEGY = os.getenv("MEANING_POLICY_STRATEGY", "intraday")

TF_ORDER = [
    "S1", "S2",
    "M1", "M2", "M3", "M5", "M15", "M30",
    "H1", "H4",
    "D1",
]
TF_AUTHORITY = {tf: idx + 1 for idx, tf in enumerate(TF_ORDER)}


def _normalize_timeframe(tf: Optional[str]) -> Optional[str]:
    if not tf:
        return None
    s = str(tf).strip().upper().replace(" ", "")
    if s in TF_AUTHORITY:
        return s
    # Handle 1M/5M/1H etc
    import re
    m = re.match(r"^(\d+)([SMHDW])$", s)
    if m:
        return f"{m.group(2)}{m.group(1)}"
    m = re.match(r"^([SMHDW])(\d+)$", s)
    if m:
        return f"{m.group(1)}{m.group(2)}"
    if s == "DAILY":
        return "D1"
    if s == "WEEKLY":
        return "W1"
    return s


def _as_of_ts(value: Optional[str]) -> datetime:
    if not value:
        return datetime.now(timezone.utc)
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return datetime.now(timezone.utc)


def _bias_from_text(text: str) -> Optional[str]:
    t = text.lower()
    if "bull" in t or "long" in t or "uptrend" in t or "buy" in t:
        return "bullish"
    if "bear" in t or "short" in t or "downtrend" in t or "sell" in t:
        return "bearish"
    return None


def _infer_bias(event_type: str, payload: Dict[str, Any]) -> str:
    for key in ("bias", "direction", "trend", "side"):
        val = payload.get(key)
        if isinstance(val, str):
            b = _bias_from_text(val)
            if b:
                return b
    b = _bias_from_text(event_type or "")
    return b or "neutral"


def _extract_event(data: Dict[str, Any], topic: str) -> Dict[str, Any]:
    payload = data.get("payload") if isinstance(data, dict) else {}
    if payload is None and isinstance(data, dict):
        payload = data
    payload = payload or {}

    event_type = payload.get("event_type") or data.get("event_type") or data.get("topic") or topic
    event_id = payload.get("event_id") or data.get("event_id") or payload.get("id")
    symbol = payload.get("symbol") or payload.get("instrument") or payload.get("ticker") or payload.get("asset")
    timeframe = _normalize_timeframe(payload.get("timeframe") or payload.get("tf"))
    timestamp = payload.get("timestamp") or data.get("timestamp") or datetime.now(timezone.utc).isoformat()
    confidence = payload.get("confidence")
    if confidence is None:
        confidence = payload.get("strength", 0.5)
    try:
        confidence = float(confidence)
    except Exception:
        confidence = 0.5
    bias = _infer_bias(event_type or "", payload)
    shape_id = payload.get("shape_id") or payload.get("shapeId") or (payload.get("shape") or {}).get("id")
    return {
        "event_id": event_id,
        "event_type": event_type,
        "topic": topic,
        "symbol": symbol,
        "timeframe": timeframe,
        "timestamp": timestamp,
        "confidence": max(0.0, min(1.0, confidence)),
        "bias": bias,
        "shape_id": shape_id,
        "payload": payload,
    }


def _event_signature(event: Dict[str, Any]) -> str:
    base = {
        "event_type": event.get("event_type"),
        "symbol": event.get("symbol"),
        "timeframe": event.get("timeframe"),
        "timestamp": event.get("timestamp"),
        "bias": event.get("bias"),
        "shape_id": event.get("shape_id"),
    }
    return hashlib.sha256(json.dumps(base, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def _ensure_symbol_state(state: Dict[str, Any], symbol: str) -> Dict[str, Any]:
    symbols = state.setdefault("symbols", {})
    if symbol not in symbols:
        symbols[symbol] = {
            "timeframes": {},
            "events": [],
            "shapes": {},
            "last_updated": datetime.now(timezone.utc).isoformat(),
        }
    return symbols[symbol]


def _update_state_with_event(state: Dict[str, Any], event: Dict[str, Any]) -> None:
    symbol = event.get("symbol")
    if not symbol:
        return
    symbol_state = _ensure_symbol_state(state, symbol)
    tf = event.get("timeframe") or "UNKNOWN"
    tf_state = symbol_state["timeframes"].setdefault(tf, {"events": [], "last_event": None})

    event["signature"] = _event_signature(event)
    tf_state["events"].append(event)
    if len(tf_state["events"]) > MEANING_EVENT_HISTORY_SIZE:
        tf_state["events"] = tf_state["events"][-MEANING_EVENT_HISTORY_SIZE:]
    tf_state["last_event"] = event

    symbol_state["events"].append(event)
    if len(symbol_state["events"]) > MEANING_EVENT_HISTORY_SIZE:
        symbol_state["events"] = symbol_state["events"][-MEANING_EVENT_HISTORY_SIZE:]
    symbol_state["last_updated"] = datetime.now(timezone.utc).isoformat()


async def _consume_topic(app: FastAPI, topic: str) -> None:
    """Consume SSE stream from event-bus and update meaning state."""
    import httpx

    url = f"{EVENT_BUS_URL}/api/v1/stream"
    params = {"topic": topic}
    client: httpx.AsyncClient = app.state.event_bus_client

    while not app.state.stop_event.is_set():
        try:
            async with client.stream("GET", url, params=params) as resp:
                if resp.status_code != 200:
                    await asyncio.sleep(1.0)
                    continue
                async for line in resp.aiter_lines():
                    if app.state.stop_event.is_set():
                        break
                    if not line or not line.startswith("data:"):
                        continue
                    raw = line.replace("data:", "", 1).strip()
                    try:
                        data = json.loads(raw)
                        payload = data.get("payload") if isinstance(data, dict) else data
                        state = app.state.meaning_state
                        state["counts"][topic] = state["counts"].get(topic, 0) + 1
                        state["last_event"] = {
                            "topic": topic,
                            "received_at": datetime.utcnow().isoformat(),
                            "payload": payload,
                        }
                        state["last_by_topic"][topic] = state["last_event"]

                        event = _extract_event(data, topic)
                        async with app.state.state_lock:
                            _update_state_with_event(state, event)
                        
                        # Ingest into enterprise engine
                        engine = getattr(app.state, "enterprise_engine", None)
                        if engine:
                            try:
                                if topic == "learning.calibration":
                                    # Feedback loop: apply calibration from learning-engine
                                    cal_payload = payload if isinstance(payload, dict) else {}
                                    version = cal_payload.get("version", "?")
                                    app.state.meaning_state["learning_calibration"] = cal_payload
                                    logger.info(
                                        "Applied learning calibration feedback",
                                        version=version,
                                        shape_types=len(cal_payload.get("by_shape_type", {})),
                                        timeframes=len(cal_payload.get("by_timeframe", {})),
                                    )
                                elif "perception" in topic.lower() or "bos" in topic.lower() or "choch" in topic.lower():
                                    await engine.ingest_perception_event(event)
                                elif "shape" in topic.lower():
                                    await engine.ingest_shape_event(event)
                            except Exception as exc:
                                logger.warning("enterprise_engine_ingest_failed", error=str(exc))

                        if MEANING_PUBLISH_ENABLED:
                            await _publish_meaning_state(app, topic, payload)
                    except Exception as exc:
                        logger.warning("event_bus_parse_failed", error=str(exc), topic=topic)
        except asyncio.CancelledError:
            break
        except Exception as exc:
            logger.warning("event_bus_stream_error", error=str(exc), topic=topic)
            await asyncio.sleep(1.0)


async def _publish_meaning_state(app: FastAPI, source_topic: str, payload: Dict[str, Any]) -> None:
    """Publish a compact meaning-state snapshot to the event bus."""
    try:
        import uuid as _uuid
        event_id = str(_uuid.uuid4())
        client: httpx.AsyncClient = app.state.event_bus_client
        await client.post(
            f"{EVENT_BUS_URL}/api/v1/publish",
            json={
                "topic": MEANING_PUBLISH_TOPIC,
                "event_type": "MEANING_STATE",
                "source": "meaning-engine",
                "timestamp": datetime.utcnow().isoformat(),
                "correlation_id": payload.get("correlation_id", event_id),
                "causation_id": payload.get("causation_id", ""),
                "schema_version": "1.0.0",
                "payload": {
                    "source_topic": source_topic,
                    "received_at": datetime.utcnow().isoformat(),
                    "payload": payload,
                },
                "headers": {"source_service": "meaning-engine"},
            },
        )
    except Exception as exc:
        logger.warning("meaning_publish_failed", error=str(exc))


async def _publish_meaning_decision(app: FastAPI, decision: Dict[str, Any]) -> None:
    if not MEANING_DECISION_PUBLISH_ENABLED:
        return
    try:
        import uuid as _uuid
        event_id = str(_uuid.uuid4())
        client = app.state.event_bus_client
        await client.post(
            f"{EVENT_BUS_URL}/api/v1/publish",
            json={
                "topic": MEANING_DECISION_TOPIC,
                "event_type": "MEANING_DECISION",
                "source": "meaning-engine",
                "timestamp": datetime.utcnow().isoformat(),
                "correlation_id": decision.get("trace_id", event_id),
                "causation_id": decision.get("causation_id", ""),
                "schema_version": "1.0.0",
                "payload": decision,
                "headers": {"source_service": "meaning-engine"},
            },
        )
    except Exception as exc:
        logger.warning("meaning_decision_publish_failed", error=str(exc))


async def _publish_to_memory(app: FastAPI, decision: Dict[str, Any]) -> None:
    if not MEMORY_URL:
        return
    try:
        client = app.state.event_bus_client
        await client.post(
            f"{MEMORY_URL}/api/v1/memory/events",
            json={
                "event_type": "MEANING_DECISION",
                "payload": decision,
                "source_service": "meaning-engine",
                "correlation_id": decision.get("trace_id"),
                "decision_id": decision.get("decision_id"),
                "symbol": decision.get("symbol"),
                "timeframe": decision.get("execution_timeframe"),
                "confidence": decision.get("confidence"),
            },
        )
    except Exception as exc:
        logger.warning("memory_publish_failed", error=str(exc))


@app.on_event("startup")
async def _startup_event_bus():
    import httpx

    app.state.event_bus_client = httpx.AsyncClient(timeout=None)
    app.state.stop_event = asyncio.Event()
    app.state.state_lock = asyncio.Lock()
    app.state.meaning_state = {
        "counts": {},
        "last_event": None,
        "last_by_topic": {},
        "symbols": {},
        "decisions": {},
    }
    app.state.event_tasks = [
        asyncio.create_task(_consume_topic(app, topic)) for topic in MEANING_EVENT_TOPICS
    ]
    
    # Initialize enterprise decision engine
    global enterprise_engine
    enterprise_engine = EnterpriseDecisionEngine(
        event_bus_url=EVENT_BUS_URL,
        perception_url=PERCEPTION_URL,
        shape_engine_url=SHAPE_ENGINE_URL,
        memory_url=MEMORY_URL,
        policy_engine_url=POLICY_ENGINE_URL,
        ontology_url=ONTOLOGY_URL,
    )
    app.state.enterprise_engine = enterprise_engine
    
    logger.info("Meaning Engine started with enterprise decision engine")


@app.on_event("shutdown")
async def _shutdown_event_bus():
    app.state.stop_event.set()
    for task in getattr(app.state, "event_tasks", []):
        task.cancel()
    await asyncio.gather(*getattr(app.state, "event_tasks", []), return_exceptions=True)
    client = getattr(app.state, "event_bus_client", None)
    if client:
        await client.aclose()


@app.get("/")
async def root():
    return {"service": "meaning-engine", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "meaning-engine",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "symbols_tracked": len(app.state.meaning_state.get("symbols", {})),
    }


@app.get("/health/live")
async def liveness():
    return {"status": "alive"}


@app.get("/health/ready")
async def readiness():
    # Check event-bus availability if configured
    checks = {}
    try:
        import httpx
        async with httpx.AsyncClient(timeout=2.0) as client:
            resp = await client.get(f"{EVENT_BUS_URL}/health")
            checks["event_bus"] = resp.status_code < 500
    except Exception:
        checks["event_bus"] = False
    # Optional upstream checks
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            if SHAPE_ENGINE_URL:
                resp = await client.get(f"{SHAPE_ENGINE_URL}/health")
                checks["shape_engine"] = resp.status_code < 500
            if POLICY_ENGINE_URL:
                resp = await client.get(f"{POLICY_ENGINE_URL}/ready")
                checks["policy_engine"] = resp.status_code < 500
            if MEMORY_URL:
                resp = await client.get(f"{MEMORY_URL}/ready")
                checks["memory"] = resp.status_code < 500
            if ONTOLOGY_URL:
                resp = await client.get(f"{ONTOLOGY_URL}/api/v1/ready")
                checks["ontology"] = resp.status_code < 500
    except Exception:
        pass

    ready = all(checks.values()) if checks else True
    if not ready:
        return {"status": "degraded", "checks": checks}
    return {"status": "ready", "checks": checks}


@app.get("/ready")
async def readiness_alias():
    """Alias to /health/ready for uniform readiness checks."""
    return await readiness()


@app.post("/api/v1/meaning/extract", response_model=ExtractionResponse)
async def extract_meaning(request: ExtractionRequest):
    """Extract semantic meaning from input"""
    
    try:
        meaning = await extractor.extract(
            input_text=request.input_text,
            context_hints=request.context
        )
        
        return ExtractionResponse(
            meaning_id=meaning.meaning_id,
            primary_interpretation=meaning.primary_interpretation,
            concepts=[c.to_dict() for c in meaning.concepts],
            beliefs=[b.dict() for b in meaning.beliefs],
            overall_confidence=meaning.overall_confidence
        )
        
    except Exception as e:
        logger.error("extraction_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


def _compute_symbol_snapshot(symbol: str, as_of: Optional[str] = None) -> Optional[Dict[str, Any]]:
    state = app.state.meaning_state
    symbol_state = state.get("symbols", {}).get(symbol)
    if not symbol_state:
        return None

    cutoff = _as_of_ts(as_of)
    timeframe_states: Dict[str, Any] = {}
    for tf, tf_state in symbol_state.get("timeframes", {}).items():
        events = [e for e in tf_state.get("events", []) if _as_of_ts(e.get("timestamp")) <= cutoff]
        if not events:
            continue
        events.sort(key=lambda e: e.get("timestamp") or "")
        last_event = events[-1]
        timeframe_states[tf] = {
            "bias": last_event.get("bias", "neutral"),
            "confidence": last_event.get("confidence", 0.5),
            "last_event": last_event,
            "events": events[-MEANING_EVENT_HISTORY_SIZE:],
        }

    # Determine HTF bias
    htf_bias = "neutral"
    htf_tf = None
    htf_conf = 0.0
    for tf in sorted(timeframe_states.keys(), key=lambda x: TF_AUTHORITY.get(x, 0), reverse=True):
        bias = timeframe_states[tf]["bias"]
        if bias and bias != "neutral":
            htf_bias = bias
            htf_tf = tf
            htf_conf = timeframe_states[tf]["confidence"]
            break

    contradictions = 0
    confluence = 0
    for tf, tf_state in timeframe_states.items():
        bias = tf_state.get("bias", "neutral")
        if bias == "neutral":
            continue
        if htf_bias != "neutral" and bias != htf_bias:
            contradictions += 1
        if htf_bias != "neutral" and bias == htf_bias:
            confluence += 1

    snapshot = {
        "symbol": symbol,
        "timeframes": timeframe_states,
        "htf_bias": htf_bias,
        "htf_timeframe": htf_tf,
        "htf_confidence": htf_conf,
        "confluence": confluence,
        "contradictions": contradictions,
        "as_of": cutoff.isoformat(),
    }
    snapshot["narrative"] = _generate_narrative(snapshot)
    return snapshot


def _generate_narrative(snapshot: Dict[str, Any]) -> str:
    """Generate a human-readable narrative from a symbol snapshot."""
    htf_bias = snapshot.get("htf_bias", "neutral")
    htf_tf = snapshot.get("htf_timeframe")
    confluence = snapshot.get("confluence", 0)
    contradictions = snapshot.get("contradictions", 0)
    timeframes = snapshot.get("timeframes", {})

    parts: List[str] = []

    # HTF bias summary
    if htf_bias == "neutral" or not htf_tf:
        parts.append("HTF neutral — no directional bias established")
    else:
        parts.append(f"HTF {htf_bias} ({htf_tf}) with {confluence}-TF confluence")

    # LTF (lowest-authority populated timeframe) context
    if timeframes:
        ltf_key = min(timeframes.keys(), key=lambda x: TF_AUTHORITY.get(x, 0))
        ltf_bias = timeframes[ltf_key].get("bias", "neutral")
        if htf_bias != "neutral" and ltf_bias == htf_bias:
            parts.append(f"LTF ({ltf_key}) aligned")
        elif htf_bias != "neutral" and ltf_bias != "neutral" and ltf_bias != htf_bias:
            parts.append(f"LTF ({ltf_key}) retracing but aligned" if confluence >= 2 else f"LTF ({ltf_key}) counter-trend")
        elif ltf_bias == "neutral":
            parts.append(f"LTF ({ltf_key}) neutral")

    # Contradictions
    if contradictions == 0:
        parts.append("No contradictions")
    else:
        parts.append(f"{contradictions} contradiction{'s' if contradictions != 1 else ''}")

    return ". ".join(parts) + "."


async def _fetch_shapes(symbol: str, timeframe: Optional[str] = None) -> List[Dict[str, Any]]:
    if not SHAPE_ENGINE_URL:
        return []
    params = {"symbol": symbol, "limit": 200, "offset": 0}
    if timeframe:
        params["timeframe"] = timeframe
    try:
        client = app.state.event_bus_client
        resp = await client.get(f"{SHAPE_ENGINE_URL}/api/v1/shapes", params=params)
        if resp.status_code != 200:
            return []
        data = resp.json()
        return data.get("shapes", []) if isinstance(data, dict) else []
    except Exception:
        return []


async def _fetch_memory(symbol: str, timeframe: Optional[str], as_of: Optional[str]) -> List[Dict[str, Any]]:
    if not MEMORY_URL:
        return []
    payload = {
        "symbol": symbol,
        "timeframe": timeframe,
        "as_of": as_of,
        "limit": 50,
        "min_confidence": 0.1,
    }
    try:
        client = app.state.event_bus_client
        resp = await client.post(f"{MEMORY_URL}/api/v1/memory/recall", json=payload)
        if resp.status_code != 200:
            return []
        data = resp.json()
        return data.get("results", []) if isinstance(data, dict) else []
    except Exception:
        return []


async def _evaluate_policy(
    bias: str,
    execution_timeframe: Optional[str],
    signals: List[str],
    contradictions: int,
    shape_types: List[str],
) -> Optional[Dict[str, Any]]:
    if not POLICY_ENGINE_URL:
        return None
    payload = {
        "strategy": MEANING_POLICY_STRATEGY,
        "bias": bias,
        "execution_timeframe": execution_timeframe,
        "session": None,
        "autonomy": True,
        "signals": signals,
        "poi_present": False,
        "contradictions": contradictions,
        "risk_state": {},
        "shape_types": shape_types,
    }
    try:
        client = app.state.event_bus_client
        resp = await client.post(f"{POLICY_ENGINE_URL}/api/v1/policy/evaluate", json=payload)
        if resp.status_code != 200:
            return None
        return resp.json()
    except Exception:
        return None


class MeaningDecisionRequest(BaseModel):
    symbol: str
    execution_timeframe: Optional[str] = None
    strategy: Optional[str] = None
    as_of: Optional[str] = None
    seed: Optional[int] = None
    context: Optional[Dict[str, Any]] = None


@app.post("/api/v1/meaning/decision")
async def meaning_decision(request: MeaningDecisionRequest):
    symbol = request.symbol
    as_of = request.as_of or datetime.now(timezone.utc).isoformat()

    async with app.state.state_lock:
        snapshot = _compute_symbol_snapshot(symbol, as_of=as_of)
    if not snapshot:
        raise HTTPException(status_code=404, detail="No meaning state for symbol")

    execution_tf = _normalize_timeframe(request.execution_timeframe) or snapshot.get("htf_timeframe")
    shapes = await _fetch_shapes(symbol, execution_tf)
    memory_context = await _fetch_memory(symbol, execution_tf, as_of)

    htf_bias = snapshot.get("htf_bias", "neutral")
    contradictions = snapshot.get("contradictions", 0)
    confluence = snapshot.get("confluence", 0)

    # Determine action
    action = "ignore"
    if htf_bias != "neutral":
        action = "monitor"
        if confluence >= 2 and contradictions == 0:
            action = "enter"

    # Evidence bundle
    event_ids = []
    for tf_state in snapshot.get("timeframes", {}).values():
        last_event = tf_state.get("last_event")
        if last_event and last_event.get("event_id"):
            event_ids.append(last_event.get("event_id"))
    shape_ids = [s.get("id") or s.get("shape_id") for s in shapes if s.get("id") or s.get("shape_id")]
    shape_types = [s.get("shape_type") for s in shapes if s.get("shape_type")]

    # Confidence calibration
    base_conf = snapshot.get("htf_confidence", 0.5)
    confidence = base_conf + (0.05 * confluence) - (0.1 * contradictions)
    confidence = max(0.05, min(0.95, confidence))

    policy = await _evaluate_policy(htf_bias, execution_tf, signals=list({e.get("event_type") for e in snapshot.get("timeframes", {}).get(execution_tf, {}).get("events", []) if e.get("event_type")}), contradictions=contradictions, shape_types=shape_types)
    policy_status = {
        "allowed": True,
        "reasons": [],
        "decision": policy,
    }
    if policy and policy.get("entry_allowed") is False:
        policy_status["allowed"] = False
        policy_status["reasons"] = policy.get("reasons", [])
        action = "blocked"
        confidence = min(confidence, 0.4)

    decision_id = str(uuid.uuid4())
    trace_id = str(uuid.uuid4())
    decision = {
        "decision_id": decision_id,
        "trace_id": trace_id,
        "symbol": symbol,
        "execution_timeframe": execution_tf,
        "timeframe_scope": sorted(snapshot.get("timeframes", {}).keys(), key=lambda x: TF_AUTHORITY.get(x, 0)),
        "bias": htf_bias,
        "action": action,
        "confidence": confidence,
        "confluence": confluence,
        "contradictions": contradictions,
        "invalidation": None,
        "targets": [],
        "evidence_bundle": {
            "event_ids": sorted(set(event_ids)),
            "shape_ids": sorted(set([sid for sid in shape_ids if sid])),
        },
        "policy_status": policy_status,
        "memory_context": memory_context[:10],
        "as_of": as_of,
    }

    snapshot_hash = hashlib.sha256(json.dumps(decision, sort_keys=True, default=str).encode("utf-8")).hexdigest()
    decision["snapshot_hash"] = snapshot_hash

    async with app.state.state_lock:
        app.state.meaning_state["decisions"][decision_id] = decision
    await _publish_meaning_decision(app, decision)
    await _publish_to_memory(app, decision)

    return decision


@app.get("/api/v1/meaning/state")
async def meaning_state(symbol: Optional[str] = Query(default=None), as_of: Optional[str] = Query(default=None)):
    """Return the latest event-driven meaning state summary."""
    if symbol:
        async with app.state.state_lock:
            snapshot = _compute_symbol_snapshot(symbol, as_of=as_of)
        if not snapshot:
            raise HTTPException(status_code=404, detail="No meaning state for symbol")
        return snapshot
    async with app.state.state_lock:
        return dict(app.state.meaning_state)


@app.get("/api/v1/meaning/narrative/{symbol}")
async def get_narrative(symbol: str, as_of: Optional[str] = Query(default=None)):
    """Return a human-readable narrative for the symbol's current meaning state."""
    async with app.state.state_lock:
        snapshot = _compute_symbol_snapshot(symbol, as_of=as_of)
    if not snapshot:
        raise HTTPException(status_code=404, detail="No meaning state for symbol")
    return {"symbol": symbol, "narrative": snapshot["narrative"], "as_of": snapshot["as_of"]}


@app.post("/api/v1/meaning/decision/enterprise")
async def enterprise_decision(
    symbol: str,
    execution_timeframe: Optional[str] = None,
    run_id: Optional[str] = None,
    seed: Optional[int] = None,
):
    """
    Generate enterprise-grade decision with full 12-TF analysis.
    
    Returns MeaningDecision with:
    - Evidence bundle (mandatory)
    - Policy status
    - Multi-TF confluence/contradiction scores
    - Rationale with reasoning steps
    - Deterministic replay hashes
    """
    try:
        engine = app.state.enterprise_engine
        
        decision = await engine.generate_decision(
            symbol=symbol,
            execution_timeframe=execution_timeframe,
            run_id=run_id,
            seed=seed,
            client=app.state.event_bus_client,
        )
        
        # Publish decision to event bus
        if MEANING_DECISION_PUBLISH_ENABLED:
            await _publish_meaning_decision(app, decision.to_event_payload())
        
        # Publish to memory
        await _publish_to_memory(app, decision.dict())
        
        return decision.dict()
    
    except Exception as e:
        logger.error("enterprise_decision_failed", error=str(e), symbol=symbol)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/meaning/belief-graph/{symbol}")
async def get_belief_graph(symbol: str):
    """Get 12-TF belief graph for symbol."""
    try:
        engine = app.state.enterprise_engine
        graph = engine.belief_graphs.get(symbol)
        
        if not graph:
            raise HTTPException(status_code=404, detail="No belief graph for symbol")
        
        return graph.to_dict()
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error("get_belief_graph_failed", error=str(e), symbol=symbol)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/meaning/confluence/{symbol}")
async def get_confluence(symbol: str):
    """Get multi-TF confluence analysis for symbol."""
    try:
        engine = app.state.enterprise_engine
        graph = engine.belief_graphs.get(symbol)
        
        if not graph:
            raise HTTPException(status_code=404, detail="No belief graph for symbol")
        
        confluence = graph.compute_confluence()
        return confluence.to_dict()
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error("get_confluence_failed", error=str(e), symbol=symbol)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/meaning/ingest/perception")
async def ingest_perception(event: Dict[str, Any]):
    """Ingest perception event and update belief graph."""
    try:
        engine = app.state.enterprise_engine
        await engine.ingest_perception_event(event)
        
        return {"status": "ingested", "event_id": event.get("event_id")}
    
    except Exception as e:
        logger.error("ingest_perception_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/meaning/ingest/shape")
async def ingest_shape(event: Dict[str, Any]):
    """Ingest shape event and update belief graph."""
    try:
        engine = app.state.enterprise_engine
        await engine.ingest_shape_event(event)
        
        return {"status": "ingested", "event_id": event.get("event_id")}
    
    except Exception as e:
        logger.error("ingest_shape_failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.SERVICE_PORT)
