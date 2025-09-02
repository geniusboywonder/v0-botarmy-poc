# BotArmy Workflow Recursion Fix

## Problem
The `botarmy_workflow` function was experiencing a `maximum recursion depth exceeded` error that would repeat approximately 100 times. The error was occurring in FastAPI's `jsonable_encoder` function during Prefect workflow parameter serialization.

## Root Cause
The recursion was caused by circular references in the workflow parameters, specifically:
1. **AgentStatusBroadcaster**: Contains a reference to `connection_manager`
2. **Connection Manager**: Likely contains references back to broadcasters or other components
3. **FastAPI jsonable_encoder**: When Prefect tries to serialize workflow parameters, the encoder gets stuck in an infinite loop trying to serialize these circular references

## Error Pattern
```
File ".../fastapi/encoders.py", line 289, in jsonable_encoder
File ".../fastapi/encoders.py", line 333, in jsonable_encoder  
File ".../fastapi/encoders.py", line 289, in jsonable_encoder
File ".../fastapi/encoders.py", line 333, in jsonable_encoder
[Repeats infinitely]
```

## Solution Implemented

### 1. Disabled Prefect Parameter Validation
Modified both workflow decorators to disable parameter serialization:

```python
@prefect.flow(name="BotArmy SDLC Workflow with HITL", persist_result=False, validate_parameters=False)
```

**Files Changed:**
- `backend/legacy_workflow.py:66`
- `backend/workflow/generic_orchestrator.py:13`

### 2. Created Serialization-Safe Wrapper (Backup Solution)
Created `backend/serialization_safe_wrapper.py` with a wrapper class that prevents circular reference serialization. This provides a fallback approach if parameter validation needs to be re-enabled in the future.

### 3. Added Parameter Unwrapping
Both workflows now check for and unwrap serialization-safe wrappers at runtime:

```python
# Unwrap status_broadcaster if it's wrapped to prevent circular reference serialization
if hasattr(status_broadcaster, 'get_wrapped_object'):
    status_broadcaster = status_broadcaster.get_wrapped_object()
    logger.info("Unwrapped status_broadcaster from serialization-safe wrapper")
```

## Test Results
The test `test_workflow_recursion.py` successfully reproduces the issue and confirms the fix:
- ✅ **Before**: `maximum recursion depth exceeded` error
- ✅ **After**: Normal workflow execution (fails with expected API authentication errors instead of recursion)

## Impact
- **Positive**: Eliminates the infinite recursion crash that prevented workflow execution
- **Minimal**: Disabling parameter validation is safe for this use case as the workflow parameters are trusted internal objects
- **Performance**: No performance impact; may be slightly faster without parameter serialization overhead

## Prevention
The fix prevents future recursion issues by:
1. Avoiding FastAPI serialization of complex objects with potential circular references
2. Providing a wrapper pattern for future use cases requiring parameter serialization
3. Adding logging to detect when wrapped parameters are being used

## Files Modified
1. `backend/legacy_workflow.py` - Added flow options and parameter unwrapping
2. `backend/workflow/generic_orchestrator.py` - Added flow options and parameter unwrapping  
3. `backend/main.py` - Added wrapper imports (ready for future use)
4. `backend/serialization_safe_wrapper.py` - New utility for safe parameter wrapping
5. `test_workflow_recursion.py` - Test to reproduce and verify the fix

## Verification
The fix has been tested and confirmed to resolve the recursion issue. The workflow now executes normally and fails gracefully with expected errors (like API authentication failures) rather than crashing with recursion depth exceeded.