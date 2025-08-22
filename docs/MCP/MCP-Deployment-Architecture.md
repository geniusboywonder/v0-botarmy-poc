# Deployment Architecture - Production Infrastructure

**Part of:** MCP-Based Role-Constrained Agent Orchestration  
**Focus:** Production deployment strategies, scaling, and infrastructure

---

## Production Deployment Overview

This architecture supports both cloud-native and on-premises deployments with horizontal scaling for each MCP service and the orchestration engine.

### Infrastructure Requirements

**Minimum Production Setup:**
- 3-node Kubernetes cluster (or equivalent container orchestration)
- PostgreSQL cluster with read replicas
- Redis cluster for caching and session management
- Load balancer with SSL termination
- Monitoring and logging infrastructure

**Recommended Production Setup:**
- 6+ node Kubernetes cluster with auto-scaling
- Multi-region database deployment
- CDN for static assets
- Dedicated monitoring cluster
- Backup and disaster recovery systems

---

## Kubernetes Deployment Configuration

### Namespace Configuration

```yaml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: mcp-orchestration
  labels:
    app.kubernetes.io/name: mcp-orchestration
    app.kubernetes.io/part-of: agent-platform
---
apiVersion: v1
kind: Namespace
metadata:
  name: mcp-agents
  labels:
    app.kubernetes.io/name: mcp-agents
    app.kubernetes.io/part-of: agent-platform
```

### ConfigMap for Global Settings

```yaml
# global-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: mcp-global-config
  namespace: mcp-orchestration
data:
  ENVIRONMENT: "production"
  LOG_LEVEL: "INFO"
  POSTGRES_HOST: "postgresql-cluster.database.svc.cluster.local"
  REDIS_HOST: "redis-cluster.cache.svc.cluster.local"
  MONITORING_ENABLED: "true"
  RATE_LIMITING_ENABLED: "true"
  DEFAULT_LLM_MODEL: "gpt-4o"
  MAX_CONCURRENT_WORKFLOWS: "100"
  AGENT_TIMEOUT_SECONDS: "120"
```

### MCP Orchestration Engine Deployment

```yaml
# orchestration-engine-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: orchestration-engine
  namespace: mcp-orchestration
  labels:
    app: orchestration-engine
    version: v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: orchestration-engine
  template:
    metadata:
      labels:
        app: orchestration-engine
        version: v1
    spec:
      containers:
      - name: orchestration-engine
        image: mcp-platform/orchestration-engine:latest
        ports:
        - containerPort: 8000
          name: http
        - containerPort: 8001
          name: websocket
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: database-secrets
              key: connection-string
        - name: REDIS_URL
          valueFrom:
            configMapKeyRef:
              name: mcp-global-config
              key: REDIS_HOST
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: llm-secrets
              key: openai-api-key
        - name: ANTHROPIC_API_KEY
          valueFrom:
            secretKeyRef:
              name: llm-secrets
              key: anthropic-api-key
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
        volumeMounts:
        - name: config-volume
          mountPath: /app/config
        - name: logs-volume
          mountPath: /app/logs
      volumes:
      - name: config-volume
        configMap:
          name: mcp-global-config
      - name: logs-volume
        emptyDir: {}
---
apiVersion: v1
kind: Service
metadata:
  name: orchestration-engine-service
  namespace: mcp-orchestration
spec:
  selector:
    app: orchestration-engine
  ports:
  - name: http
    port: 80
    targetPort: 8000
  - name: websocket
    port: 8001
    targetPort: 8001
  type: ClusterIP
```

### MCP Agent Service Template

```yaml
# business-analyst-agent-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: business-analyst-agent
  namespace: mcp-agents
  labels:
    app: business-analyst-agent
    role: business-analyst
spec:
  replicas: 2
  selector:
    matchLabels:
      app: business-analyst-agent
  template:
    metadata:
      labels:
        app: business-analyst-agent
        role: business-analyst
    spec:
      containers:
      - name: business-analyst
        image: mcp-platform/business-analyst:latest
        ports:
        - containerPort: 3001
          name: mcp-port
        env:
        - name: ROLE_ID
          value: "business_analyst"
        - name: MCP_PORT
          value: "3001"
        - name: LLM_MODEL
          value: "gpt-4o-mini"
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: llm-secrets
              key: openai-api-key
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3001
          initialDelaySeconds: 15
          periodSeconds: 20
        readinessProbe:
          httpGet:
            path: /ready
            port: 3001
          initialDelaySeconds: 5
          periodSeconds: 5
        volumeMounts:
        - name: role-config
          mountPath: /app/config/role.yaml
          subPath: business_analyst.yaml
      volumes:
      - name: role-config
        configMap:
          name: agent-role-configs
---
apiVersion: v1
kind: Service
metadata:
  name: business-analyst-service
  namespace: mcp-agents
  labels:
    role: business-analyst
spec:
  selector:
    app: business-analyst-agent
  ports:
  - port: 3001
    targetPort: 3001
    name: mcp
  type: ClusterIP
```

### Auto-scaling Configuration

```yaml
# orchestration-engine-hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: orchestration-engine-hpa
  namespace: mcp-orchestration
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: orchestration-engine
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  - type: Pods
    pods:
      metric:
        name: websocket_connections
      target:
        type: AverageValue
        averageValue: "100"
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 25
        periodSeconds: 60
---
# agent-services-hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: mcp-agents-hpa
  namespace: mcp-agents
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: business-analyst-agent
  minReplicas: 2
  maxReplicas: 8
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 75
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 85
```

---

## Database Infrastructure

### PostgreSQL Cluster Configuration

```yaml
# postgresql-cluster.yaml
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: postgresql-cluster
  namespace: database
spec:
  instances: 3
  
  postgresql:
    parameters:
      max_connections: "200"
      shared_buffers: "256MB"
      effective_cache_size: "1GB"
      maintenance_work_mem: "64MB"
      checkpoint_completion_target: "0.9"
      wal_buffers: "16MB"
      default_statistics_target: "100"
      random_page_cost: "1.1"
      effective_io_concurrency: "200"
    
  bootstrap:
    initdb:
      database: mcp_orchestration
      owner: mcp_user
      secret:
        name: postgresql-credentials
  
  storage:
    size: 100Gi
    storageClass: fast-ssd
  
  resources:
    requests:
      memory: "2Gi"
      cpu: "1000m"
    limits:
      memory: "4Gi"
      cpu: "2000m"
  
  monitoring:
    enabled: true
  
  backup:
    target: "prefer-standby"
    retentionPolicy: "30d"
    data:
      compression: "gzip"
    wal:
      compression: "gzip"
      maxParallel: 8
```

### Database Migration Job

```yaml
# database-migration-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: database-migration
  namespace: mcp-orchestration
spec:
  template:
    spec:
      containers:
      - name: migration
        image: mcp-platform/database-migration:latest
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: database-secrets
              key: connection-string
        command:
        - /bin/sh
        - -c
        - |
          echo "Starting database migration..."
          alembic upgrade head
          echo "Migration completed successfully"
      restartPolicy: OnFailure
  backoffLimit: 3
```

---

## Load Balancer and Ingress

### Nginx Ingress Configuration

```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: mcp-orchestration-ingress
  namespace: mcp-orchestration
  annotations:
    kubernetes.io/ingress.class: "nginx"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/proxy-body-size: "50m"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "300"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "300"
    nginx.ingress.kubernetes.io/websocket-services: "orchestration-engine-service"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
spec:
  tls:
  - hosts:
    - api.mcp-platform.com
    - ws.mcp-platform.com
    secretName: mcp-platform-tls
  rules:
  - host: api.mcp-platform.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: orchestration-engine-service
            port:
              number: 80
  - host: ws.mcp-platform.com
    http:
      paths:
      - path: /ws
        pathType: Prefix
        backend:
          service:
            name: orchestration-engine-service
            port:
              number: 8001
```

### Rate Limiting Configuration

```yaml
# rate-limiting-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-rate-limiting
  namespace: ingress-nginx
data:
  nginx.conf: |
    http {
      # Rate limiting zones
      limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
      limit_req_zone $binary_remote_addr zone=ws_limit:10m rate=5r/s;
      limit_req_zone $binary_remote_addr zone=upload_limit:10m rate=2r/s;
      
      # Connection limiting
      limit_conn_zone $binary_remote_addr zone=conn_limit:10m;
      
      server {
        # API endpoints
        location /api/ {
          limit_req zone=api_limit burst=20 nodelay;
          limit_conn conn_limit 10;
        }
        
        # WebSocket connections
        location /ws {
          limit_req zone=ws_limit burst=10 nodelay;
          limit_conn conn_limit 5;
        }
        
        # File uploads
        location /upload {
          limit_req zone=upload_limit burst=5 nodelay;
          client_max_body_size 50M;
        }
      }
    }
```

---

## Monitoring and Observability

### Prometheus Configuration

```yaml
# prometheus-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: monitoring
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
      evaluation_interval: 15s
    
    rule_files:
      - "mcp_orchestration_rules.yml"
    
    scrape_configs:
    - job_name: 'orchestration-engine'
      kubernetes_sd_configs:
      - role: pod
        namespaces:
          names:
          - mcp-orchestration
      relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_app]
        action: keep
        regex: orchestration-engine
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
    
    - job_name: 'mcp-agents'
      kubernetes_sd_configs:
      - role: pod
        namespaces:
          names:
          - mcp-agents
      relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_role]
        action: keep
        regex: (business-analyst|technical-architect|developer|qa-tester)
    
    - job_name: 'postgresql'
      static_configs:
      - targets: ['postgresql-cluster.database.svc.cluster.local:5432']
      metrics_path: /metrics
      params:
        collect[]:
        - 'pg_stat_database'
        - 'pg_stat_user_tables'
        - 'pg_locks'
    
    alerting:
      alertmanagers:
      - static_configs:
        - targets:
          - alertmanager.monitoring.svc.cluster.local:9093
  
  mcp_orchestration_rules.yml: |
    groups:
    - name: mcp_orchestration_alerts
      rules:
      - alert: HighWorkflowFailureRate
        expr: (
          rate(workflow_executions_total{status="failed"}[5m]) / 
          rate(workflow_executions_total[5m])
        ) > 0.1
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High workflow failure rate detected"
          description: "Workflow failure rate is {{ $value | humanizePercentage }} over the last 5 minutes"
      
      - alert: AgentResponseTimeTooHigh
        expr: histogram_quantile(0.95, rate(agent_response_duration_seconds_bucket[5m])) > 120
        for: 3m
        labels:
          severity: warning
        annotations:
          summary: "Agent response time too high"
          description: "95th percentile agent response time is {{ $value }}s"
      
      - alert: DatabaseConnectionPoolExhausted
        expr: postgresql_active_connections / postgresql_max_connections > 0.9
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Database connection pool nearly exhausted"
          description: "Database connection usage is at {{ $value | humanizePercentage }}"
      
      - alert: MCPServiceDown
        expr: up{job=~"orchestration-engine|mcp-agents"} == 0
        for: 30s
        labels:
          severity: critical
        annotations:
          summary: "MCP service is down"
          description: "Service {{ $labels.job }} on {{ $labels.instance }} is down"
```

### Grafana Dashboard Configuration

```yaml
# grafana-dashboard-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: mcp-orchestration-dashboard
  namespace: monitoring
  labels:
    grafana_dashboard: "1"
data:
  mcp-orchestration-dashboard.json: |
    {
      "dashboard": {
        "id": null,
        "title": "MCP Orchestration Platform",
        "tags": ["mcp", "orchestration", "agents"],
        "timezone": "browser",
        "panels": [
          {
            "id": 1,
            "title": "Workflow Success Rate",
            "type": "stat",
            "targets": [
              {
                "expr": "rate(workflow_executions_total{status=\"completed\"}[5m]) / rate(workflow_executions_total[5m])",
                "legendFormat": "Success Rate"
              }
            ],
            "fieldConfig": {
              "defaults": {
                "unit": "percentunit",
                "min": 0,
                "max": 1,
                "thresholds": {
                  "steps": [
                    {"color": "red", "value": 0},
                    {"color": "yellow", "value": 0.8},
                    {"color": "green", "value": 0.95}
                  ]
                }
              }
            }
          },
          {
            "id": 2,
            "title": "Agent Response Times",
            "type": "timeseries",
            "targets": [
              {
                "expr": "histogram_quantile(0.95, rate(agent_response_duration_seconds_bucket[5m]))",
                "legendFormat": "95th percentile"
              },
              {
                "expr": "histogram_quantile(0.50, rate(agent_response_duration_seconds_bucket[5m]))",
                "legendFormat": "50th percentile"
              }
            ]
          },
          {
            "id": 3,
            "title": "Active Workflows",
            "type": "timeseries",
            "targets": [
              {
                "expr": "sum(workflow_executions_active)",
                "legendFormat": "Active Workflows"
              }
            ]
          },
          {
            "id": 4,
            "title": "Agent Utilization",
            "type": "heatmap",
            "targets": [
              {
                "expr": "rate(agent_executions_total[1m])",
                "legendFormat": "{{ agent_role }}"
              }
            ]
          },
          {
            "id": 5,
            "title": "Database Performance",
            "type": "timeseries",
            "targets": [
              {
                "expr": "rate(postgresql_queries_total[5m])",
                "legendFormat": "Queries/sec"
              },
              {
                "expr": "postgresql_active_connections",
                "legendFormat": "Active Connections"
              }
            ]
          }
        ],
        "time": {
          "from": "now-1h",
          "to": "now"
        },
        "refresh": "30s"
      }
    }
```

---

## Logging Infrastructure

### ELK Stack Configuration

```yaml
# elasticsearch-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: elasticsearch
  namespace: logging
spec:
  replicas: 3
  selector:
    matchLabels:
      app: elasticsearch
  template:
    metadata:
      labels:
        app: elasticsearch
    spec:
      containers:
      - name: elasticsearch
        image: docker.elastic.co/elasticsearch/elasticsearch:8.8.0
        env:
        - name: discovery.type
          value: single-node
        - name: ES_JAVA_OPTS
          value: "-Xms1g -Xmx1g"
        - name: xpack.security.enabled
          value: "false"
        ports:
        - containerPort: 9200
        - containerPort: 9300
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        volumeMounts:
        - name: elasticsearch-storage
          mountPath: /usr/share/elasticsearch/data
      volumes:
      - name: elasticsearch-storage
        persistentVolumeClaim:
          claimName: elasticsearch-pvc
---
# fluentd-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluentd-config
  namespace: logging
data:
  fluent.conf: |
    <source>
      @type tail
      path /var/log/containers/orchestration-engine*.log
      pos_file /var/log/fluentd-orchestration.log.pos
      tag mcp.orchestration
      format json
    </source>
    
    <source>
      @type tail
      path /var/log/containers/*mcp-agents*.log
      pos_file /var/log/fluentd-agents.log.pos
      tag mcp.agents
      format json
    </source>
    
    <filter mcp.**>
      @type parser
      key_name log
      <parse>
        @type json
      </parse>
    </filter>
    
    <filter mcp.**>
      @type record_transformer
      <record>
        hostname ${hostname}
        timestamp ${time}
        environment production
      </record>
    </filter>
    
    <match mcp.**>
      @type elasticsearch
      host elasticsearch.logging.svc.cluster.local
      port 9200
      index_name mcp-logs
      type_name _doc
      include_tag_key true
      tag_key @log_name
      <buffer>
        flush_interval 10s
        chunk_limit_size 8m
        flush_thread_count 4
      </buffer>
    </match>
```

---

## Security Configuration

### Network Policies

```yaml
# network-policies.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: mcp-orchestration-netpol
  namespace: mcp-orchestration
spec:
  podSelector:
    matchLabels:
      app: orchestration-engine
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8000
    - protocol: TCP
      port: 8001
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: mcp-agents
    ports:
    - protocol: TCP
      port: 3001
    - protocol: TCP
      port: 3002
    - protocol: TCP
      port: 3003
  - to:
    - namespaceSelector:
        matchLabels:
          name: database
    ports:
    - protocol: TCP
      port: 5432
  - to: []
    ports:
    - protocol: TCP
      port: 443  # HTTPS for external APIs
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: mcp-agents-netpol
  namespace: mcp-agents
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: mcp-orchestration
    ports:
    - protocol: TCP
      port: 3001
    - protocol: TCP
      port: 3002
    - protocol: TCP
      port: 3003
  egress:
  - to: []
    ports:
    - protocol: TCP
      port: 443  # HTTPS for LLM APIs
```

### Pod Security Standards

```yaml
# pod-security-policy.yaml
apiVersion: v1
kind: Pod
metadata:
  name: orchestration-engine
  namespace: mcp-orchestration
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    runAsGroup: 1000
    fsGroup: 1000
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: orchestration-engine
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
        - ALL
    resources:
      requests:
        memory: "512Mi"
        cpu: "500m"
      limits:
        memory: "2Gi"
        cpu: "2000m"
```

---

## Backup and Disaster Recovery

### Database Backup Configuration

```yaml
# database-backup-cronjob.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: postgresql-backup
  namespace: database
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: postgres-backup
            image: postgres:15
            env:
            - name: POSTGRES_HOST
              value: "postgresql-cluster.database.svc.cluster.local"
            - name: POSTGRES_USER
              valueFrom:
                secretKeyRef:
                  name: postgresql-credentials
                  key: username
            - name: PGPASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgresql-credentials
                  key: password
            - name: BACKUP_BUCKET
              value: "s3://mcp-platform-backups"
            command:
            - /bin/bash
            - -c
            - |
              BACKUP_FILE="mcp_orchestration_$(date +%Y%m%d_%H%M%S).sql"
              pg_dump -h $POSTGRES_HOST -U $POSTGRES_USER mcp_orchestration > /tmp/$BACKUP_FILE
              aws s3 cp /tmp/$BACKUP_FILE $BACKUP_BUCKET/database/
              
              # Cleanup old backups (keep 30 days)
              aws s3 ls $BACKUP_BUCKET/database/ | \
                awk '{print $4}' | \
                sort -r | \
                tail -n +31 | \
                xargs -I {} aws s3 rm $BACKUP_BUCKET/database/{}
            volumeMounts:
            - name: aws-credentials
              mountPath: /root/.aws
          volumes:
          - name: aws-credentials
            secret:
              secretName: aws-backup-credentials
          restartPolicy: OnFailure
```

### Configuration Backup

```yaml
# config-backup-cronjob.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: config-backup
  namespace: mcp-orchestration
spec:
  schedule: "0 3 * * *"  # Daily at 3 AM
  jobTemplate:
    spec:
      template:
        spec:
          serviceAccountName: config-backup-sa
          containers:
          - name: config-backup
            image: bitnami/kubectl:latest
            command:
            - /bin/bash
            - -c
            - |
              BACKUP_DIR="/tmp/config-backup-$(date +%Y%m%d)"
              mkdir -p $BACKUP_DIR
              
              # Backup ConfigMaps
              kubectl get configmaps -n mcp-orchestration -o yaml > $BACKUP_DIR/configmaps.yaml
              kubectl get configmaps -n mcp-agents -o yaml > $BACKUP_DIR/agent-configmaps.yaml
              
              # Backup Secrets (encrypted)
              kubectl get secrets -n mcp-orchestration -o yaml > $BACKUP_DIR/secrets.yaml
              
              # Backup Deployments and Services
              kubectl get deployments,services,ingresses -n mcp-orchestration -o yaml > $BACKUP_DIR/resources.yaml
              kubectl get deployments,services -n mcp-agents -o yaml > $BACKUP_DIR/agent-resources.yaml
              
              # Compress and upload
              tar -czf /tmp/config-backup-$(date +%Y%m%d).tar.gz -C /tmp config-backup-$(date +%Y%m%d)
              aws s3 cp /tmp/config-backup-$(date +%Y%m%d).tar.gz s3://mcp-platform-backups/config/
            volumeMounts:
            - name: aws-credentials
              mountPath: /root/.aws
          volumes:
          - name: aws-credentials
            secret:
              secretName: aws-backup-credentials
          restartPolicy: OnFailure
```

---

## Production Deployment Checklist

### Pre-Deployment Validation

```bash
#!/bin/bash
# deployment-validation.sh

echo "🔍 Pre-deployment validation checklist"

# Check Kubernetes cluster health
echo "Checking Kubernetes cluster..."
kubectl cluster-info
kubectl get nodes

# Verify required namespaces
echo "Checking namespaces..."
kubectl get namespaces | grep -E "(mcp-orchestration|mcp-agents|database|monitoring|logging)"

# Check resource quotas
echo "Checking resource availability..."
kubectl describe quota -n mcp-orchestration
kubectl describe quota -n mcp-agents

# Validate secrets
echo "Validating secrets..."
kubectl get secrets -n mcp-orchestration | grep -E "(database-secrets|llm-secrets)"

# Check database connectivity
echo "Testing database connectivity..."
kubectl run -it --rm --restart=Never postgres-test --image=postgres:15 \
  --env="PGPASSWORD=$(kubectl get secret database-secrets -o jsonpath='{.data.password}' | base64 -d)" \
  -- psql -h postgresql-cluster.database.svc.cluster.local -U mcp_user -d mcp_orchestration -c "\dt"

# Validate configuration files
echo "Validating configuration files..."
kubectl get configmaps -n mcp-orchestration
kubectl get configmaps -n mcp-agents

echo "✅ Pre-deployment validation completed"
```

### Deployment Script

```bash
#!/bin/bash
# deploy-mcp-platform.sh

set -e

echo "🚀 Starting MCP Platform Deployment"

# Function to wait for deployment to be ready
wait_for_deployment() {
    local namespace=$1
    local deployment=$2
    echo "Waiting for $deployment in $namespace to be ready..."
    kubectl rollout status deployment/$deployment -n $namespace --timeout=300s
}

# Function to wait for service to be available
wait_for_service() {
    local namespace=$1
    local service=$2
    echo "Waiting for service $service in $namespace to be available..."
    kubectl wait --for=condition=available --timeout=300s service/$service -n $namespace
}

# Step 1: Create namespaces
echo "📁 Creating namespaces..."
kubectl apply -f k8s/namespaces/

# Step 2: Apply secrets and configmaps
echo "🔐 Applying secrets and configuration..."
kubectl apply -f k8s/secrets/
kubectl apply -f k8s/configmaps/

# Step 3: Deploy database
echo "🗄️ Deploying database infrastructure..."
kubectl apply -f k8s/database/
echo "Waiting for database to be ready..."
kubectl wait --for=condition=ready pod -l app=postgresql-cluster -n database --timeout=600s

# Step 4: Run database migrations
echo "📊 Running database migrations..."
kubectl apply -f k8s/migrations/
kubectl wait --for=condition=complete job/database-migration -n mcp-orchestration --timeout=300s

# Step 5: Deploy MCP agent services
echo "🤖 Deploying MCP agent services..."
kubectl apply -f k8s/agents/
wait_for_deployment mcp-agents business-analyst-agent
wait_for_deployment mcp-agents technical-architect-agent
wait_for_deployment mcp-agents developer-agent
wait_for_deployment mcp-agents qa-tester-agent

# Step 6: Deploy orchestration engine
echo "🎯 Deploying orchestration engine..."
kubectl apply -f k8s/orchestration/
wait_for_deployment mcp-orchestration orchestration-engine

# Step 7: Deploy monitoring and logging
echo "📊 Deploying monitoring infrastructure..."
kubectl apply -f k8s/monitoring/
kubectl apply -f k8s/logging/

# Step 8: Configure ingress and load balancing
echo "🌐 Configuring ingress and load balancing..."
kubectl apply -f k8s/ingress/

# Step 9: Apply auto-scaling policies
echo "📈 Applying auto-scaling policies..."
kubectl apply -f k8s/autoscaling/

# Step 10: Run post-deployment tests
echo "🧪 Running post-deployment tests..."
./scripts/post-deployment-tests.sh

echo "✅ MCP Platform deployment completed successfully!"
echo "🌐 Platform available at: https://api.mcp-platform.com"
echo "📊 Monitoring dashboard: https://grafana.mcp-platform.com"
```

### Post-Deployment Testing

```bash
#!/bin/bash
# post-deployment-tests.sh

echo "🧪 Running post-deployment tests"

# Test orchestration engine health
echo "Testing orchestration engine health..."
HEALTH_RESPONSE=$(kubectl exec -n mcp-orchestration deployment/orchestration-engine -- curl -s http://localhost:8000/health)
if [[ $HEALTH_RESPONSE == *"healthy"* ]]; then
    echo "✅ Orchestration engine is healthy"
else
    echo "❌ Orchestration engine health check failed"
    exit 1
fi

# Test agent services
echo "Testing MCP agent services..."
AGENTS=("business-analyst" "technical-architect" "developer" "qa-tester")
for agent in "${AGENTS[@]}"; do
    AGENT_HEALTH=$(kubectl exec -n mcp-agents deployment/${agent}-agent -- curl -s http://localhost:3001/health)
    if [[ $AGENT_HEALTH == *"healthy"* ]]; then
        echo "✅ $agent agent is healthy"
    else
        echo "❌ $agent agent health check failed"
        exit 1
    fi
done

# Test database connectivity
echo "Testing database connectivity..."
DB_TEST=$(kubectl run -it --rm --restart=Never db-test --image=postgres:15 \
    --env="PGPASSWORD=$(kubectl get secret database-secrets -n database -o jsonpath='{.data.password}' | base64 -d)" \
    -- psql -h postgresql-cluster.database.svc.cluster.local -U mcp_user -d mcp_orchestration -c "SELECT 1;" 2>/dev/null)
if [[ $? -eq 0 ]]; then
    echo "✅ Database connectivity test passed"
else
    echo "❌ Database connectivity test failed"
    exit 1
fi

# Test external API access
echo "Testing external API access..."
kubectl run -it --rm --restart=Never api-test --image=curlimages/curl:latest \
    -- curl -s https://api.openai.com/v1/models -H "Authorization: Bearer test" >/dev/null 2>&1
if [[ $? -eq 0 ]]; then
    echo "✅ External API access test passed"
else
    echo "❌ External API access test failed"
    exit 1
fi

# Test ingress connectivity
echo "Testing ingress connectivity..."
INGRESS_IP=$(kubectl get ingress mcp-orchestration-ingress -n mcp-orchestration -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
if [[ -n "$INGRESS_IP" ]]; then
    echo "✅ Ingress configured with IP: $INGRESS_IP"
else
    echo "❌ Ingress IP not assigned"
    exit 1
fi

echo "✅ All post-deployment tests passed!"
```

---

## Multi-Region Deployment

### Global Load Balancer Configuration

```yaml
# global-load-balancer.yaml
apiVersion: v1
kind: Service
metadata:
  name: global-load-balancer
  annotations:
    cloud.google.com/global-access: "true"
    cloud.google.com/backend-config: '{"default": "mcp-backend-config"}'
spec:
  type: LoadBalancer
  loadBalancerClass: gce-global
  ports:
  - port: 80
    targetPort: 8000
    name: http
  - port: 443
    targetPort: 8000
    name: https
  selector:
    app: orchestration-engine
---
apiVersion: cloud.google.com/v1
kind: BackendConfig
metadata:
  name: mcp-backend-config
spec:
  healthCheck:
    checkIntervalSec: 15
    timeoutSec: 5
    healthyThreshold: 2
    unhealthyThreshold: 3
    type: HTTP
    requestPath: /health
    port: 8000
  connectionDraining:
    drainingTimeoutSec: 300
  sessionAffinity:
    affinityType: "CLIENT_IP"
    affinityCookieTtlSec: 3600
```

### Region-Specific Configurations

```yaml
# us-east-cluster-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: region-config
  namespace: mcp-orchestration
data:
  REGION: "us-east-1"
  DATABASE_READ_REPLICA: "postgresql-read-replica-us-east.database.svc.cluster.local"
  REDIS_CLUSTER: "redis-us-east.cache.svc.cluster.local"
  LLM_PROVIDER_PREFERENCE: "openai"  # Lower latency to OpenAI from US East
  BACKUP_REGION: "us-west-2"
---
# eu-west-cluster-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: region-config
  namespace: mcp-orchestration
data:
  REGION: "eu-west-1"
  DATABASE_READ_REPLICA: "postgresql-read-replica-eu-west.database.svc.cluster.local"
  REDIS_CLUSTER: "redis-eu-west.cache.svc.cluster.local"
  LLM_PROVIDER_PREFERENCE: "anthropic"  # Data residency considerations
  BACKUP_REGION: "eu-central-1"
```

---

## Performance Optimization

### Resource Optimization Script

```bash
#!/bin/bash
# optimize-resources.sh

echo "🔧 Optimizing MCP Platform Resources"

# Analyze current resource usage
echo "📊 Current resource usage:"
kubectl top nodes
kubectl top pods -n mcp-orchestration
kubectl top pods -n mcp-agents

# Optimize based on usage patterns
echo "⚡ Applying optimizations..."

# Update resource requests/limits based on actual usage
kubectl patch deployment orchestration-engine -n mcp-orchestration -p '{
  "spec": {
    "template": {
      "spec": {
        "containers": [{
          "name": "orchestration-engine",
          "resources": {
            "requests": {"memory": "1Gi", "cpu": "750m"},
            "limits": {"memory": "3Gi", "cpu": "2500m"}
          }
        }]
      }
    }
  }
}'

# Enable vertical pod autoscaling for agents
kubectl apply -f - <<EOF
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: business-analyst-vpa
  namespace: mcp-agents
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: business-analyst-agent
  updatePolicy:
    updateMode: "Auto"
  resourcePolicy:
    containerPolicies:
    - containerName: business-analyst
      maxAllowed:
        memory: 2Gi
        cpu: 1500m
      minAllowed:
        memory: 128Mi
        cpu: 100m
EOF

# Configure cluster autoscaling
kubectl apply -f - <<EOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: cluster-autoscaler-status
  namespace: kube-system
data:
  scale-down-delay-after-add: "10m"
  scale-down-unneeded-time: "10m"
  scale-down-delay-after-failure: "3m"
  max-node-provision-time: "15m"
  scale-down-utilization-threshold: "0.5"
EOF

echo "✅ Resource optimization completed"
```

### Cache Optimization

```yaml
# redis-cache-optimization.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis-cache
  namespace: cache
spec:
  replicas: 3
  selector:
    matchLabels:
      app: redis-cache
  template:
    metadata:
      labels:
        app: redis-cache
    spec:
      containers:
      - name: redis
        image: redis:7-alpine
        args:
        - redis-server
        - --maxmemory 2gb
        - --maxmemory-policy allkeys-lru
        - --save ""  # Disable persistence for cache
        - --appendonly no
        - --tcp-keepalive 60
        - --timeout 300
        ports:
        - containerPort: 6379
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          tcpSocket:
            port: 6379
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          exec:
            command:
            - redis-cli
            - ping
          initialDelaySeconds: 5
          periodSeconds: 5
```

---

## Disaster Recovery Procedures

### Automated Failover Configuration

```yaml
# disaster-recovery-runbook.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: disaster-recovery-runbook
  namespace: mcp-orchestration
data:
  runbook.md: |
    # MCP Platform Disaster Recovery Runbook
    
    ## Incident Response Procedures
    
    ### Database Failure
    1. Check primary database status: `kubectl get pods -n database`
    2. Promote read replica: `kubectl exec -n database postgresql-cluster-2 -- pg_promote`
    3. Update connection strings in applications
    4. Verify application connectivity
    
    ### Agent Service Failure
    1. Check agent health: `kubectl get pods -n mcp-agents`
    2. Scale up healthy replicas: `kubectl scale deployment <agent>-agent --replicas=4`
    3. Route traffic away from failed instances
    4. Investigate logs: `kubectl logs -n mcp-agents deployment/<agent>-agent`
    
    ### Complete Region Failure
    1. Activate standby region: `./scripts/activate-standby-region.sh`
    2. Update DNS records to point to standby region
    3. Restore from latest backup: `./scripts/restore-from-backup.sh`
    4. Verify all services are operational
    
    ### Recovery Validation
    1. Run health checks: `./scripts/health-check-all.sh`
    2. Execute integration tests: `./scripts/integration-tests.sh`
    3. Monitor metrics for 30 minutes
    4. Document incident and lessons learned
```

### Backup Restoration Script

```bash
#!/bin/bash
# restore-from-backup.sh

set -e

BACKUP_DATE=${1:-$(date -d "yesterday" +%Y%m%d)}
BACKUP_BUCKET="s3://mcp-platform-backups"

echo "🔄 Starting disaster recovery from backup: $BACKUP_DATE"

# Step 1: Stop all services
echo "⏹️ Stopping services..."
kubectl scale deployment orchestration-engine --replicas=0 -n mcp-orchestration
kubectl scale deployment --all --replicas=0 -n mcp-agents

# Step 2: Restore database
echo "🗄️ Restoring database..."
aws s3 cp $BACKUP_BUCKET/database/mcp_orchestration_${BACKUP_DATE}_*.sql /tmp/restore.sql

kubectl exec -n database postgresql-cluster-1 -- psql -U mcp_user -d mcp_orchestration -c "
    DROP SCHEMA public CASCADE;
    CREATE SCHEMA public;
"

kubectl exec -i -n database postgresql-cluster-1 -- psql -U mcp_user -d mcp_orchestration < /tmp/restore.sql

# Step 3: Restore configurations
echo "⚙️ Restoring configurations..."
aws s3 cp $BACKUP_BUCKET/config/config-backup-${BACKUP_DATE}.tar.gz /tmp/
tar -xzf /tmp/config-backup-${BACKUP_DATE}.tar.gz -C /tmp/

kubectl apply -f /tmp/config-backup-${BACKUP_DATE}/configmaps.yaml
kubectl apply -f /tmp/config-backup-${BACKUP_DATE}/agent-configmaps.yaml

# Step 4: Restart services
echo "🚀 Restarting services..."
kubectl scale deployment orchestration-engine --replicas=3 -n mcp-orchestration
kubectl scale deployment --all --replicas=2 -n mcp-agents

# Step 5: Verify restoration
echo "✅ Verifying restoration..."
./scripts/post-deployment-tests.sh

echo "✅ Disaster recovery completed successfully!"
```

This comprehensive deployment architecture provides production-ready infrastructure for the MCP-based agent orchestration platform, with robust monitoring, security, scaling, and disaster recovery capabilities.