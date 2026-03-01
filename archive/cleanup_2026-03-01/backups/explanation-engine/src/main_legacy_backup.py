"""
Explanation-Engine Main Service
FastAPI entry point with all API endpoints
"""

import time
import httpx
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from prometheus_client import Counter, Histogram, generate_latest, CollectorRegistry, REGISTRY
from pydantic import BaseModel, Field

from .causal import BeliefChainBuilder, CausalExplainer, ChainBuilder
from .config import get_settings
from .generation import BeliefExplainer, ContextBuilder, ExplanationGenerator
from .generation.enterprise_orchestrator import EnterpriseExplanationOrchestrator
from .models import Explanation, ExplanationType
from .natural_language import EvidenceNarrator, NLGEngine, StyleAdapter, TextBuilder
from .templates import TemplateLoader, TemplateManager
from .utils import (
    ExplanationEngineError,
    get_logger,
    log_service_ready,
    log_service_start,
    setup_logging,
)
from .visualization import GraphRenderer, VisualExplainer

# Initialize settings and logging
settings = get_settings()
setup_logging(settings.log_level, settings.json_logs)
logger = get_logger(__name__)

# Prometheus metrics
def _get_or_create_counter(name, documentation, labelnames):
    """Get existing metric or create new one"""
    try:
        return Counter(name, documentation, labelnames)
    except ValueError:
        # Metric already registered, retrieve it from registry
        return REGISTRY._names_to_collectors.get(name)

def _get_or_create_histogram(name, documentation, labelnames):
    """Get existing metric or create new one"""
    try:
        return Histogram(name, documentation, labelnames)
    except ValueError:
        # Metric already registered, retrieve it from registry
        metric = REGISTRY._names_to_collectors.get(name)
        if metric is None:
            # Try to find in the registry's collector_to_names mapping
            for collector, names in REGISTRY._collector_to_names.items():
                if name in names:
                    return collector
        return metric

request_counter = _get_or_create_counter(
    "explanation_requests_total",
    "Total explanation requests",
    ["endpoint", "status"]
)

request_latency = _get_or_create_histogram(
    "explanation_latency_seconds",
    "Explanation generation latency",
    ["endpoint"]
)

# Ensure request_latency is not None
if request_latency is None:
    request_latency = Histogram(
        "explanation_latency_seconds_v2",
        "Explanation generation latency",
        ["endpoint"]
    )


# Request/Response Models
class ExplainRequest(BaseModel):
    """Request model for explanation generation"""
    decision_id: str = Field(..., description="Decision ID to explain")
    style: str = Field(default="standard", description="Explanation style")
    include_visuals: bool = Field(default=False, description="Include visualization payload")


class ExternalGenerateRequest(BaseModel):
    """Gateway/frontend-compatible request (elementId + style)."""
    elementId: str = Field(..., description="Element/decision ID to explain")
    style: str = Field(default="standard", description="Explanation style")
    include_visuals: bool = Field(default=False, description="Include visualization payload")


class ExplainResponse(BaseModel):
    """Response model for explanation"""
    explanation: Dict[str, Any]
    natural_language: str
    visual_payload: Optional[Dict[str, Any]] = None
    message_card: str
    trace_ids: List[str]
    generation_time_ms: float


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    service: str
    version: str
    timestamp: float


# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage service lifecycle"""
    start_time = time.time()
    
    # Startup
    log_service_start(
        settings.service_name,
        settings.service_port,
        settings.model_dump()
    )
    
    # Initialize components
    app.state.chain_builder = ChainBuilder()
    app.state.belief_chain_builder = BeliefChainBuilder()
    app.state.causal_explainer = CausalExplainer()
    app.state.belief_explainer = BeliefExplainer()
    
    # Initialize context builder
    app.state.context_builder = ContextBuilder(
        semantic_memory_url=settings.semantic_memory_url,
        knowledge_graph_url=settings.knowledge_graph_url,
        core_brain_url=settings.core_brain_url,
        timeout_seconds=settings.explanation_timeout_seconds,
    )
    
    # Initialize explanation generator
    app.state.explanation_generator = ExplanationGenerator(
        chain_builder=app.state.chain_builder,
        belief_chain_builder=app.state.belief_chain_builder,
        causal_explainer=app.state.causal_explainer,
    )
    
    # Initialize NLG components
    text_builder = TextBuilder()
    style_adapter = StyleAdapter()
    app.state.nlg_engine = NLGEngine(text_builder, style_adapter)
    app.state.evidence_narrator = EvidenceNarrator()
    
    # Initialize templates
    template_loader = TemplateLoader()
    app.state.template_manager = TemplateManager(template_loader)
    
    # Initialize visualization
    graph_renderer = GraphRenderer()
    app.state.visual_explainer = VisualExplainer(graph_renderer)
    
    # Initialize enterprise orchestrator
    app.state.enterprise_orchestrator = EnterpriseExplanationOrchestrator(
        knowledge_graph_url=settings.knowledge_graph_url,
        simulation_url=settings.semantic_memory_url,  # Placeholder - adjust to simulation service
        policy_url=settings.core_brain_url,  # Policy through Core Brain
        memory_url=settings.semantic_memory_url,
        core_brain_url=settings.core_brain_url,
        timeout=settings.explanation_timeout_seconds,
    )
    
    startup_time_ms = (time.time() - start_time) * 1000
    log_service_ready(settings.service_name, startup_time_ms)
    
    yield
    
    # Shutdown
    logger.info("Shutting down Explanation-Engine")
    await app.state.context_builder.close()


# Create FastAPI app
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="Cognitive Introspection & Justification Service",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware for request tracking
@app.middleware("http")
async def track_requests(request: Request, call_next):
    """Track request metrics"""
    start_time = time.time()
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    request_latency.labels(endpoint=request.url.path).observe(duration)
    
    return response


# Exception handler
@app.exception_handler(ExplanationEngineError)
async def explanation_error_handler(request: Request, exc: ExplanationEngineError):
    """Handle explanation engine errors"""
    logger.error(
        "Explanation error",
        error=exc.message,
        details=exc.details,
    )
    
    request_counter.labels(
        endpoint=request.url.path,
        status="error"
    ).inc()
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=exc.to_dict(),
    )


# Health check endpoint
@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"],
    summary="Health check"
)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        service=settings.service_name,
        version=settings.api_version,
        timestamp=time.time(),
    )


# Readiness check endpoint
@app.get(
    "/ready",
    response_model=HealthResponse,
    tags=["Health"],
    summary="Readiness check"
)
async def readiness_check():
    """Readiness check endpoint"""
    checks = {}
    deps = {
        "core_brain": settings.core_brain_url,
        "semantic_memory": settings.semantic_memory_url,
        "knowledge_graph": settings.knowledge_graph_url,
    }
    async with httpx.AsyncClient(timeout=2.0) as client:
        for name, base in deps.items():
            if not base:
                continue
            base = base.rstrip("/")
            try:
                resp = await client.get(f"{base}/health")
                checks[name] = resp.status_code < 500
            except Exception:
                checks[name] = False

    ready = all(checks.values()) if checks else True
    if not ready:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"ready": False, "checks": checks},
        )

    return HealthResponse(
        status="ready",
        service=settings.service_name,
        version=settings.api_version,
        timestamp=time.time(),
    )


# Metrics endpoint
@app.get(
    "/metrics",
    tags=["Monitoring"],
    summary="Prometheus metrics"
)
async def metrics():
    """Expose Prometheus metrics"""
    from fastapi.responses import PlainTextResponse
    return PlainTextResponse(generate_latest())


# Main explanation endpoint
@app.post(
    f"{settings.api_prefix}/explain",
    response_model=ExplainResponse,
    tags=["Explanation"],
    summary="Generate explanation",
)
async def generate_explanation(request: ExplainRequest):
    """
    Generate complete explanation for a decision.
    
    Supports all 6 explanation types:
    - causal: Why did X happen?
    - structural: Was this valid according to rules?
    - temporal: Why did timing matter?
    - counterfactual: What if this didn't happen?
    - policy: Why was action blocked/allowed?
    - confidence: Why is belief strong/weak?
    """
    start_time = time.time()
    
    try:
        # Use enterprise orchestrator for comprehensive explanations
        explanations = await app.state.enterprise_orchestrator.explain_decision(
            decision_id=request.decision_id,
            explanation_types=[
                ExplanationType.CAUSAL,
                ExplanationType.STRUCTURAL,
                ExplanationType.TEMPORAL,
                ExplanationType.COUNTERFACTUAL,
                ExplanationType.POLICY,
                ExplanationType.CONFIDENCE_WEIGHTED,
            ],
            style=request.style,
        )
        
        # Use primary explanation (causal) for response
        primary_explanation = explanations.get(ExplanationType.CAUSAL)
        if not primary_explanation:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate explanation"
            )
        
        generation_time_ms = (time.time() - start_time) * 1000
        
        # Build message card (DIN 1451 format)
        from .templates.message_card import render_message_card
        card_sections = {
            "EXPLANATION TYPE": ["All 6 modes generated"],
            "PRIMARY (CAUSAL)": [primary_explanation.why],
            "EVIDENCE": primary_explanation.evidence[:5],
            "CONFIDENCE": [f"{primary_explanation.confidence.overall:.1%}"],
            "ALTERNATIVES": [alt.option for alt in primary_explanation.alternatives[:3]],
        }
        message_card = render_message_card(card_sections)
        
        request_counter.labels(endpoint="/explain", status="success").inc()
        
        return ExplainResponse(
            explanation=primary_explanation.to_dict(),
            natural_language=primary_explanation.natural_language,
            visual_payload=primary_explanation.visual_payload if request.include_visuals else None,
            message_card=message_card,
            trace_ids=primary_explanation.metadata.trace_ids,
            generation_time_ms=generation_time_ms,
        )
        
    except Exception as e:
        logger.error(f"Explanation generation failed: {str(e)}")
        request_counter.labels(endpoint="/explain", status="error").inc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.post(
    f"{settings.api_prefix}/explanation/generate",
    response_model=ExplainResponse,
    tags=["Explanation"],
    summary="Generate explanation (gateway-compatible)",
    description="Alias endpoint to keep gateway/frontend contract stable",
)
async def explain_generate_alias(
    request_data: ExternalGenerateRequest,
    request: Request,
):
    start_time = time.time()
    logger.info(
        "Explanation generate (alias) request received",
        decision_id=request_data.elementId,
        style=request_data.style,
    )
    return await _generate_explanation_response(
        decision_id=request_data.elementId,
        style=request_data.style,
        include_visuals=request_data.include_visuals,
        request=request,
        start_time=start_time,
    )


async def _generate_explanation_response(
    decision_id: str,
    style: str,
    include_visuals: bool,
    request: Request,
    start_time: float,
) -> ExplainResponse:
    """Shared generation flow for both native and alias endpoints."""
    try:
        context = await request.app.state.context_builder.build_context(
            decision_id=decision_id,
            require_all_traces=settings.require_all_traces,
        )

        trace_data = {
            "trace_1": {
                "reasoning_steps": [],
                "rejected_alternatives": [],
                "invalidation_conditions": [],
            }
        }

        belief_data = {
            "belief_1": {
                "concept_id": context.semantic_context.concept_id,
                "timestamp": context.timestamp.isoformat(),
                "value": "bullish",
                "confidence": context.confidence,
                "evidence_count": len(context.evidence_sources),
            }
        }

        causal_graph = {
            "nodes": [],
            "edges": [],
        }

        explanation = await request.app.state.explanation_generator.generate(
            context=context,
            trace_data=trace_data,
            belief_data=belief_data,
            causal_graph=causal_graph,
            style=style,
            include_visuals=include_visuals,
        )

        natural_language = request.app.state.nlg_engine.generate_text(
            explanation=explanation,
            style=style,
        )

        visual_payload = None
        if include_visuals:
            visual_payload = request.app.state.visual_explainer.generate_visual_payload(
                explanation=explanation,
            )

        generation_time_ms = (time.time() - start_time) * 1000

        logger.info(
            "Explanation generated successfully",
            decision_id=decision_id,
            generation_time_ms=generation_time_ms,
            confidence=explanation.confidence.overall,
        )

        request_counter.labels(
            endpoint=request.url.path,
            status="success"
        ).inc()

        return ExplainResponse(
            explanation=explanation.to_dict(),
            natural_language=natural_language,
            message_card=explanation.natural_language,
            visual_payload=visual_payload,
            trace_ids=context.reasoning_trace_ids,
            generation_time_ms=generation_time_ms,
        )

    except Exception as e:
        logger.error(
            "Explanation generation failed",
            decision_id=decision_id,
            error=str(e),
            exc_info=True,
        )

        request_counter.labels(
            endpoint=request.url.path,
            status="error"
        ).inc()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Explanation generation failed: {str(e)}"
        )


# Belief evolution endpoint
@app.get(
    f"{settings.api_prefix}/explain/belief/{{concept_id}}",
    tags=["Explanation"],
    summary="Explain belief evolution"
)
async def explain_belief_evolution(
    concept_id: str,
    request: Request,
):
    """Explain how a belief evolved over time"""
    try:
        # TODO: Implement belief evolution explanation
        return {
            "concept_id": concept_id,
            "message": "Belief evolution explanation not yet implemented"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# Reasoning path endpoint
@app.get(
    f"{settings.api_prefix}/explain/path",
    tags=["Explanation"],
    summary="Get reasoning path"
)
async def get_reasoning_path(
    from_concept: str,
    to_concept: str,
    request: Request,
):
    """Get reasoning path between two concepts"""
    try:
        # TODO: Implement reasoning path retrieval
        return {
            "from": from_concept,
            "to": to_concept,
            "message": "Reasoning path not yet implemented"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# Root endpoint
@app.get("/", tags=["Info"])
async def root():
    """Root endpoint with service information"""
    return {
        "service": settings.service_name,
        "version": settings.api_version,
        "status": "operational",
        "endpoints": {
            "health": "/health",
            "ready": "/ready",
            "metrics": "/metrics",
            "explain": f"{settings.api_prefix}/explain",
            "docs": "/docs",
        }
    }


# Main entry point
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=settings.service_port,
        reload=settings.is_development(),
        log_level=settings.log_level.lower(),
    )
