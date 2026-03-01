# COMPLETE API GATEWAY IMPLEMENTATION
## Service 52031 - Meaning-Centric Cognitive System
## All Files and Complete Implementation

---

## TABLE OF CONTENTS

1. [Project Structure](#project-structure)
2. [Configuration Files](#configuration-files)
3. [Source Code](#source-code)
   - Main Entry Point
   - Configuration Management
   - Models (Errors, Requests, Responses)
   - Middleware (Auth, CORS, Logging, Metrics, Rate Limiting, Recovery, Tracing)
   - Handlers (Health, Semantic, WebSocket)
   - Routes (Router Setup, API Routes, Health Routes, WebSocket Routes)
   - Services (Circuit Breaker, Discovery, Load Balancer, Proxy)
   - Utils (Logger, Validator, Errors)
4. [Kubernetes Deployment](#kubernetes-deployment)
5. [Helm Charts](#helm-charts)
6. [Docker Configuration](#docker-configuration)
7. [Testing](#testing)
8. [Makefile](#makefile)

---

## PROJECT STRUCTURE

```
gateway/
├── src/
│   ├── main.go
│   ├── config/
│   │   ├── config.go
│   │   └── loader.go
│   ├── handlers/
│   │   ├── health.go
│   │   ├── semantic.go
│   │   └── websocket.go
│   ├── middleware/
│   │   ├── auth.go
│   │   ├── cors.go
│   │   ├── logging.go
│   │   ├── metrics.go
│   │   ├── ratelimit.go
│   │   ├── recovery.go
│   │   └── tracing.go
│   ├── models/
│   │   ├── error.go
│   │   ├── request.go
│   │   └── response.go
│   ├── routes/
│   │   ├── router.go
│   │   ├── api.go
│   │   ├── health.go
│   │   └── websocket.go
│   ├── services/
│   │   ├── circuitbreaker.go
│   │   ├── discovery.go
│   │   ├── loadbalancer.go
│   │   └── proxy.go
│   └── utils/
│       ├── logger.go
│       ├── validator.go
│       └── errors.go
├── config/
│   └── config.yaml
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── configmap.yaml
├── helm/
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── deployment.yaml
│       └── service.yaml
├── tests/
│   ├── unit/
│   └── integration/
├── Dockerfile
├── Makefile
├── go.mod
├── go.sum
└── README.md
```

---

## MIDDLEWARE IMPLEMENTATIONS

### middleware/auth.go
```go
// Package middleware - JWT Authentication Middleware
// Validates JWT tokens and extracts user context
package middleware

import (
	"net/http"
	"strings"

	"gateway/src/models"
	"gateway/src/utils"

	"github.com/gin-gonic/gin"
	"github.com/golang-jwt/jwt/v5"
)

// Claims represents JWT custom claims
type Claims struct {
	UserID   string   `json:"user_id"`
	Username string   `json:"username"`
	Role     string   `json:"role"`
	Permissions []string `json:"permissions"`
	jwt.RegisteredClaims
}

// AuthMiddleware validates JWT tokens
func AuthMiddleware(jwtSecret string) gin.HandlerFunc {
	return func(c *gin.Context) {
		// Extract token from Authorization header
		authHeader := c.GetHeader("Authorization")
		if authHeader == "" {
			c.JSON(http.StatusUnauthorized, models.NewUnauthorizedError("Missing authorization header").ToErrorResponse())
			c.Abort()
			return
		}

		// Check Bearer prefix
		parts := strings.Split(authHeader, " ")
		if len(parts) != 2 || parts[0] != "Bearer" {
			c.JSON(http.StatusUnauthorized, models.NewUnauthorizedError("Invalid authorization format").ToErrorResponse())
			c.Abort()
			return
		}

		tokenString := parts[1]

		// Parse and validate token
		claims := &Claims{}
		token, err := jwt.ParseWithClaims(tokenString, claims, func(token *jwt.Token) (interface{}, error) {
			return []byte(jwtSecret), nil
		})

		if err != nil {
			if err == jwt.ErrSignatureInvalid {
				c.JSON(http.StatusUnauthorized, models.NewUnauthorizedError("Invalid token signature").ToErrorResponse())
			} else {
				c.JSON(http.StatusUnauthorized, models.NewUnauthorizedError("Invalid token").WithError(err).ToErrorResponse())
			}
			c.Abort()
			return
		}

		if !token.Valid {
			c.JSON(http.StatusUnauthorized, models.NewUnauthorizedError("Token is not valid").ToErrorResponse())
			c.Abort()
			return
		}

		// Store user context for downstream handlers
		c.Set("user_id", claims.UserID)
		c.Set("username", claims.Username)
		c.Set("role", claims.Role)
		c.Set("permissions", claims.Permissions)

		c.Next()
	}
}

// RequireRole ensures user has specific role
func RequireRole(allowedRoles ...string) gin.HandlerFunc {
	return func(c *gin.Context) {
		role, exists := c.Get("role")
		if !exists {
			c.JSON(http.StatusForbidden, models.NewForbiddenError("User role not found in context").ToErrorResponse())
			c.Abort()
			return
		}

		userRole := role.(string)
		for _, allowed := range allowedRoles {
			if userRole == allowed {
				c.Next()
				return
			}
		}

		c.JSON(http.StatusForbidden, models.NewForbiddenError("Insufficient permissions").ToErrorResponse())
		c.Abort()
	}
}

// RequirePermission ensures user has specific permission
func RequirePermission(permission string) gin.HandlerFunc {
	return func(c *gin.Context) {
		perms, exists := c.Get("permissions")
		if !exists {
			c.JSON(http.StatusForbidden, models.NewForbiddenError("Permissions not found").ToErrorResponse())
			c.Abort()
			return
		}

		permissions := perms.([]string)
		for _, p := range permissions {
			if p == permission || p == "*" { // Wildcard permission
				c.Next()
				return
			}
		}

		c.JSON(http.StatusForbidden, models.NewForbiddenError("Missing required permission: "+permission).ToErrorResponse())
		c.Abort()
	}
}
```

### middleware/cors.go
```go
// Package middleware - CORS Middleware
// Handles Cross-Origin Resource Sharing
package middleware

import (
	"gateway/src/config"

	"github.com/gin-gonic/gin"
)

// CORSMiddleware handles CORS headers
func CORSMiddleware(cfg config.CORSConfig) gin.HandlerFunc {
	return func(c *gin.Context) {
		origin := c.Request.Header.Get("Origin")
		
		// Check if origin is allowed
		allowed := false
		for _, allowedOrigin := range cfg.AllowedOrigins {
			if allowedOrigin == "*" || allowedOrigin == origin {
				allowed = true
				break
			}
		}

		if allowed {
			c.Header("Access-Control-Allow-Origin", origin)
		}

		// Set other CORS headers
		c.Header("Access-Control-Allow-Methods", strings.Join(cfg.AllowedMethods, ", "))
		c.Header("Access-Control-Allow-Headers", strings.Join(cfg.AllowedHeaders, ", "))
		c.Header("Access-Control-Expose-Headers", strings.Join(cfg.ExposedHeaders, ", "))
		
		if cfg.AllowCredentials {
			c.Header("Access-Control-Allow-Credentials", "true")
		}
		
		c.Header("Access-Control-Max-Age", fmt.Sprintf("%d", cfg.MaxAge))

		// Handle preflight requests
		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(204)
			return
		}

		c.Next()
	}
}
```

### middleware/logging.go
```go
// Package middleware - Request Logging Middleware
// Logs all HTTP requests with semantic context
package middleware

import (
	"time"

	"gateway/src/utils"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
)

// LoggingMiddleware logs all requests with semantic information
func LoggingMiddleware(logger *utils.Logger) gin.HandlerFunc {
	return func(c *gin.Context) {
		start := time.Now()

		// Generate request ID if not present
		requestID := c.GetHeader("X-Request-ID")
		if requestID == "" {
			requestID = uuid.New().String()
			c.Header("X-Request-ID", requestID)
		}
		c.Set("request_id", requestID)

		// Process request
		c.Next()

		// Calculate duration
		duration := time.Since(start)

		// Log request details
		logger.Info("HTTP Request",
			"request_id", requestID,
			"method", c.Request.Method,
			"path", c.Request.URL.Path,
			"status", c.Writer.Status(),
			"duration_ms", duration.Milliseconds(),
			"client_ip", c.ClientIP(),
			"user_agent", c.Request.UserAgent(),
		)

		// Log errors if any
		if len(c.Errors) > 0 {
			for _, err := range c.Errors {
				logger.Error("Request error",
					"request_id", requestID,
					"error", err.Error(),
				)
			}
		}
	}
}
```

### middleware/metrics.go
```go
// Package middleware - Prometheus Metrics Middleware
// Collects HTTP metrics for monitoring
package middleware

import (
	"strconv"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/prometheus/client_golang/prometheus"
)

var (
	httpRequestsTotal = prometheus.NewCounterVec(
		prometheus.CounterOpts{
			Name: "http_requests_total",
			Help: "Total number of HTTP requests",
		},
		[]string{"method", "path", "status"},
	)

	httpRequestDuration = prometheus.NewHistogramVec(
		prometheus.HistogramOpts{
			Name:    "http_request_duration_seconds",
			Help:    "HTTP request duration in seconds",
			Buckets: prometheus.DefBuckets,
		},
		[]string{"method", "path", "status"},
	)

	httpRequestSize = prometheus.NewHistogramVec(
		prometheus.HistogramOpts{
			Name:    "http_request_size_bytes",
			Help:    "HTTP request size in bytes",
			Buckets: prometheus.ExponentialBuckets(100, 10, 8),
		},
		[]string{"method", "path"},
	)

	httpResponseSize = prometheus.NewHistogramVec(
		prometheus.HistogramOpts{
			Name:    "http_response_size_bytes",
			Help:    "HTTP response size in bytes",
			Buckets: prometheus.ExponentialBuckets(100, 10, 8),
		},
		[]string{"method", "path", "status"},
	)
)

func init() {
	prometheus.MustRegister(httpRequestsTotal)
	prometheus.MustRegister(httpRequestDuration)
	prometheus.MustRegister(httpRequestSize)
	prometheus.MustRegister(httpResponseSize)
}

// MetricsMiddleware collects Prometheus metrics
func MetricsMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		start := time.Now()

		// Record request size
		if c.Request.ContentLength > 0 {
			httpRequestSize.WithLabelValues(
				c.Request.Method,
				c.FullPath(),
			).Observe(float64(c.Request.ContentLength))
		}

		// Process request
		c.Next()

		// Calculate duration
		duration := time.Since(start).Seconds()
		status := strconv.Itoa(c.Writer.Status())

		// Record metrics
		httpRequestsTotal.WithLabelValues(
			c.Request.Method,
			c.FullPath(),
			status,
		).Inc()

		httpRequestDuration.WithLabelValues(
			c.Request.Method,
			c.FullPath(),
			status,
		).Observe(duration)

		// Record response size
		httpResponseSize.WithLabelValues(
			c.Request.Method,
			c.FullPath(),
			status,
		).Observe(float64(c.Writer.Size()))
	}
}
```

### middleware/ratelimit.go
```go
// Package middleware - Rate Limiting Middleware
// Implements token bucket rate limiting per user/IP
package middleware

import (
	"fmt"
	"sync"
	"time"

	"gateway/src/config"
	"gateway/src/models"

	"github.com/gin-gonic/gin"
)

// RateLimiter implements token bucket algorithm
type RateLimiter struct {
	mu      sync.RWMutex
	buckets map[string]*bucket
	config  config.RateLimitConfig
}

type bucket struct {
	tokens     int
	lastRefill time.Time
}

// NewRateLimiter creates a new rate limiter
func NewRateLimiter(cfg config.RateLimitConfig) *RateLimiter {
	limiter := &RateLimiter{
		buckets: make(map[string]*bucket),
		config:  cfg,
	}

	// Start cleanup goroutine
	go limiter.cleanup()

	return limiter
}

// RateLimitMiddleware applies rate limiting
func (rl *RateLimiter) RateLimitMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		if !rl.config.Enabled {
			c.Next()
			return
		}

		// Determine key (user_id or IP)
		key := rl.getKey(c)

		// Check if allowed
		allowed, remaining := rl.allow(key, c)
		if !allowed {
			c.Header("X-RateLimit-Limit", fmt.Sprintf("%d", rl.getLimit(c)))
			c.Header("X-RateLimit-Remaining", "0")
			c.Header("X-RateLimit-Reset", fmt.Sprintf("%d", time.Now().Add(rl.config.WindowSize).Unix()))
			
			c.JSON(429, models.NewRateLimitError(rl.getLimit(c), rl.config.WindowSize.String()).ToErrorResponse())
			c.Abort()
			return
		}

		// Set rate limit headers
		c.Header("X-RateLimit-Limit", fmt.Sprintf("%d", rl.getLimit(c)))
		c.Header("X-RateLimit-Remaining", fmt.Sprintf("%d", remaining))
		c.Header("X-RateLimit-Reset", fmt.Sprintf("%d", time.Now().Add(rl.config.WindowSize).Unix()))

		c.Next()
	}
}

// getKey determines the rate limit key (user_id or IP)
func (rl *RateLimiter) getKey(c *gin.Context) string {
	userID, exists := c.Get("user_id")
	if exists {
		return fmt.Sprintf("user:%s", userID)
	}
	return fmt.Sprintf("ip:%s", c.ClientIP())
}

// getLimit returns the rate limit for the user's role
func (rl *RateLimiter) getLimit(c *gin.Context) int {
	role, exists := c.Get("role")
	if exists && rl.config.RoleLimits != nil {
		if limit, ok := rl.config.RoleLimits[role.(string)]; ok {
			return limit
		}
	}
	return rl.config.RequestsPer
}

// allow checks if request is allowed
func (rl *RateLimiter) allow(key string, c *gin.Context) (bool, int) {
	rl.mu.Lock()
	defer rl.mu.Unlock()

	now := time.Now()
	b, exists := rl.buckets[key]
	
	if !exists {
		// Create new bucket
		b = &bucket{
			tokens:     rl.getLimit(c),
			lastRefill: now,
		}
		rl.buckets[key] = b
	}

	// Refill tokens if window has passed
	if now.Sub(b.lastRefill) >= rl.config.WindowSize {
		b.tokens = rl.getLimit(c)
		b.lastRefill = now
	}

	// Check if tokens available
	if b.tokens > 0 {
		b.tokens--
		return true, b.tokens
	}

	return false, 0
}

// cleanup removes old buckets periodically
func (rl *RateLimiter) cleanup() {
	ticker := time.NewTicker(rl.config.WindowSize)
	defer ticker.Stop()

	for range ticker.C {
		rl.mu.Lock()
		now := time.Now()
		for key, b := range rl.buckets {
			if now.Sub(b.lastRefill) > rl.config.WindowSize*2 {
				delete(rl.buckets, key)
			}
		}
		rl.mu.Unlock()
	}
}
```

### middleware/recovery.go
```go
// Package middleware - Panic Recovery Middleware
// Gracefully handles panics and returns proper error responses
package middleware

import (
	"fmt"
	"runtime/debug"

	"gateway/src/models"
	"gateway/src/utils"

	"github.com/gin-gonic/gin"
)

// RecoveryMiddleware recovers from panics
func RecoveryMiddleware(logger *utils.Logger) gin.HandlerFunc {
	return func(c *gin.Context) {
		defer func() {
			if err := recover(); err != nil {
				// Log the panic with stack trace
				logger.Error("Panic recovered",
					"error", fmt.Sprintf("%v", err),
					"stack", string(debug.Stack()),
					"path", c.Request.URL.Path,
					"method", c.Request.Method,
				)

				// Return error response
				apiError := models.NewInternalError("An unexpected error occurred").
					WithDetail(fmt.Sprintf("%v", err))
				
				if requestID, exists := c.Get("request_id"); exists {
					apiError.WithRequestID(requestID.(string))
				}

				c.JSON(apiError.StatusCode, apiError.ToErrorResponse())
				c.Abort()
			}
		}()

		c.Next()
	}
}
```

### middleware/tracing.go
```go
// Package middleware - Distributed Tracing Middleware
// Integrates with Jaeger for distributed tracing
package middleware

import (
	"context"

	"github.com/gin-gonic/gin"
	"github.com/opentracing/opentracing-go"
	"github.com/opentracing/opentracing-go/ext"
)

// TracingMiddleware adds distributed tracing spans
func TracingMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		// Extract span context from headers (if exists)
		spanCtx, _ := opentracing.GlobalTracer().Extract(
			opentracing.HTTPHeaders,
			opentracing.HTTPHeadersCarrier(c.Request.Header),
		)

		// Start a new span
		span := opentracing.GlobalTracer().StartSpan(
			c.Request.URL.Path,
			ext.RPCServerOption(spanCtx),
		)
		defer span.Finish()

		// Set span tags
		ext.HTTPMethod.Set(span, c.Request.Method)
		ext.HTTPUrl.Set(span, c.Request.URL.String())
		ext.Component.Set(span, "api-gateway")

		// Store span in context
		ctx := opentracing.ContextWithSpan(context.Background(), span)
		c.Request = c.Request.WithContext(ctx)

		// Process request
		c.Next()

		// Set response tags
		ext.HTTPStatusCode.Set(span, uint16(c.Writer.Status()))
		if c.Writer.Status() >= 400 {
			ext.Error.Set(span, true)
		}
	}
}
```

---

## HANDLERS

### handlers/health.go
```go
// Package handlers - Health Check Handler
// Provides system health status including all backend services
package handlers

import (
	"net/http"
	"sync"
	"time"

	"gateway/src/config"
	"gateway/src/models"
	"gateway/src/services"

	"github.com/gin-gonic/gin"
)

var (
	startTime = time.Now()
)

// HealthHandler handles health check requests
type HealthHandler struct {
	config          *config.Config
	serviceDiscovery *services.ServiceDiscovery
}

// NewHealthHandler creates a new health handler
func NewHealthHandler(cfg *config.Config, sd *services.ServiceDiscovery) *HealthHandler {
	return &HealthHandler{
		config:          cfg,
		serviceDiscovery: sd,
	}
}

// GetHealth returns gateway health status
func (h *HealthHandler) GetHealth(c *gin.Context) {
	response := models.HealthResponse{
		Status:    "healthy",
		Timestamp: time.Now(),
		Version:   "1.0.0",
		Services:  make(map[string]models.ServiceHealth),
		Uptime:    int64(time.Since(startTime).Seconds()),
	}

	// Check all backend services in parallel
	services := config.ListAllServices()
	var wg sync.WaitGroup
	var mu sync.Mutex

	for _, serviceName := range services {
		wg.Add(1)
		go func(svc string) {
			defer wg.Done()

			health := h.checkServiceHealth(svc)
			
			mu.Lock()
			response.Services[svc] = health
			
			// If any service is unhealthy, mark gateway as degraded
			if health.Status != "healthy" {
				response.Status = "degraded"
			}
			mu.Unlock()
		}(serviceName)
	}

	wg.Wait()

	// Determine appropriate status code
	statusCode := http.StatusOK
	if response.Status == "degraded" {
		statusCode = http.StatusServiceUnavailable
	}

	c.JSON(statusCode, response)
}

// checkServiceHealth checks individual service health
func (h *HealthHandler) checkServiceHealth(serviceName string) models.ServiceHealth {
	endpoint, err := config.GetServiceEndpoint(h.config, serviceName)
	if err != nil {
		return models.ServiceHealth{
			Status:       "unknown",
			ResponseTime: 0,
			LastChecked:  time.Now(),
			Error:        err.Error(),
		}
	}

	start := time.Now()
	err = h.serviceDiscovery.CheckHealth(serviceName, endpoint.URL+endpoint.HealthEndpoint)
	duration := time.Since(start).Milliseconds()

	if err != nil {
		return models.ServiceHealth{
			Status:       "unhealthy",
			ResponseTime: duration,
			LastChecked:  time.Now(),
			Error:        err.Error(),
		}
	}

	return models.ServiceHealth{
		Status:       "healthy",
		ResponseTime: duration,
		LastChecked:  time.Now(),
	}
}

// GetLiveness returns liveness probe status
func (h *HealthHandler) GetLiveness(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"status": "alive",
		"timestamp": time.Now(),
	})
}

// GetReadiness returns readiness probe status
func (h *HealthHandler) GetReadiness(c *gin.Context) {
	// Check if critical services are available
	criticalServices := []string{
		"access-control",
		"meaning-engine",
	}

	for _, svc := range criticalServices {
		endpoint, err := config.GetServiceEndpoint(h.config, svc)
		if err != nil {
			c.JSON(http.StatusServiceUnavailable, gin.H{
				"status": "not ready",
				"reason": "Critical service configuration missing: " + svc,
			})
			return
		}

		err = h.serviceDiscovery.CheckHealth(svc, endpoint.URL+endpoint.HealthEndpoint)
		if err != nil {
			c.JSON(http.StatusServiceUnavailable, gin.H{
				"status": "not ready",
				"reason": "Critical service unavailable: " + svc,
			})
			return
		}
	}

	c.JSON(http.StatusOK, gin.H{
		"status": "ready",
		"timestamp": time.Now(),
	})
}
```

---

*Due to length constraints, this is Part 1 of the complete implementation guide. The document continues with:*

- handlers/semantic.go (Semantic API handlers)
- handlers/websocket.go (WebSocket streaming)
- services/* (Circuit breaker, discovery, load balancer, proxy)
- routes/* (Router setup and route definitions)
- utils/* (Logger, validator, errors)
- Kubernetes manifests
- Helm charts
- Dockerfile
- Makefile

**Each file follows the meaning-centric philosophy:**
- Semantic naming
- Explainable logic
- Context preservation
- Error handling with full explanations
- Tracing and monitoring built-in

Would you like me to:
1. Continue with specific sections in detail?
2. Create individual artifact files for each component?
3. Package everything into a downloadable archive?
