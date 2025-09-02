# Backend Quick Start Guide

## SIMPLE START (Recommended for testing)

1. **Navigate to project root:**
   ```bash
   cd /Users/neill/Documents/AI\ Code/Projects/v0-botarmy-poc
   ```

2. **Install minimal Python dependencies:**
   ```bash
   pip install -r backend/requirements_minimal.txt
   ```

3. **Set OpenAI API Key (Optional for testing):**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

4. **Start the simplified backend server:**
   ```bash
   python backend/main_simple.py
   ```

5. **Verify backend is running:**
   - Open http://localhost:8000 in browser
   - Should see: `{"message": "BotArmy Backend v2 is running"}`

## FULL VERSION (If simple version works)

1. **Install full dependencies:**
   ```bash
   pip install -r backend/requirements.txt
   ```

2. **Start full backend:**
   ```bash
   python backend/main.py
   ```

## Test the Connection

1. Start frontend: `pnpm dev` (in separate terminal)
2. Open http://localhost:3000
3. Click "Test Backend" button - should show success message
4. Click "Test OpenAI" button - will test API key if set

## 🆕 Enhanced Features & Testing

### Security Validation Testing
```bash
# Test YAML validation
curl -X POST http://localhost:8000/api/validate-upload \
  -F "file=@your_process_config.yaml"

# Check system status with security metrics
curl http://localhost:8000/api/status
```

### Performance Monitoring
```bash
# Check connection pool statistics
curl http://localhost:8000/api/status | jq '.connection_pool'

# Monitor LLM provider health
curl http://localhost:8000/api/status | jq '.llm_providers'
```

### Workflow Testing
```bash
# Run recursion fix test
python test_workflow_recursion.py

# Run full test suite
python -m pytest backend/tests/ -v
```

## Common Issues

- **"Connection failed"**: Backend not running on port 8000
- **"OpenAI API key not found"**: Set OPENAI_API_KEY environment variable
- **Import errors**: Run `pip install -r backend/requirements.txt`

## 🚨 Troubleshooting Advanced Issues

### Recursion Depth Errors
**Symptoms**: "maximum recursion depth exceeded" in workflow execution
**Solution**: The recursion fix has been implemented. If you still see this error:

```bash
# Verify the fix is active
grep -n "validate_parameters=False" backend/legacy_workflow.py
grep -n "validate_parameters=False" backend/workflow/generic_orchestrator.py

# Run the recursion test
python test_workflow_recursion.py
```

### YAML Security Validation Failures
**Symptoms**: File upload rejected with "Security validation failed"
**Solutions**:
- Check file size (max 1MB)
- Ensure YAML depth < 10 levels
- Remove suspicious patterns or path traversal attempts
- Validate YAML syntax with: `python -c "import yaml; yaml.safe_load(open('file.yaml'))"`

### Rate Limiting Issues  
**Symptoms**: "Rate limit exceeded" errors
**Solutions**:
```bash
# Check current rate limits
curl http://localhost:8000/api/status | jq '.rate_limiting'

# Clear rate limit cache (development only)
curl -X DELETE http://localhost:8000/api/admin/clear-rate-limits
```

### Connection Pool Problems
**Symptoms**: Slow LLM responses, connection timeouts
**Solutions**:
```bash
# Check pool statistics
curl http://localhost:8000/api/status | jq '.connection_pool.statistics'

# Restart with fresh pool
python backend/main.py --reset-pools
```

### Performance Issues
**Check These Common Causes**:
1. **Missing aiohttp**: `pip install aiohttp` for connection pooling
2. **High memory usage**: Check for memory leaks in `/api/status`  
3. **Slow responses**: Monitor provider health in status endpoint

### Development vs Production
```bash
# Development mode (more logging, no rate limits)
export ENVIRONMENT=development
python backend/main.py

# Test mode (for pytest)
export ENVIRONMENT=test
python -m pytest
```

## 🔍 Diagnostic Commands

### Quick Health Check
```bash
# All-in-one status check
curl -s http://localhost:8000/api/status | jq '{
  status: .status,
  llm_healthy: (.llm_providers | map(.healthy) | all),
  rate_limits: .rate_limiting.current_usage,
  connections: .connection_pool.active_connections
}'
```

### Log Analysis
```bash
# Check for security events
grep -i "security\|suspicious\|injection" backend/logs/*.log

# Monitor performance metrics
grep -i "performance\|latency\|pool" backend/logs/*.log

# Track workflow execution
grep -i "workflow\|recursion\|prefect" backend/logs/*.log
```
