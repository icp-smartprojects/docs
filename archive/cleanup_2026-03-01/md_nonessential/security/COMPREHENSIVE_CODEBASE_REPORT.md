# Comprehensive Codebase Report — `@sentinel/security-core`

**Generated:** Auto-generated full codebase audit  
**Package:** `@sentinel/security-core` v1.0.0-military-grade  
**Runtime:** Node.js >= 20.11.0, ESM (`"type": "module"`)  
**Framework:** Fastify 4.25.0

---

## Table of Contents

1. [Environment Variables](#1-environment-variables)
2. [API Endpoints](#2-api-endpoints)
3. [Integration Points](#3-integration-points)
4. [Security Features](#4-security-features)
5. [Configuration](#5-configuration)
6. [Scripts & Automation](#6-scripts--automation)
7. [Testing](#7-testing)
8. [Helm / Kubernetes](#8-helm--kubernetes)
9. [SDK](#9-sdk)
10. [Compliance Framework](#10-compliance-framework)
11. [Server Imports & Module Wiring](#11-server-imports--module-wiring)

---

## 1. Environment Variables

### Core / Service

| Variable | Default | Source File(s) |
|---|---|---|
| `NODE_ENV` | `"development"` | `main.js`, `constants.js`, `complianceChecker.js` |
| `SERVICE_NAME` | `"security-core"` | `main.js` |
| `SERVICE_REGION` | `""` | `main.js` |
| `SERVICE_INSTANCE_ID` | `""` | `main.js` |
| `APP_NAME` | `"security-repo"` | `constants.js` |
| `APP_VERSION` | `"0.1.0"` | `constants.js` |
| `HOSTNAME` | OS hostname | `main.js` |

### HTTP / Server

| Variable | Default | Source File(s) |
|---|---|---|
| `HOST` | `"0.0.0.0"` | `main.js` |
| `PORT` | `55000` | `main.js` |
| `TRUST_PROXY` | `false` | `main.js` |
| `TLS_ENABLED` | `false` | `main.js` |
| `REQUEST_MAX_BYTES` | `1048576` (1MB) | `main.js` |
| `RATE_LIMIT_PER_MIN` | `120` | `main.js` |
| `REQUIRE_AUTH` | `false` | `main.js`, `server.js` |
| `BEHIND_INGRESS` | `true` | `complianceChecker.js` |
| `REQUIRE_TLS` | `false` | `complianceChecker.js` |
| `FAIL_CLOSED` | `"true"` | `constants.js` |

### Rate Limit Constants

| Variable | Default | Source File(s) |
|---|---|---|
| `RL_DEFAULT_RPM` | `120` | `constants.js` |
| `RL_SENSITIVE_RPM` | `30` | `constants.js` |
| `RL_ADMIN_RPM` | `20` | `constants.js` |
| `RATELIMIT_ENABLED` | `true` | `complianceChecker.js` |

### Cryptography

| Variable | Default | Source File(s) |
|---|---|---|
| `KEK_BASE64` | (none) | `main.js` |
| `ACTIVE_KEY_ID` | `"kek-001"` | `main.js` |
| `ACTIVE_KEK_ID` | `"kek-001"` | `main.js` |
| `LOCAL_KEK_BASE64` | (none) | `kmsClient.js`, `complianceChecker.js` |
| `KEY_WRAP_PROVIDER` | `"kms"` | `keyManager.js`, `keyRotation.worker.js` |
| `UNWRAP_RATE_LIMIT` | `100` | `keyManager.js` |
| `CRYPTO_PAYLOAD_ALG` | `"A256GCM"` | `complianceChecker.js` |
| `KEY_ROTATION_DAYS` | `90` | `rotation.js` |
| `MAX_KEK_AGE_DAYS` | `90` | `keyRotation.worker.js`, `complianceChecker.js` |
| `KEK_OVERLAP_DAYS` | `14` | `keyRotation.worker.js`, `complianceChecker.js` |

### KMS

| Variable | Default | Source File(s) |
|---|---|---|
| `KMS_ENABLED` | `false` | `kmsClient.js` |
| `KMS_PROVIDER` | `"simulator"` | `kmsClient.js` |
| `KMS_ENDPOINT` | `""` | `kmsClient.js` |
| `KMS_MASTER_SECRET` | (none) | `kmsClient.js` |
| `KMS_ROTATE_URL` | `""` | `keyRotation.worker.js` |
| `KMS_API_KEY` | `""` | `keyRotation.worker.js` |
| `KMS_FAIL_OPEN` | `"false"` | `complianceChecker.js` |

### HSM

| Variable | Default | Source File(s) |
|---|---|---|
| `HSM_ENABLED` | `false` | `hsmClient.js` |
| `HSM_PROVIDER` | `"simulator"` | `hsmClient.js` |
| `HSM_SLOT` | `""` | `hsmClient.js` |
| `HSM_MASTER_KEY` | (none) | `hsmClient.js` |

### OIDC / Authentication

| Variable | Default | Source File(s) |
|---|---|---|
| `OIDC_ISSUER` | `""` | `oidcVerifier.js`, `authn.js` |
| `OIDC_AUDIENCE` | `""` | `oidcVerifier.js`, `authn.js` |
| `OIDC_JWKS_URL` | `""` | `oidcVerifier.js`, `authn.js` |
| `OIDC_DISCOVERY` | `""` | `oidcVerifier.js` |
| `OIDC_ALLOWED_ALGS` | `"RS256,ES256"` | `oidcVerifier.js`, `authn.js` |
| `OIDC_CLOCK_TOLERANCE_SEC` | `60` | `oidcVerifier.js`, `authn.js` |
| `OIDC_JWKS_CACHE_MS` | `600000` (10m) | `oidcVerifier.js` |
| `OIDC_TRUSTED_ISSUERS` | `""` (CSV) | `oidcContext.js` |
| `OIDC_ROLE_CLAIM` | `"roles"` | `authn.js` |
| `OIDC_SCOPE_CLAIM` | `"scope"` | `authn.js` |
| `OIDC_REQUIRED_ALGS` | `"RS256,ES256"` | `authn.js` |
| `AUTHN_ENABLED` | `true` | `authn.js` |
| `ADMIN_TOKEN` | `""` | `main.js`, `admin.routes.js` |

### mTLS / Service Identity

| Variable | Default | Source File(s) |
|---|---|---|
| `MTLS_ENABLED` | `false` | `mtls.js`, `algorithms.js` |
| `MTLS_CERT_PATH` | `""` | `algorithms.js` |
| `MTLS_KEY_PATH` | `""` | `algorithms.js` |
| `MTLS_CA_PATH` | `""` | `algorithms.js` |
| `MTLS_TRUSTED_ID_HEADER` | `""` | `mtls.js` |
| `MTLS_TRUSTED_CERT_FINGERPRINT_HEADER` | `""` | `mtls.js` |
| `SVC_ID_MODE` | `"auto"` | `serviceIdentity.js` |

### Audit

| Variable | Default | Source File(s) |
|---|---|---|
| `AUDIT_ENABLED` | `true` | `main.js` |
| `AUDIT_FILE` | `""` | `main.js` |
| `AUDIT_ARCHIVE_PATH` / `AUDIT_ARCHIVE_DIR` | `"/var/lib/security/audit"` | `immutableArchive.js`, `auditFlush.worker.js` |
| `AUDIT_SIGNING_KEY` | `""` | `main.js` |
| `AUDIT_SIGNING_SEED_HEX` | (none, 32-byte hex) | `signer.js` |
| `AUDIT_SIGNING_SECRET_HEX` | (none, 64-byte hex) | `signer.js` |
| `AUDIT_SIGN_MODE` | `"ed25519"` | `complianceChecker.js` |
| `AUDIT_ARCHIVE_ENABLED` | `true` | `complianceChecker.js` |
| `AUDIT_CHAINING` | `true` | `complianceChecker.js` |

### Audit Flush Worker

| Variable | Default | Source File(s) |
|---|---|---|
| `AUDIT_FLUSH_INTERVAL_SEC` | `30` | `auditFlush.worker.js` |
| `AUDIT_FLUSH_LOCK_NAME` | `"worker:audit-flush"` | `auditFlush.worker.js` |
| `AUDIT_FLUSH_CHECKPOINT_DIR` | `"/var/lib/security/audit/.checkpoints"` | `auditFlush.worker.js` |
| `AUDIT_FLUSH_MAX_FILES_PER_RUN` | `25` | `auditFlush.worker.js` |
| `AUDIT_FLUSH_MAX_LINES_PER_FILE` | `5000` | `auditFlush.worker.js` |

### Vault / Secrets

| Variable | Default | Source File(s) |
|---|---|---|
| `VAULT_ADDR` | `""` | `vaultClient.js` |
| `VAULT_TOKEN` | `""` | `vaultClient.js` |
| `VAULT_TIMEOUT_MS` | `5000` | `vaultClient.js` |
| `VAULT_RETRIES` | `2` | `vaultClient.js` |
| `VAULT_NAMESPACE` | `""` | `vaultClient.js` |
| `VAULT_TRANSIT_KEY` | `"security-kek"` | `keyRotation.worker.js` |
| `SECRETS_MODE` | `"vault"` | `secretManager.js` |
| `SECRETS_MAX_TTL_SEC` | `3600` | `secretManager.js` |
| `SECRETS_MIN_TTL_SEC` | `30` | `secretManager.js` |
| `SECRETS_DEFAULT_TTL_SEC` | `300` | `secretManager.js` |

### Database (PostgreSQL)

| Variable | Default | Source File(s) |
|---|---|---|
| `DB_URL` | `""` | `db.js` |
| `DB_SSL` | `false` | `db.js` |
| `DB_SSL_CA_PATH` | `""` | `db.js` |
| `DB_SSL_REJECT_UNAUTHORIZED` | `true` | `db.js` |
| `DB_POOL_MAX` | `10` | `db.js` |
| `DB_POOL_IDLE_TIMEOUT_MS` | `30000` | `db.js` |
| `DB_POOL_CONN_TIMEOUT_MS` | `5000` | `db.js` |
| `DB_APP_NAME` | `"security-core"` | `db.js` |
| `DB_STATEMENT_TIMEOUT_MS` | `5000` | `db.js` |
| `DB_LOG_QUERIES` | `false` | `db.js` |

### Object Storage

| Variable | Default | Source File(s) |
|---|---|---|
| `OBJECT_STORE_PROVIDER` | `"local"` | `objectStore.js` |
| `OBJECT_STORE_PATH` | `/tmp/security-objects` | `objectStore.js` |
| `S3_ENDPOINT` | `""` | `objectStore.js` |
| `S3_BUCKET_PREFIX` | `""` | `objectStore.js` |
| `S3_REGION` | `""` | `objectStore.js` |

### AV Scanning (ClamAV)

| Variable | Default | Source File(s) |
|---|---|---|
| `CLAMD_HOST` | `"127.0.0.1"` | `avScanner.js` |
| `CLAMD_PORT` | `3310` | `avScanner.js` |
| `CLAMD_TIMEOUT_MS` | `30000` | `avScanner.js` |
| `CLAMD_MAX_STREAM` | `26214400` (25MB) | `avScanner.js` |
| `AV_MODE` | `"clamd"` | `avScanner.js` |

### Sandbox / Detonation

| Variable | Default | Source File(s) |
|---|---|---|
| `SANDBOX_ENABLED` | `false` | `sandboxDetonation.js` |
| `SANDBOX_TIMEOUT_MS` | `30000` | `sandboxDetonation.js` |
| `SANDBOX_MAX_FILE_SIZE` | `10485760` (10MB) | `sandboxDetonation.js` |
| `SANDBOX_MODE` | `"simulate"` | `sandboxDetonation.js` |
| `SANDBOX_IMAGE` | `"security-sandbox:latest"` | `sandboxDetonation.js` |
| `SANDBOX_MALICIOUS_THRESHOLD` | `3` | `sandboxDetonation.js` |
| `SANDBOX_SUSPICIOUS_THRESHOLD` | `1` | `sandboxDetonation.js` |
| `SANDBOX_MODE_ENABLED` | `"false"` | `sandboxManager.js` |
| `SANDBOX_SESSION_TTL_MS` | `14400000` (4h) | `sandboxManager.js` |
| `SANDBOX_MAX_SESSIONS` | `50` | `sandboxManager.js` |

### API Keys

| Variable | Default | Source File(s) |
|---|---|---|
| `API_KEY_TTL_MS` | `2592000000` (30d) | `apiKeyManager.js` |
| `API_KEY_ROTATION_GRACE_MS` | `86400000` (24h) | `apiKeyManager.js` |
| `API_KEY_MAX_PER_OWNER` | `10` | `apiKeyManager.js` |

### Backpressure / Admission Control

| Variable | Default | Source File(s) |
|---|---|---|
| `BP_MAX_CONCURRENT` | `100` | `backpressure.js` |
| `BP_HIGH_WATERMARK` | `0.75` | `backpressure.js` |
| `BP_CRITICAL_WATERMARK` | `0.95` | `backpressure.js` |
| `BP_MAX_EVENT_LOOP_LAG_MS` | `500` | `backpressure.js` |
| `BP_MAX_MEMORY_PERCENT` | `85` | `backpressure.js` |
| `BP_CHECK_INTERVAL_MS` | `1000` | `backpressure.js` |

### Leader Election

| Variable | Default | Source File(s) |
|---|---|---|
| `LEADER_STRATEGY` | `"pg"` | `leaderElection.js` |
| `LEADER_LEASE_TTL_MS` | `15000` | `leaderElection.js` |
| `LEADER_RENEW_INTERVAL_MS` | `5000` | `leaderElection.js` |
| `LEADER_LOCK_DIR` | `/tmp/security-locks` | `leaderElection.js` |

### Re-wrap Worker

| Variable | Default | Source File(s) |
|---|---|---|
| `REWRAP_BATCH_SIZE` | `50` | `rewrap.worker.js` |
| `REWRAP_DELAY_MS` | `200` | `rewrap.worker.js` |
| `REWRAP_OLD_KEY_ID` | `""` | `rewrap.worker.js` |

### WAF

| Variable | Default | Source File(s) |
|---|---|---|
| `WAF_MODE` | `"enforce"` | `waf.js` |
| `WAF_MAX_HEADER_SIZE` | `8192` | `waf.js` |
| `WAF_MAX_COOKIE_SIZE` | `4096` | `waf.js` |
| `WAF_MAX_URL_LENGTH` | `2048` | `waf.js` |

### Compliance Worker

| Variable | Default | Source File(s) |
|---|---|---|
| `COMPLIANCE_SCAN_INTERVAL_SEC` | `3600` | `complianceScan.worker.js` |
| `COMPLIANCE_EVIDENCE_DIR` | `"/tmp/security-compliance"` | `complianceScan.worker.js` |
| `COMPLIANCE_LOCK_NAME` | `"worker:compliance-scan"` | `complianceScan.worker.js` |
| `COMPLIANCE_BASE_DIR` | `process.cwd()` | `complianceScan.worker.js` |
| `CLASSIFICATION_REQUIRED` | `true` | `complianceChecker.js` |

### Observability

| Variable | Default | Source File(s) |
|---|---|---|
| `LOG_LEVEL` | `"info"` | `logger.js` |
| `LOG_REDACT` | `true` | `logger.js` |
| `LOG_PRETTY` | `false` (prod) | `logger.js` |
| `METRICS_ENABLED` | `true` | `metrics.js` |
| `METRICS_PATH` | `"/metrics"` | `metrics.js` |
| `METRICS_PORT` | `9090` | `metrics.js` |
| `METRICS_STANDALONE` | `false` | `metrics.js` |
| `HEALTH_REQUIRE_DEPENDENCIES` | `true` | `health.js` |
| `HEALTH_TIMEOUT_MS` | `1000` | `health.js` |
| `TRACE_ENABLED` | `true` | `tracing.js` |
| `TRACE_HEADER` | `"x-trace-id"` | `tracing.js` |
| `SPAN_HEADER` | `"x-span-id"` | `tracing.js` |
| `CIRCUIT_BREAKER_ENABLED` | `true` | `main.js` |

### Alert Manager

| Variable | Default | Source File(s) |
|---|---|---|
| `PAGERDUTY_ROUTING_KEY` | `""` | `alertManager.js` |
| `PAGERDUTY_ENDPOINT` | PagerDuty v2 events API | `alertManager.js` |
| `OPSGENIE_API_KEY` | `""` | `alertManager.js` |
| `OPSGENIE_ENDPOINT` | Opsgenie v2 alerts API | `alertManager.js` |
| `SLACK_WEBHOOK_URL` | `""` | `alertManager.js` |
| `ALERT_WEBHOOK_URL` | `""` | `alertManager.js` |
| `ALERT_MIN_SEVERITY` | `"medium"` | `alertManager.js` |

### AuthZ Decision Logging

| Variable | Default | Source File(s) |
|---|---|---|
| `AUTHZ_DECISION_LOGS` | `"true"` | `authz.js` |

---

## 2. API Endpoints

All routes are prefixed at the application root. The API is versioned where indicated.

### Health / System

| Method | Path | Auth | Description | Source |
|---|---|---|---|---|
| `GET` | `/` | No | Root info (service name, version, uptime) | `health.routes.js` |
| `GET` | `/health/live` | No | Liveness probe (always `{ok:true}`) | `health.routes.js` |
| `GET` | `/health/ready` | No | Readiness (probes OPA, Vault, KMS, HSM) | `health.routes.js` |
| `GET` | `/health/info` | No | Service version + env metadata | `health.routes.js` |

### Cryptography

| Method | Path | Auth | Description | Source |
|---|---|---|---|---|
| `POST` | `/crypto/encrypt` | Yes | Encrypt JSON payload (envelope encryption) | `crypto.routes.js` |
| `POST` | `/crypto/decrypt` | Yes | Decrypt envelope (requires justification) | `crypto.routes.js` |
| `GET` | `/crypto/status` | Yes | Crypto subsystem status | `crypto.routes.js` |

### Secrets

| Method | Path | Auth | Description | Source |
|---|---|---|---|---|
| `POST` | `/secrets/issue` | Yes | Issue short-lived token (TTL-clamped) | `secrets.routes.js` |
| `POST` | `/secrets/revoke` | Yes | Revoke token by hash | `secrets.routes.js` |
| `POST` | `/secrets/validate` | Yes | Validate token liveness | `secrets.routes.js` |
| `GET` | `/secrets/status` | Yes | Secrets subsystem status | `secrets.routes.js` |

### Audit

| Method | Path | Auth | Description | Source |
|---|---|---|---|---|
| `GET` | `/audit/public-key` | No | Ed25519 public key for offline verification | `audit.routes.js` |
| `GET` | `/audit/recent` | Yes | Recent audit events (paginated) | `audit.routes.js` |
| `GET` | `/audit/by-subject/:subject` | Yes | Events by subject identity | `audit.routes.js` |
| `GET` | `/audit/by-type/:type` | Yes | Events by event type | `audit.routes.js` |
| `POST` | `/audit/record` | Yes | Write an audit event | `audit.routes.js` |

### Policy

| Method | Path | Auth | Description | Source |
|---|---|---|---|---|
| `POST` | `/policy/explain` | Yes | Explain ABAC+PBAC+OPA decision | `policy.routes.js` |
| `POST` | `/policy/check` | Yes | Check allow/deny for action | `policy.routes.js` |

### Admin

| Method | Path | Auth | Description | Source |
|---|---|---|---|---|
| `GET` | `/admin/status` | Admin | Full system status | `admin.routes.js` |
| `GET` | `/admin/config` | Admin | Safe config projection | `admin.routes.js` |
| `POST` | `/admin/approval/request` | Admin | Request multi-person approval | `admin.routes.js` |
| `POST` | `/admin/approval/:id/approve` | Admin | Approve operation | `admin.routes.js` |
| `POST` | `/admin/approval/:id/reject` | Admin | Reject operation | `admin.routes.js` |
| `GET` | `/admin/approval/:id` | Admin | Get approval status | `admin.routes.js` |
| `POST` | `/admin/rotate-keys` | Admin | Trigger key rotation (requires approval) | `admin.routes.js` |

### API Keys (`/api/v1/apikeys`)

| Method | Path | Auth | Description | Source |
|---|---|---|---|---|
| `POST` | `/api/v1/apikeys` | Yes | Create API key (scopes, IP allowlist, rate limits, expiry) | `apikeys.routes.js` |
| `GET` | `/api/v1/apikeys` | Yes | List keys for owner | `apikeys.routes.js` |
| `GET` | `/api/v1/apikeys/:id` | Yes | Get key metadata | `apikeys.routes.js` |
| `POST` | `/api/v1/apikeys/:id/rotate` | Yes | Rotate key (grace period) | `apikeys.routes.js` |
| `POST` | `/api/v1/apikeys/:id/revoke` | Yes | Revoke key | `apikeys.routes.js` |
| `POST` | `/api/v1/apikeys/:id/suspend` | Yes | Suspend key | `apikeys.routes.js` |
| `POST` | `/api/v1/apikeys/:id/reinstate` | Yes | Reinstate suspended key | `apikeys.routes.js` |
| `GET` | `/api/v1/apikeys/:id/usage` | Yes | Usage analytics | `apikeys.routes.js` |
| `DELETE` | `/api/v1/apikeys/expired` | Yes | Purge expired keys | `apikeys.routes.js` |

### Files (`/api/v1/files`)

| Method | Path | Auth | Description | Source |
|---|---|---|---|---|
| `POST` | `/api/v1/files/upload` | Yes | File upload (multipart/octet-stream → ingestion pipeline) | `files.routes.js` |
| `GET` | `/api/v1/files/:id` | Yes | Download file (streams from object store) | `files.routes.js` |
| `GET` | `/api/v1/files/:id/status` | Yes | File processing status | `files.routes.js` |
| `GET` | `/api/v1/files/:id/audit` | Yes | File audit trail | `files.routes.js` |
| `DELETE` | `/api/v1/files/:id` | Yes | Delete/purge file | `files.routes.js` |

### Metrics (standalone)

| Method | Path | Auth | Description | Source |
|---|---|---|---|---|
| `GET` | `:9090/metrics` | No | Prometheus text-format metrics | `metrics.js` |

---

## 3. Integration Points

### External Services

| Service | Protocol | Purpose | Source |
|---|---|---|---|
| **PostgreSQL 16** | TCP (pg driver) | Primary data store, tenant isolation, advisory locks, admin approvals | `db.js`, `docker-compose.yml` |
| **Open Policy Agent (OPA)** | HTTP POST `/v1/data/authz/allow` | External policy decisions (fail-closed) | `opaClient.js`, `docker-compose.yml` |
| **HashiCorp Vault** | HTTP REST | KV, Transit (key wrap/rotate), dynamic DB creds, token lifecycle | `vaultClient.js` |
| **KMS Gateway** | HTTP REST | Key wrapping/unwrapping (simulator mode uses PBKDF2+XOR) | `kmsClient.js` |
| **HSM** | Driver/API | Key wrapping (simulator uses AES-256-CBC) | `hsmClient.js` |
| **ClamAV (clamd)** | TCP `INSTREAM` + CLI fallback | Antivirus scanning for uploaded files | `avScanner.js` |
| **OIDC Identity Provider** | HTTPS (JWKS endpoint) | JWT verification, JWKS key rotation | `oidcVerifier.js`, `authn.js` |

### Alert Channels

| Channel | Protocol | Purpose | Source |
|---|---|---|---|
| **PagerDuty** | HTTPS POST (Events v2) | Critical security alerting | `alertManager.js` |
| **Opsgenie** | HTTPS POST (Alerts v2) | On-call alerting | `alertManager.js` |
| **Slack** | HTTPS POST (Webhook) | Team notifications | `alertManager.js` |
| **Generic Webhook** | HTTPS POST | Custom alert integration | `alertManager.js` |

### Docker Compose Services

| Service | Image | Ports |
|---|---|---|
| `postgres` | `postgres:16-alpine` | `5432` |
| `opa` | `openpolicyagent/opa:latest` | `8181` |
| `security-core` | Built from `Dockerfile` | `55000`, `9090` |

### Headers for Service-to-Service Identity

| Header | Purpose | Source |
|---|---|---|
| `x-trace-id` | Distributed trace correlation | `requestContext.js`, `tracing.js` |
| `x-request-id` | Request correlation | `requestContext.js` |
| `x-org` | Tenant/org isolation | `requestContext.js` |
| `x-purpose` | Purpose-based access control | `requestContext.js` |
| `x-classification` | Data classification level | `requestContext.js` |
| `x-verified-spiffe-id` | SPIFFE identity from mesh | `serviceIdentity.js` |
| `x-verified-client-cert-sha256` | mTLS cert fingerprint | `serviceIdentity.js`, `mtls.js` |
| `x-verified-client-dn` | mTLS distinguished name | `serviceIdentity.js` |
| `x-api-key` | API key auth | `apiKeyAuth.js` |
| `x-signature` | HMAC request signing | `apiKeyAuth.js` |

---

## 4. Security Features

### 4.1 Authentication

- **OIDC/JWT** — RS256, ES256 verification via JWKS with caching + in-flight dedup (`oidcVerifier.js`, `authn.js`)
- **Zero-dependency JWT parser** — Pure `node:crypto` JWT verification (`jwt.js`)
- **mTLS** — Peer certificate extraction + upstream verified header mode (`mtls.js`)
- **API Keys** — SHA-256 hashed storage, constant-time validation, IP allowlisting, per-key rate limits, HMAC signatures, rotation with grace period (`apiKeyManager.js`, `apiKeyAuth.js`)
- **Service Identity** — SPIFFE, cert fingerprint, DN extraction; distinguishes machine vs human (`serviceIdentity.js`, `jwt.js`)
- **Session Replay Protection** — TTL-bounded replay cache with token-context binding, timing-safe verification (`session.js`)

### 4.2 Authorization

- **3-layer Policy Engine** — Local ABAC + PBAC + optional OPA (`policyEngine.js`)
  - **ABAC rules**: Cross-org deny, network-based admin restrictions, classification gating (`abac.rules.js`)
  - **PBAC rules**: Purpose whitelisting for decrypt/secrets/audit access (`pbac.rules.js`)
  - **Data Access rules**: RBAC role matrix per action, justification required for decrypt (`dataAccess.rules.js`)
- **OPA Integration** — Circuit-breaker protected, fail-closed, OPA can restrict but never expand access
- **Default Deny** — Every route requires a `config.action` or is rejected 500

### 4.3 Cryptography

- **Envelope Encryption** — DEK/KEK separation with AAD (keyId, version, algorithm, classification, objectId)
- **Algorithms**: AES-256-GCM, ChaCha20-Poly1305, HKDF-SHA256, PBKDF2 (min 100k iterations)
- **Key Management**: HSM → KMS → local provider hierarchy; local denied in enterprise mode
- **Key Rotation**: Configurable rotation interval (default 90 days), overlap window, version tracking
- **Re-wrap Worker**: Background re-encryption on key rotation with rate limiting and crash-safe progress
- **mTLS Config**: TLS 1.2 minimum, strong cipher suites only, certificate pinning support

### 4.4 Audit & Non-Repudiation

- **Ed25519 Signing** — Every audit event signed with `tweetnacl`
- **Hash Chaining** — SHA-256 chain linking consecutive events
- **Immutable Archive** — Append-only WORM JSONL files with rotation at configurable max size (default 100MB)
- **Idempotent Recording** — Dedup via idempotency keys
- **Offline Verification** — Public key export + archive verifier validates signatures and chain integrity
- **Audit Flush Worker** — Flushes JSONL → PostgreSQL with checkpointing, advisory-lock leader election

### 4.5 WAF (Web Application Firewall)

- SQL injection, XSS, path traversal, command injection, request smuggling detection
- Header injection, oversized headers/cookies
- Malicious user-agent blocking (sqlmap, nikto, nessus, burpsuite, metasploit, etc.)
- Configurable enforce/detect/disabled mode
- Health/metrics paths whitelisted

### 4.6 Log Redaction

- **18 default patterns** — Bearer tokens, JWT, API keys, passwords, DB connection strings, AWS credentials, SSH keys, credit cards, SSNs, emails, phone numbers, Vault tokens, TLS certs, hex secrets (`redaction.js`)
- **Key-name blacklisting** — `password`, `secret`, `token`, `apiKey`, `jwt`, `credentials`, etc. (`sanitize.js`, `logging.js`)
- **Recursive object redaction** with depth/key limits

### 4.7 Request Protection

- **Header Spoofing Detection** — Validates `x-forwarded-for`, `x-real-ip`, etc. against trusted proxy list; generates `SECURITY_HEADER_SPOOFING_ATTEMPT` events (`requestContext.js`)
- **Content-Type Enforcement** — JSON required for mutation endpoints (`validate.js`)
- **Schema Enforcement** — Routes without schemas fail closed 500 (`validate.js`)
- **Body Size Guards** — Extra guard beyond Fastify's `bodyLimit`
- **Rate Limiting** — Global (via `@fastify/rate-limit`) + per-route (subject/IP/org-based) (`rateLimit.js`)

### 4.8 File Ingestion Security

- **8-step pipeline**: validate → quarantine → AV scan → PDF CDR → sandbox → encrypt → store → audit
- **Magic byte detection** for 25+ file types, 60+ blocked extensions, double-extension detection
- **ClamAV integration**: clamd TCP INSTREAM + CLI fallback with circuit breaker
- **PDF CDR**: Strips JavaScript, auto-actions, Launch, embedded files, URI actions, XFA, encrypted streams (16 dangerous patterns)
- **Sandbox Detonation**: Docker/nsjail/firejail with --network=none, --memory=512m, --cpus=0.5, --read-only; 15 behavioral IoC signatures
- **Quarantine statuses**: PENDING → SCANNING → AV_CLEAN/SUSPICIOUS/MALICIOUS → SANDBOX_* → RELEASED/REJECTED/PURGED

### 4.9 Break-Glass Emergency Access

- Time-boxed sessions (default 30min, max 1h)
- Requires: requester, reason, incidentTicket, justification
- Valid reasons: production_outage, security_incident, data_recovery, critical_bug_fix, system_failure
- Full audit trail with critical alerts, auto-expiration, no renewal
- All actions under break-glass are individually audited

### 4.10 Multi-Person Approval

- Required for: key rotation, policy change, secret issuance, admin role grant/revoke, config change, audit purge, credential revocation
- Quorum-based: 1–3 approvers depending on operation criticality
- Ed25519 signature verification on approvals (via `tweetnacl`)
- 24-hour expiry on approval requests
- Prevents duplicate approvals from same admin
- Database-backed workflow with full audit trail

### 4.11 Sandbox Mode (Developer)

- Isolated "sandbox" tenant with fake keys (never real KMS/HSM)
- Sandbox tokens invalid against production auth
- Watermarked audit trail (tagged "SANDBOX")
- Auto-cleanup with TTL, bounded session count (max 50)

---

## 5. Configuration

### 5.1 Config Files

| File | Purpose |
|---|---|
| `config/default.json` | Development defaults: port 55000, auth disabled, OPA disabled, DB disabled, rate limit 300/min, 1MB request max |
| `config/production.json` | Production overrides: auth required, OPA enabled, DB enabled, TLS enabled, rate limit 100/min, 512KB request max, pool max 50, daily compliance scan |
| `config/custom-environment-variables.json` | **EMPTY** — not currently mapping env vars via `config` package |
| `config/policies/abac.json` | 5 ABAC rules: admin all, crypto to operators, deny delete, org isolation, classification enforcement |
| `config/policies/pbac.json` | RBAC roles (admin/security_officer/operator/service) with permissions & constraints; classifications; purposes |
| `config/policies/data-classification.json` | **EMPTY** |

### 5.2 Docker

**Dockerfile** (multi-stage):
- Base: `node:20-alpine`
- Stage 1 (`builder`): `npm ci --omit=dev`
- Stage 2 (`runtime`): Non-root user `appuser:1001`, `dumb-init` entrypoint, read-only filesystem, healthcheck on `:55000/health`, `EXPOSE 55000 9090`

**docker-compose.yml** (3 services):
- `postgres:16-alpine` — port 5432, `postgres-data` volume
- `openpolicyagent/opa:latest` — port 8181
- `security-core` — built from Dockerfile, ports 55000 + 9090, depends on postgres + OPA

### 5.3 Data Classification Levels

Defined in `data/governance.js`:

| Level | Encryption | Retention | Org Isolation | Max Accessors |
|---|---|---|---|---|
| PUBLIC | No | 7 years | No | Unlimited |
| INTERNAL | Yes | 1 year | Yes | Unlimited |
| CONFIDENTIAL | Yes | 90 days | Yes | Unlimited (PII, audit 2yr) |
| SECRET | Yes | 30 days | Yes | 3 (approval required, audit 3yr) |

---

## 6. Scripts & Automation

### package.json npm scripts

| Script | Command |
|---|---|
| `start` | `node src/main.js` |
| `dev` | `node --watch src/main.js` |
| `test` | `tap tests/unit/*.test.js` |
| `test:integration` | `tap tests/integration/*.test.js` |
| `test:e2e` | `tap tests/e2e/*.test.js` |
| `test:all` | `npm test && npm run test:integration` |
| `migrate` | `node scripts/migrate.js` |
| `compliance-scan` | `node src/workers/complianceScan.worker.js` |
| `key-rotation` | `node src/workers/keyRotation.worker.js` |
| `audit-flush` | `node src/workers/auditFlush.worker.js` |
| `docker:build` | `docker build -t sentinel/security-core .` |
| `docker:push` | `docker push sentinel/security-core` |
| `helm:lint` | `helm lint helm/` |
| `helm:template` | `helm template security-core helm/` |
| `verify` | `node scripts/verify-all.js` |
| `assurance` | `node scripts/assurance-framework.js` |
| `gates` | `node scripts/pre-deployment-gates.js` |
| `chaos` | `node scripts/chaos-tests.js` |
| `sbom` | `node scripts/verify-sbom.js` |
| `evidence-pack` | `bash scripts/evidence-pack.sh` |
| `power-report` | `node scripts/power-report-generator.js` |

### Shell Scripts (`scripts/`)

| Script | Purpose |
|---|---|
| `bootstrap.sh` | Initial project setup |
| `backup.sh` | Backup procedures |
| `restore.sh` | Restore from backup |
| `rotate-certs.sh` | TLS certificate rotation |
| `rotate-keys.sh` | Key rotation automation |
| `smoke-test.sh` | Post-deployment smoke test |
| `hardening-check.sh` | System hardening verification |
| `evidence-pack.sh` | Generate compliance evidence bundle |
| `test-all.sh` | Run complete test suite |
| `test_audit_verifier.sh` | Test audit verification |
| `test_chaos.sh` | Chaos test runner |
| `test_security.sh` | Security test runner |
| `verify-system.sh` | Full system verification |

### JavaScript Scripts (`scripts/`)

| Script | Purpose |
|---|---|
| `assurance-framework.js` | Run assurance framework checks |
| `chaos-tests.js` | Chaos engineering tests |
| `evidence-pack.sh` | Compliance evidence generation |
| `migrate.js` | Database migration runner |
| `power-report-generator.js` | Generate comprehensive power report |
| `pre-deployment-gates.js` | Pre-deployment quality gates |
| `security-architecture-review.js` | Architecture security review |
| `test-all-12-checks.js` | All 12 government-grade checks |
| `verify-all.js` | Run all verifications |
| `verify-audit-archive.js` | Verify audit archive integrity |
| `verify-military-grade.js` | Military-grade compliance verification |
| `verify-operational.js` | Operational readiness checks |
| `verify-sbom.js` | SBOM verification |

### Background Workers

| Worker | Interval | Leader Election | Purpose |
|---|---|---|---|
| `auditFlush.worker.js` | 30s | PG advisory lock | Flush JSONL audit archives → PostgreSQL |
| `complianceScan.worker.js` | 1h | PG advisory lock | Run compliance checker, generate evidence reports |
| `keyRotation.worker.js` | Configurable | PG advisory lock | Rotate KEKs via Vault Transit or KMS gateway |
| `rewrap.worker.js` | 60s | Leader election | Re-encrypt data with new KEK versions |

---

## 7. Testing

### Test Framework

- **Unit tests**: `tap` (Node TAP)
- **Integration tests**: `@jest/globals` + `tap`
- Test runner configured via npm scripts

### Unit Tests (`tests/unit/`)

| Test File | Coverage |
|---|---|
| `crypto.test.js` | AES-256-GCM encrypt/decrypt round-trip, envelope encryption (DEK/KEK), auth tag tamper detection |
| `audit.test.js` | Ed25519 signer hash chains, immutable archive append-only + truncation rejection |
| `policy.test.js` | ABAC cross-org denial, PBAC purpose whitelisting for decrypt, role matrix data access |

### Integration Tests (`tests/integration/`)

| Test File | Coverage |
|---|---|
| `server.integration.test.js` | Service wiring verification (audit, policy, keyManager, health decorated), health check 200, request context middleware |
| `military-grade-system.test.js` | All 12 government-grade checks: Identity/Auth, Authorization/Policy, Cryptography, Secrets, Audit, Compliance, Resilience, Observability, Data Governance, Deployment, Governance/Admin, Integration |

### E2E Tests

- `tests/e2e/` — **Empty** (placeholder for future E2E tests)

### Test Fixtures

- `tests/fixtures/` — Available for test data

---

## 8. Helm / Kubernetes

### Helm Chart

| Field | Value |
|---|---|
| Chart Name | `security-core` |
| Version | `1.0.0` |
| App Version | `1.0.0` |
| Type | `application` |

### Helm values.yaml Defaults

| Setting | Value |
|---|---|
| `replicaCount` | `2` |
| `image.repository` | `sentinel/security-core` |
| `service.type` | `ClusterIP` |
| `service.port` | `55000` |
| `service.metricsPort` | `9090` |
| `ingress.enabled` | `true` (nginx class, cert-manager) |
| `resources.requests` | CPU: 100m, Memory: 256Mi |
| `resources.limits` | CPU: 500m, Memory: 512Mi |
| `autoscaling` | min: 2, max: 5, CPU: 70%, Memory: 80% |
| `security.runAsNonRoot` | `true` (UID 1001) |
| `security.readOnlyRootFilesystem` | `true` |

### Deployment Security Context

- `runAsNonRoot: true`, `runAsUser: 1001`, `runAsGroup: 1001`
- `seccompProfile: RuntimeDefault`
- `allowPrivilegeEscalation: false`
- `readOnlyRootFilesystem: true`
- `capabilities.drop: ALL`
- `automountServiceAccountToken: false`
- `topologySpreadConstraints` for HA (maxSkew=1 across nodes)
- `RollingUpdate` strategy: maxUnavailable=0, maxSurge=1

### Helm Templates

| Template | Purpose |
|---|---|
| `deployment.yaml` | Deployment with security context, probes, volumes, env |
| `configmap.yaml` | ConfigMap (empty, populated via values) |
| `ingress.yaml` | Ingress with TLS (cert-manager) |
| `hpa.yaml` | Horizontal Pod Autoscaler |
| `pdb.yaml` | Pod Disruption Budget |
| `role.yaml` | RBAC role |

### Probes

| Probe | Path | Settings |
|---|---|---|
| Liveness | `/health/live` | initialDelay=10s, period=15s, timeout=5s, failureThreshold=3 |
| Readiness | `/health/ready` | initialDelay=5s, period=10s, timeout=5s, failureThreshold=3 |
| Startup | `/health/live` | initialDelay=5s, period=5s, failureThreshold=12 |

### Volumes

| Volume | Mount | Purpose |
|---|---|---|
| `tmp` (emptyDir 100Mi) | `/tmp` | Temp files (read-only rootfs) |
| `audit-data` (emptyDir 500Mi) | `/app/audit-data` | Audit archives |
| `object-data` (emptyDir 1Gi) | `/app/data/objects` | Object storage |
| `tls-certs` (Secret, optional) | `/app/config/tls` | TLS certificates |

### Kustomize

- `k8s/base/` — Base Kubernetes manifests
- `k8s/overlays/` — Environment-specific overlays (dev/staging/prod)

---

## 9. SDK

### Node.js SDK (`sdk/nodejs/`)

**Package**: `@sentinel/security-client` v1.0.0  
**Dependency**: `axios`

**Constructor Config**:
- `baseURL` (default: `http://localhost:55000`)
- `token`, `org`, `purpose`, `classification`, `timeout`

**Methods**:

| Category | Method | HTTP |
|---|---|---|
| Crypto | `encrypt(plaintext, options)` | POST `/v1/crypto/encrypt` |
| Crypto | `decrypt(envelope)` | POST `/v1/crypto/decrypt` |
| Crypto | `wrapKey(dek, options)` | POST `/v1/crypto/wrap` |
| Crypto | `unwrapKey(wrappedDek)` | POST `/v1/crypto/unwrap` |
| Secrets | `issueSecret(options)` | POST `/v1/secrets/issue` |
| Secrets | `revokeSecret(secretId)` | DELETE `/v1/secrets/{id}` |
| Secrets | `getSecret(secretId)` | GET `/v1/secrets/{id}` |
| Policy | `checkPolicy(action, resource)` | PUT `/v1/policy/check` |
| Audit | `getRecentAudit(options)` | GET `/v1/audit/recent` |
| Audit | `getAuditBySubject(subject)` | GET `/v1/audit/by-subject/{subject}` |
| Audit | `getAuditPublicKey()` | GET `/v1/audit/public-key` |
| Health | `health()` | GET `/health` |
| Health | `metrics()` | GET `/metrics` |
| Admin | `admin.status()` | GET `/admin/status` |
| Admin | `admin.config()` | GET `/admin/config` |
| Admin | `admin.requestApproval(...)` | POST `/admin/approval/request` |
| Admin | `admin.approveRequest(id)` | POST `/admin/approval/{id}/approve` |
| Admin | `admin.rejectRequest(id, reason)` | POST `/admin/approval/{id}/reject` |
| Admin | `admin.getApproval(id)` | GET `/admin/approval/{id}` |
| Admin | `admin.createBreakGlass(...)` | POST `/admin/break-glass/create` |
| Admin | `admin.listActiveBreakGlass()` | GET `/admin/break-glass/active` |

**Features**: Auto-injects `Authorization`, `X-Org-ID`, `X-Purpose`, `X-Classification` headers. Response interceptor extracts `.data`. Error interceptor creates structured errors with `statusCode` and `code`.

---

## 10. Compliance Framework

### 10.1 Control Catalog (`controlCatalog.js`)

- **Catalog Version**: `2026.01`
- **Framework Mappings**: ISO 27001, NIST 800-53, CIS, SOC2, OWASP ASVS
- **Severity Levels**: CRITICAL, HIGH, MEDIUM, LOW
- **Status Outcomes**: PASS, FAIL, WARN, NOT_APPLICABLE, UNKNOWN

**Control Domains**:

| Domain | ID Prefix | Example Controls |
|---|---|---|
| Governance | `GOV-*` | Policy existence/versioning, risk assessment |
| Identity & Access | `IAM-*` | OIDC/JWT auth, ABAC/PBAC/OPA authz, mTLS |
| Cryptography | `CRYPTO-*` | TLS required, envelope AEAD, KMS/HSM key management, rotation policy |
| Audit & Logging | `AUD-*` | Tamper-evident signed/chained logs, event coverage |
| Operations | `OPS-*` | Rate limiting, KMS fail-closed, classification required |

### 10.2 Government-Grade 12-Check System (`governmentGradeChecks.js`)

**843 lines** implementing 100+ individual checks across 12 categories:

| # | Category | Check ID Prefix | Count |
|---|---|---|---|
| 1 | Identity & Authentication | `AUTHN_*` | 9 checks |
| 2 | Authorization & Policy | `AUTHZ_*` | 9 checks |
| 3 | Cryptography | `CRYPTO_*` | 8 checks |
| 4 | Secrets Management | `SECRETS_*` | 7 checks |
| 5 | Audit & Non-Repudiation | `AUDIT_*` | 8 checks |
| 6 | Compliance & Evidence | `COMPLIANCE_*` | 7 checks |
| 7 | Resilience & Failure Modes | `RESILIENCE_*` | 7 checks |
| 8 | Observability & Operations | `OBS_*` | 7 checks |
| 9 | Data Governance | `GOVERNANCE_*` | 7 checks |
| 10 | Deployment & Supply Chain | `DEPLOY_*` | 8 checks |
| 11 | Governance & Admin | `ADMIN_*` | 6 checks |
| 12 | Integration | `INTEGRATION_*` | 7 checks |

**Overall Status**: Any single FAIL → `NON_COMPLIANT`, warnings → `DEGRADED`, all pass → `COMPLIANT`

**Report Generation**: SHA-256 evidence hashing for non-repudiation, categorized results, UUID report IDs.

### 10.3 Compliance Checker (`complianceChecker.js`)

Automated posture monitor with 20+ individual checks covering:
- OIDC configuration, JWT algorithm verification
- OPA fail-closed enforcement
- mTLS / verified headers
- TLS requirement assertion
- Envelope encryption (A256GCM) verification
- KMS/HSM enablement, no local KEK in production
- Rotation policy configuration
- Audit signing, archive, chaining
- Rate limiting, KMS fail-closed, classification

### 10.4 Report Generator (`reportGenerator.js`)

- **Markdown reports** with emoji status indicators, sorted by severity then status
- **JSON reports** with SHA-256 evidence hashing
- Evidence bundle checklist for auditors
- Framework reference mapping per control

---

## 11. Server Imports & Module Wiring

### `server.js` — Complete Import Map

```
Node Built-ins:
  node:crypto, node:fs, node:path, node:url

Framework:
  fastify
  @fastify/helmet
  @fastify/rate-limit

Crypto Layer:
  src/crypto/kmsClient.js        → createKmsClient
  src/crypto/hsmClient.js        → createHsmClient
  src/crypto/keyManager.js       → createKeyManager

Audit Layer:
  src/audit/immutableArchive.js  → createImmutableArchive
  src/audit/eventRecorder.js     → createEventRecorder
  src/audit/signer.js            → createAuditSigner

Policy Layer:
  src/policy/policyEngine.js     → createPolicyEngine

Observability:
  src/observability/health.js    → createHealthChecker

Identity:
  src/identity/oidcContext.js    → initOidcVerifier
  src/identity/jwt.js            → verifyJwt, identifySubjectType
  src/identity/serviceIdentity.js → extractServiceIdentity

Storage:
  src/storage/db.js              → createDb
  src/storage/objectStore.js     → createObjectStore
  src/storage/quarantine.js      → createQuarantineManager

Ingestion:
  src/ingestion/ingestionPipeline.js → createIngestionPipeline
  src/ingestion/avScanner.js         → createAvScanner
  src/ingestion/sandboxDetonation.js → createSandboxEngine

Identity (API Keys):
  src/identity/apiKeyManager.js  → createApiKeyManager

Middleware:
  src/api/middleware/apiKeyAuth.js → createApiKeyAuthMiddleware
  src/api/middleware/waf.js       → createWafMiddleware

Resilience:
  src/resilience/backpressure.js   → createBackpressureManager
  src/resilience/leaderElection.js → createLeaderElection

Workers:
  src/workers/rewrap.worker.js   → createRewrapWorker

Admin:
  src/sandbox/sandboxManager.js  → createSandboxManager

Route Plugins:
  src/api/routes/health.routes.js
  src/api/routes/crypto.routes.js
  src/api/routes/secrets.routes.js
  src/api/routes/audit.routes.js
  src/api/routes/policy.routes.js
  src/api/routes/admin.routes.js
  src/api/routes/apikeys.routes.js
  src/api/routes/files.routes.js
```

### Middleware Pipeline (per-request order)

1. **WAF** — SQL injection / XSS / path traversal / command injection / request smuggling detection
2. **Backpressure** — Admission control based on concurrency, event loop lag, memory pressure
3. **@fastify/helmet** — Security headers (CSP, HSTS, X-Frame-Options, etc.)
4. **@fastify/rate-limit** — Global rate limiting
5. **Request Context** — traceId, requestId, org, purpose, risk, spoofing detection
6. **Authentication** — OIDC JWT verification via JWKS + API key extraction
7. **mTLS** — Peer cert extraction or upstream verified identity
8. **Per-route Rate Limiting** — Subject/IP/org-keyed limits
9. **Validation** — Content-Type, schema, body size enforcement
10. **Authorization (AuthZ)** — Policy engine enforcement (ABAC+PBAC+OPA), fail-closed
11. **Policy Decision Logging** — ALLOW + DENY decisions logged with complete context
12. **Route Handler** — Business logic
13. **Error Handler** — Strips details for 500s, safe error payloads

### Utility Modules

| Module | Purpose |
|---|---|
| `utils/constants.js` | App constants: HTTP headers, classifications, roles, limits, error codes, sensitive key list |
| `utils/errors.js` | Error hierarchy: AppError → ValidationError, UnauthenticatedError, ForbiddenError, NotFoundError, ConflictError, RateLimitedError, TimeoutError, UpstreamUnavailableError |
| `utils/logger.js` | Structured JSON logger (dependency-free): trace→fatal levels, auto-redaction, child loggers, safe error serialization |
| `utils/sanitize.js` | Control char stripping, CRLF injection prevention, recursive deep redaction, safe JSON stringify, safe ID assertion |
| `data/governance.js` | Data classification levels, retention policies, org isolation enforcement, automated purge workflows |

### Key Dependencies (from `package.json`)

| Package | Version | Purpose |
|---|---|---|
| `fastify` | `^4.25.0` | Web framework |
| `@fastify/helmet` | `^11.1.1` | Security headers |
| `@fastify/rate-limit` | `^9.1.0` | Rate limiting |
| `@fastify/jwt` | `^8.0.0` | JWT plugin |
| `@fastify/cors` | `^9.0.1` | CORS |
| `pg` | `^8.11.3` | PostgreSQL driver |
| `pino` | `^8.17.0` | Logging |
| `axios` | `^1.6.2` | HTTP client |
| `jose` | `^5.2.0` | OIDC/JWKS |
| `tweetnacl` | `^1.0.3` | Ed25519 signing |
| `node-cache` | `^5.1.2` | In-memory caching |
| `dotenv` | `^16.3.1` | Env file loading |
| `config` | `^3.3.9` | Config management |
| `helmet` | `^7.1.0` | Security headers (standalone) |

### Dev Dependencies

| Package | Version | Purpose |
|---|---|---|
| `tap` | `^18.6.1` | Unit test framework |
| `jest` | `^29.7.0` | Integration test framework |
| `@jest/globals` | `^29.7.0` | Jest globals |
| `nock` | `^13.4.0` | HTTP mocking |
| `supertest` | `^6.3.3` | HTTP assertions |
| `eslint` | `^8.56.0` | Linting |
| `prettier` | `^3.1.0` | Formatting |

---

*End of comprehensive codebase report.*
