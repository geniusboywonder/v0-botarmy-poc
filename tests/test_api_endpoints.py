import pytest
from fastapi.testclient import TestClient
from backend.main import app
from unittest.mock import patch, AsyncMock
import backend.main as main_module

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "BotArmy" in response.json()["message"]
    assert "features" in response.json()

def test_read_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert "environment" in response.json()
    assert "port" in response.json()
    assert "timestamp" in response.json()

def test_read_api_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert "services" in response.json()

def test_read_api_status(client):
    response = client.get("/api/status")
    assert response.status_code == 200
    assert "active_workflows" in response.json()
    assert "environment" in response.json()
    assert "features_available" in response.json()

def test_read_api_config(client):
    response = client.get("/api/config")
    assert response.status_code == 200
    assert "agents" in response.json()
    assert "system" in response.json()

def test_update_api_config(client):
    config_data = {
        "system": {"debug": True},
        "agents": []
    }
    response = client.post("/api/config", json=config_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Updated: agent_configurations"

def test_refresh_api_config(client):
    response = client.post("/api/config/refresh")
    assert response.status_code == 200
    assert response.json()["message"] == "Configuration cache refreshed from .env file"

def test_validate_upload(client):
    upload_data = {
        "filename": "test.txt",
        "content": "This is a test file content."
    }
    response = client.post("/api/uploads/validate", json=upload_data)
    assert response.status_code == 200
    assert response.json()["status"] == "allowed"

def test_get_rate_limit_status(client):
    identifier = "test_user"
    response = client.get(f"/api/uploads/rate-limit/{identifier}")
    assert response.status_code == 200
    assert "identifier_hash" in response.json()
    assert "limits" in response.json()
    assert "max_uploads_per_hour" in response.json()["limits"]

def test_get_upload_metrics(client):
    response = client.get("/api/uploads/metrics")
    assert response.status_code == 200
    assert "upload_metrics" in response.json()
    assert "total_uploads_allowed" in response.json()["upload_metrics"]
    assert "total_uploads_blocked" in response.json()["upload_metrics"]
    assert "total_size_uploaded_mb" in response.json()["upload_metrics"]

def test_list_interactive_sessions(client):
    response = client.get("/api/interactive/sessions")
    assert response.status_code == 200
    assert "sessions" in response.json()
    assert isinstance(response.json()["sessions"], list)
    assert response.json()["total_count"] == 0

def test_get_interactive_session_status(client):
    session_id = "test_session_123"
    mock_session_status = {
        "session_id": session_id,
        "status": "waiting_for_answer",
        "current_question": {"id": "q1", "text": "What is your name?"}
    }
    
    with patch.dict(main_module.active_workflows, clear=True):
        mock_orchestrator = type('MockOrchestrator', (object,), {})
        mock_orchestrator.session_manager = type('MockSessionManager', (object,), {})
        mock_orchestrator.session_manager.get_session_status = lambda sid: mock_session_status if sid == session_id else None
        
        main_module.active_workflows[session_id] = {
            "orchestrator": mock_orchestrator,
            "status": "running"
        }
        
        response = client.get(f"/api/interactive/sessions/{session_id}/status")
        assert response.status_code == 200
        assert response.json() == mock_session_status

        # Test for non-existent session
        response = client.get("/api/interactive/sessions/non_existent_session/status")
        assert response.status_code == 404

class MockSessionManager:
    def __init__(self):
        self.submit_answer_called_with = None
        self.cancel_session_called_with = None

    async def submit_answer(self, session_id, question_id, answer_text):
        self.submit_answer_called_with = (session_id, question_id, answer_text)
        return True

    def get_session_status(self, session_id):
        return {
            "session_id": session_id,
            "status": "processing_answer"
        }
    
    async def cancel_session(self, session_id):
        self.cancel_session_called_with = session_id
        return True

def test_submit_interactive_answer(client):
    session_id = "test_session_456"
    answer_data = {"question_id": "q1", "answer": "My name is Test."}
    
    with patch.dict(main_module.active_workflows, clear=True):
        mock_session_manager_instance = MockSessionManager()

        mock_orchestrator = type('MockOrchestrator', (object,), {})
        mock_orchestrator.session_manager = mock_session_manager_instance

        main_module.active_workflows[session_id] = {
            "orchestrator": mock_orchestrator,
            "status": "running"
        }

        response = client.post(f"/api/interactive/sessions/{session_id}/answers", json=answer_data)
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert response.json()["message"] == "Answer submitted successfully"
        assert mock_session_manager_instance.submit_answer_called_with == (session_id, "q1", "My name is Test.")

        # Test for non-existent session
        response = client.post("/api/interactive/sessions/non_existent_session/answers", json=answer_data)
        assert response.status_code == 404

def test_cancel_interactive_session(client):
    session_id = "test_session_789"
    
    with patch.dict(main_module.active_workflows, clear=True):
        mock_session_manager_instance = MockSessionManager()

        mock_orchestrator = type('MockOrchestrator', (object,), {})
        mock_orchestrator.session_manager = mock_session_manager_instance

        main_module.active_workflows[session_id] = {
            "orchestrator": mock_orchestrator,
            "status": "running"
        }

        response = client.post(f"/api/interactive/sessions/{session_id}/cancel")
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert response.json()["message"] == "Interactive session cancelled"
        assert mock_session_manager_instance.cancel_session_called_with == session_id

        # Test for non-existent session
        response = client.post("/api/interactive/sessions/non_existent_session/cancel")
        assert response.status_code == 404

def test_get_realtime_metrics(client):
    mock_metrics = {"cpu_usage": 0.5, "memory_usage": 0.7}
    with patch('backend.main.app.state.performance_monitor') as mock_performance_monitor:
        mock_performance_monitor.get_real_time_metrics.return_value = mock_metrics
        response = client.get("/api/performance/metrics/realtime")
        assert response.status_code == 200
        assert response.json() == mock_metrics

def test_get_performance_summary(client):
    mock_summary = {"total_requests": 100, "average_response_time": 0.1}
    with patch('backend.main.app.state.performance_monitor') as mock_performance_monitor:
        mock_performance_monitor.get_performance_summary.return_value = mock_summary
        
        # Test with valid hours
        response = client.get("/api/performance/summary?hours=24")
        assert response.status_code == 200
        assert response.json() == mock_summary
        mock_performance_monitor.get_performance_summary.assert_called_with(24)

        # Test with invalid hours
        response = client.get("/api/performance/summary?hours=0")
        assert response.status_code == 400
        response = client.get("/api/performance/summary?hours=169")
        assert response.status_code == 400

class MockWorkflowMetric:
    def __init__(self, workflow_id, config_name, session_id, status, start_time, end_time, duration, agents_used, artifacts_created, error_message, is_completed):
        self.workflow_id = workflow_id
        self.config_name = config_name
        self.session_id = session_id
        self.status = status
        self.start_time = start_time
        self.end_time = end_time
        self.duration = duration
        self.agents_used = agents_used
        self.artifacts_created = artifacts_created
        self.error_message = error_message
        self.is_completed = is_completed

def test_get_workflow_metrics(client):
    workflow_id = "test_workflow_123"
    mock_workflow_metric_instance = MockWorkflowMetric(
        workflow_id=workflow_id,
        config_name="sdlc",
        session_id="test_session_abc",
        status="completed",
        start_time="2025-09-10T10:00:00Z",
        end_time="2025-09-10T10:05:00Z",
        duration=300,
        agents_used=["Analyst", "Developer"],
        artifacts_created=["requirements.md"],
        error_message=None,
        is_completed=True
    )
    
    with patch('backend.main.app.state.performance_monitor') as mock_performance_monitor:
        mock_performance_monitor.workflow_metrics = {workflow_id: mock_workflow_metric_instance}
        
        response = client.get(f"/api/performance/workflows/{workflow_id}")
        assert response.status_code == 200
        assert response.json() == {
            "workflow_id": mock_workflow_metric_instance.workflow_id,
            "config_name": mock_workflow_metric_instance.config_name,
            "session_id": mock_workflow_metric_instance.session_id,
            "status": mock_workflow_metric_instance.status,
            "start_time": mock_workflow_metric_instance.start_time,
            "end_time": mock_workflow_metric_instance.end_time,
            "duration": mock_workflow_metric_instance.duration,
            "agents_used": mock_workflow_metric_instance.agents_used,
            "artifacts_created": mock_workflow_metric_instance.artifacts_created,
            "error_message": mock_workflow_metric_instance.error_message,
            "is_completed": mock_workflow_metric_instance.is_completed
        }

        # Test for non-existent workflow
        response = client.get("/api/performance/workflows/non_existent_workflow")
        assert response.status_code == 404

def test_get_agent_performance(client):
    mock_agent_performance = {
        "Analyst": {"tasks_completed": 5, "avg_time": 10.5},
        "Developer": {"tasks_completed": 8, "avg_time": 15.2}
    }
    with patch('backend.main.app.state.performance_monitor') as mock_performance_monitor:
        mock_performance_monitor.agent_performance = mock_agent_performance
        response = client.get("/api/performance/agents")
        assert response.status_code == 200
        assert response.json()["agents"] == mock_agent_performance
        assert "timestamp" in response.json()

def test_get_connection_diagnostics(client):
    mock_system_diagnostics = {"total_connections": 5, "active_websockets": 3}
    mock_client_diagnostics = {"client_id": "test_client", "status": "connected"}

    with patch('backend.main.app.state.manager') as mock_manager:
        # Test system-wide diagnostics
        mock_manager.get_system_diagnostics.return_value = mock_system_diagnostics
        response = client.get("/api/performance/connections")
        assert response.status_code == 200
        assert response.json() == mock_system_diagnostics

        # Test specific client diagnostics
        mock_manager.get_connection_diagnostics.return_value = mock_client_diagnostics
        response = client.get("/api/performance/connections?client_id=test_client")
        assert response.status_code == 200
        assert response.json() == mock_client_diagnostics

        # Test non-existent client
        mock_manager.get_connection_diagnostics.return_value = {"error": "Client not found"}
        response = client.get("/api/performance/connections?client_id=non_existent")
        assert response.status_code == 404

def test_cleanup_performance_data(client):
    with patch('backend.main.app.state.performance_monitor') as mock_performance_monitor:
        mock_performance_monitor.cleanup_old_metrics.return_value = None
        
        # Test with valid hours
        response = client.post("/api/performance/cleanup?hours=24")
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert "message" in response.json()
        mock_performance_monitor.cleanup_old_metrics.assert_called_with(24)

        # Test with invalid hours
        response = client.post("/api/performance/cleanup?hours=0")
        assert response.status_code == 400
        response = client.post("/api/performance/cleanup?hours=8761")
        assert response.status_code == 400

def test_get_dashboard_data(client):
    mock_realtime_metrics = {"cpu_usage": 0.6}
    mock_summary_1h = {"total_requests": 50}
    mock_summary_24h = {"total_requests": 500}
    mock_connection_diagnostics = {"total_connections": 10}
    mock_agent_performance = {"Analyst": {"tasks_completed": 10}}
    mock_llm_metrics = {"total_requests": 1000}
    mock_upload_metrics = {"total_uploads_allowed": 20}

    with (patch('backend.main.app.state.performance_monitor') as mock_performance_monitor,
          patch('backend.main.app.state.manager') as mock_manager,
          patch('backend.main.app.state.upload_rate_limiter') as mock_upload_rate_limiter,
          patch('backend.main.app.state.llm_service') as mock_llm_service):

        mock_performance_monitor.get_real_time_metrics.return_value = mock_realtime_metrics
        mock_performance_monitor.get_performance_summary.side_effect = [mock_summary_1h, mock_summary_24h]
        mock_manager.get_system_diagnostics.return_value = mock_connection_diagnostics
        mock_performance_monitor.agent_performance = mock_agent_performance
        mock_llm_service.get_performance_metrics.return_value = mock_llm_metrics
        mock_upload_rate_limiter.get_global_metrics.return_value = mock_upload_metrics
        mock_performance_monitor.start_time = 0 # Mock start time for uptime calculation
        mock_performance_monitor._is_monitoring = True # Mock monitoring status
        mock_performance_monitor.workflow_metrics = {"wf1": type('MockWorkflow', (object,), {"is_completed": False})()}

        response = client.get("/api/performance/dashboard")
        assert response.status_code == 200
        response_json = response.json()

        assert "dashboard_generated_at" in response_json
        assert response_json["realtime_metrics"] == mock_realtime_metrics
        assert response_json["summary_1h"] == mock_summary_1h
        assert response_json["summary_24h"] == mock_summary_24h
        assert response_json["connection_diagnostics"] == mock_connection_diagnostics
        assert response_json["agent_performance"] == mock_agent_performance
        assert response_json["llm_metrics"] == mock_llm_metrics
        assert response_json["upload_metrics"] == mock_upload_metrics
        assert "system_info" in response_json
        assert response_json["system_info"]["monitoring_active"] == True
        assert response_json["system_info"]["active_workflows_count"] == 1