# AUREXIS Detailed Issue List (2026-03-01)

Scope: cross-service runtime, integration contracts, security posture, and maintainability.
Method: static inspection of service code/config/docs without editing functional code.

## Critical Issues

1. Gateway port contract mismatch can break service startup and health probes.
- Evidence: `gateway/src/main.go:25` defaults to `52019`.
- Evidence: `gateway/Dockerfile:48` + `gateway/Dockerfile:52` expose/probe `52031`.
- Evidence: `docker-compose.yml:211` + `docker-compose.yml:229` map/probe `52031`.
- Impact: depending on runtime env vars, gateway may listen on a different port than orchestrator expects.

2. Gateway has dual entrypoints with different behavior (real service vs stub).
- Evidence: `gateway/src/main.go` is full gateway implementation.
- Evidence: `gateway/main.go:1-10` is explicit stub fallback.
- Impact: operator can launch wrong binary and think gateway is healthy while core routes are missing.

3. Shape policy gate is effectively fail-open and endpoint contract is wrong.
- Evidence: `shape-engine/src/integrations/policy_engine.py:36` calls `/api/v1/evaluate`.
- Evidence: policy service exposes `POST /api/v1/policy/evaluate` in `policy-engine/src/main.py:230`.
- Evidence: fallback allows action when policy unreachable in `shape-engine/src/integrations/policy_engine.py:24`.
- Evidence: detection service proceeds on policy errors in `shape-engine/src/services/detection_service.py:205`.
- Impact: autonomous shape creation can bypass policy enforcement under failure.

4. Simulation clients use API routes that do not exist in target services.
- Evidence: simulation perception client calls `/api/v1/events` in `simulation/src/clients/perception_client.py:44`.
- Evidence: perception app routes are in `perception/src/main.py` and do not expose `/api/v1/events`.
- Evidence: simulation reasoning client calls `/api/v1/reasoning/decisions` in `simulation/src/clients/reasoning_client.py:36`.
- Evidence: reasoning endpoints are `/api/v1/candidates` etc in `reasoning-engine/src/main.py:1392`.
- Impact: silent empty results degrade simulation quality and confidence signals.

5. Security-core keeps dev-open auth posture plus placeholder secret management in runtime path.
- Evidence: `security/.env:32` (`REQUIRE_AUTH=false`).
- Evidence: `security/src/api/routes/secrets.routes.js:22` (placeholder issuer).
- Evidence: `security/src/api/routes/health.routes.js:31` (placeholder dependency checks).
- Impact: if promoted accidentally, control-plane security guarantees are materially weakened.

6. Hardcoded/dev secrets remain in compose/config files.
- Evidence: `docker-compose.yml:8`, `docker-compose.yml:67`, `docker-compose.yml:217`.
- Evidence: `schema-registry/config/config.yaml:25`.
- Evidence: `gateway/config/config.yaml:14`.
- Impact: accidental leakage/misconfiguration risk; weak separation between local and secure environments.

## High Issues

7. Gateway service URL map is stale vs actual compose topology.
- Evidence: `gateway/config/config.yaml:45-179` uses legacy sequential ports.
- Evidence: actual services in `docker-compose.yml` use different ports, e.g. shape `52010`, simulation `52043`, event-bus `52020`, schema-registry `52025`.
- Impact: route failures and hard-to-debug cross-service connectivity errors.

8. Gateway defaults in code encode same stale topology.
- Evidence: `gateway/src/config/config.go:211-255` maps services to legacy ports.
- Impact: environments that skip YAML override inherit broken defaults.

9. Event-bus production runtime and test target are divergent.
- Evidence: production Docker builds Go binary in `event-bus/Dockerfile:7`.
- Evidence: tests target Python `main` stub (`event-bus/tests/test_api.py:1`, `event-bus/tests/test_health.py:1`).
- Impact: CI confidence does not cover production execution path.

10. Shape-engine CI workflow files are empty.
- Evidence: `shape-engine/.github/workflows/ci.yml` (0 bytes).
- Evidence: `shape-engine/.github/workflows/test.yml` (0 bytes).
- Impact: no automated validation despite complex service behavior.

11. Schema-registry lifecycle governance is incomplete.
- Evidence: retirement usage check TODO in `schema-registry/src/governance/governor.go:221`.
- Evidence: deprecate handler TODO persist status in `schema-registry/src/main.go:337`.
- Impact: schema state can diverge from governance expectations.

12. Gateway upload/stream handlers include TODO placeholders in active API.
- Evidence: `gateway/src/handlers/upload.go:159`, `:171`, `:181`, `:205`.
- Impact: endpoints can return synthetic/static responses instead of real operational data.

13. Meaning enterprise decision engine includes unresolved decision artifacts.
- Evidence: ontology concepts TODO `meaning-engine/src/utils/enterprise_decision_engine.py:600`.
- Evidence: counterfactual/rejected/confidence-factor TODOs at `:647-649`.
- Impact: downstream explainability and decision audit completeness are degraded.

14. Reasoning rule ontology validation remains partial/no-op style.
- Evidence: `reasoning-engine/src/engines/rule_engine.py:239` TODO for full ontology integration.
- Impact: invalid rule semantics may pass local checks.

15. Ontology validation has unimplemented property/constraint checks.
- Evidence: object/relationship property TODO `ontology/src/validation/ontology_validator.py:243`.
- Evidence: advanced expression validation TODO `ontology/src/validation/activation_gate.py:243`.
- Impact: false confidence in ontology integrity gates.

16. Knowledge-graph shutdown path leaves resource handling TODO.
- Evidence: `knowledge-graph/src/main.py:353-355`.
- Impact: graceful shutdown and persistence guarantees are uncertain.

17. Perception ontology client fails open on validation errors.
- Evidence: `perception/src/clients/ontology_client.py:143` returns `True` on exception.
- Impact: invalid patterns can proceed when ontology service is unavailable.

18. Learning engine swallows memory persistence failures.
- Evidence: `learning-engine/src/main.py:978` (`pass  # fail-open — memory is advisory`).
- Impact: audit/history gaps can occur silently.

19. Simulation docs and implementation are inconsistent for public endpoints.
- Evidence: docs list `/api/simulation/*` in `simulation/README.md:53-56`.
- Evidence: implementation exposes `/simulations/execute` + `/runs/*` in `simulation/src/app_factory.py:348`, `:443`.
- Impact: client integrations based on README fail.

20. Docs and historical audit statements are stale against current code.
- Evidence: placeholder date `docs/AUREXIS_V4_HONEST_AUDIT.md:3`.
- Evidence: stale `_transform_timeframe` claim in `simulation/README.md:76` while implementation exists in `simulation/src/branching_engine.py:491`.
- Impact: engineering decisions may be made on outdated facts.

21. Inactive decision action exists without selection path.
- Evidence: `FLAG_REVERSAL_RISK` defined in `core-brain/src/models/decision.py:49`.
- Impact: dead feature surface and misleading capability assumptions.

22. Core-brain fallback URL defaults are stale/non-canonical.
- Evidence: fallback values in `core-brain/src/orchestration/workflow_orchestrator.py:79-82`.
- Impact: local fallback mode can route to non-existent endpoints.

## Medium Issues

23. Perception requirements file has duplicate entries.
- Evidence: `httpx` appears at `perception/requirements.txt:11` and `:32`.
- Evidence: `python-dotenv` appears at `:15` and `:35`.
- Impact: dependency hygiene drift; potential resolver ambiguity in future edits.

24. Repository contains many backup artifacts in active service trees (before archival move).
- Evidence sample: `frontend/src/pages/Modules/ModulePage.tsx.bak`, `learning-engine/src/main.py.bak`, `gateway/config/config.yaml.bak`.
- Impact: code search noise and maintenance friction.

25. Large local data/venv artifacts are present in workspace and can hinder reproducibility.
- Evidence: multi-GB `market-ingestion/data/*` and `meaning-engine/venv/*` observed.
- Impact: slower onboarding, CI caching pressure, and accidental packaging risk.

## Notes

- This report intentionally focuses on production risk, integration correctness, and reliability.
- It excludes style-only concerns.
