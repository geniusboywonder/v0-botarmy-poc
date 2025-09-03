"""
Performance monitoring service for tracking system metrics, workflow performance,
and generating detailed analytics for the BotArmy system.
"""

import asyncio
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from collections import deque, defaultdict
from contextlib import asynccontextmanager

# Try to import psutil, fall back to mock if not available
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    # Mock psutil for environments where it's not available
    class MockPsutil:
        @staticmethod
        def cpu_percent(interval=1):
            return 0.0
        
        @staticmethod
        def virtual_memory():
            class MockMemory:
                percent = 0.0
                used = 0
                available = 1024 * 1024 * 1024  # 1GB
            return MockMemory()
        
        @staticmethod
        def disk_usage(path):
            class MockDisk:
                percent = 0.0
            return MockDisk()
    
    psutil = MockPsutil()

logger = logging.getLogger(__name__)
if not PSUTIL_AVAILABLE:
    logger.warning("psutil not available - using mock system metrics (install psutil for real metrics)")

@dataclass
class WorkflowMetric:
    """Represents a workflow execution metric."""
    workflow_id: str
    config_name: str
    session_id: str
    start_time: float
    end_time: Optional[float] = None
    status: str = "running"  # running, completed, failed, cancelled
    agents_used: List[str] = field(default_factory=list)
    artifacts_created: int = 0
    error_message: Optional[str] = None
    
    @property
    def duration(self) -> Optional[float]:
        """Get workflow duration in seconds."""
        if self.end_time:
            return self.end_time - self.start_time
        return time.time() - self.start_time if self.status == "running" else None
    
    @property
    def is_completed(self) -> bool:
        """Check if workflow is completed."""
        return self.status in ["completed", "failed", "cancelled"]

@dataclass
class SystemMetrics:
    """System resource metrics snapshot."""
    timestamp: float
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    memory_available_mb: float
    disk_usage_percent: float
    active_connections: int
    active_workflows: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "cpu_percent": self.cpu_percent,
            "memory_percent": self.memory_percent,
            "memory_used_mb": self.memory_used_mb,
            "memory_available_mb": self.memory_available_mb,
            "disk_usage_percent": self.disk_usage_percent,
            "active_connections": self.active_connections,
            "active_workflows": self.active_workflows
        }

class PerformanceMonitor:
    """
    Comprehensive performance monitoring system for BotArmy.
    Tracks workflows, system resources, connection health, and generates analytics.
    """
    
    def __init__(self, config=None):
        self.config = config or {
            "metrics_retention_hours": 24,
            "sampling_interval_seconds": 30,
            "alert_thresholds": {
                "cpu_percent": 80.0,
                "memory_percent": 85.0,
                "disk_usage_percent": 90.0,
                "workflow_failure_rate": 0.3,  # 30%
                "avg_workflow_duration_seconds": 600  # 10 minutes
            },
            "enable_alerts": True,
            "max_metrics_history": 2880  # 24 hours at 30-second intervals
        }
        
        # Metrics storage
        self.workflow_metrics: Dict[str, WorkflowMetric] = {}
        self.system_metrics_history: deque = deque(maxlen=self.config["max_metrics_history"])
        self.agent_performance: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            "total_tasks": 0,
            "successful_tasks": 0,
            "failed_tasks": 0,
            "total_duration": 0.0,
            "avg_duration": 0.0,
            "last_activity": None
        })
        
        # Performance tracking
        self.connection_manager = None
        self.status_broadcaster = None
        self.alert_handlers: List[callable] = []
        
        # Background monitoring
        self._monitoring_task = None
        self._is_monitoring = False
        self.start_time = time.time()
        
        logger.info("Performance Monitor initialized")
    
    def set_connection_manager(self, manager):
        """Set the connection manager for monitoring."""
        self.connection_manager = manager
    
    def set_status_broadcaster(self, broadcaster):
        """Set the status broadcaster for alerts."""
        self.status_broadcaster = broadcaster
    
    def add_alert_handler(self, handler: callable):
        """Add custom alert handler."""
        self.alert_handlers.append(handler)
    
    async def start_monitoring(self):
        """Start background monitoring tasks."""
        if not self._is_monitoring:
            self._is_monitoring = True
            self._monitoring_task = asyncio.create_task(self._monitoring_loop())
            logger.info("Performance monitoring started")
    
    async def stop_monitoring(self):
        """Stop background monitoring tasks."""
        self._is_monitoring = False
        if self._monitoring_task:
            self._monitoring_task.cancel()
            try:
                await self._monitoring_task
            except asyncio.CancelledError:
                pass
        logger.info("Performance monitoring stopped")
    
    async def _monitoring_loop(self):
        """Main monitoring loop."""
        while self._is_monitoring:
            try:
                await self._collect_system_metrics()
                await self._check_alerts()
                await asyncio.sleep(self.config["sampling_interval_seconds"])
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(5)  # Brief pause on error
    
    async def _collect_system_metrics(self):
        """Collect current system resource metrics."""
        try:
            # Get system metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Get application metrics
            active_connections = 0
            active_workflows = 0
            
            if self.connection_manager:
                diagnostics = self.connection_manager.get_system_diagnostics()
                active_connections = diagnostics.get("total_connections", 0)
            
            # Count running workflows
            active_workflows = sum(
                1 for metric in self.workflow_metrics.values()
                if not metric.is_completed
            )
            
            metric = SystemMetrics(
                timestamp=time.time(),
                cpu_percent=cpu_percent,
                memory_percent=memory.percent,
                memory_used_mb=memory.used / (1024 * 1024),
                memory_available_mb=memory.available / (1024 * 1024),
                disk_usage_percent=disk.percent,
                active_connections=active_connections,
                active_workflows=active_workflows
            )
            
            self.system_metrics_history.append(metric)
            
        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")
    
    async def _check_alerts(self):
        """Check for alert conditions and trigger notifications."""
        if not self.config["enable_alerts"] or not self.system_metrics_history:
            return
        
        latest_metrics = self.system_metrics_history[-1]
        thresholds = self.config["alert_thresholds"]
        alerts = []
        
        # Check resource thresholds
        if latest_metrics.cpu_percent > thresholds["cpu_percent"]:
            alerts.append(f"High CPU usage: {latest_metrics.cpu_percent:.1f}%")
        
        if latest_metrics.memory_percent > thresholds["memory_percent"]:
            alerts.append(f"High memory usage: {latest_metrics.memory_percent:.1f}%")
        
        if latest_metrics.disk_usage_percent > thresholds["disk_usage_percent"]:
            alerts.append(f"High disk usage: {latest_metrics.disk_usage_percent:.1f}%")
        
        # Check workflow performance
        recent_workflows = [
            m for m in self.workflow_metrics.values()
            if m.end_time and m.end_time > time.time() - 3600  # Last hour
        ]
        
        if recent_workflows:
            failure_rate = sum(1 for w in recent_workflows if w.status == "failed") / len(recent_workflows)
            if failure_rate > thresholds["workflow_failure_rate"]:
                alerts.append(f"High workflow failure rate: {failure_rate:.1%}")
            
            avg_duration = sum(w.duration for w in recent_workflows if w.duration) / len(recent_workflows)
            if avg_duration > thresholds["avg_workflow_duration_seconds"]:
                alerts.append(f"High average workflow duration: {avg_duration:.1f}s")
        
        # Send alerts
        for alert in alerts:
            await self._send_alert(alert)
    
    async def _send_alert(self, message: str):
        """Send alert notification."""
        logger.warning(f"Performance Alert: {message}")
        
        # Send to custom handlers
        for handler in self.alert_handlers:
            try:
                await handler(message)
            except Exception as e:
                logger.error(f"Error in alert handler: {e}")
        
        # Send to status broadcaster if available
        if self.status_broadcaster:
            try:
                await self.status_broadcaster.broadcast_agent_response(
                    "Performance Monitor",
                    f"⚠️ {message}",
                    "system_alerts"
                )
            except Exception as e:
                logger.error(f"Error broadcasting alert: {e}")
    
    @asynccontextmanager
    async def track_workflow(self, workflow_id: str, config_name: str, session_id: str):
        """Context manager for tracking workflow execution."""
        metric = WorkflowMetric(
            workflow_id=workflow_id,
            config_name=config_name,
            session_id=session_id,
            start_time=time.time()
        )
        
        self.workflow_metrics[workflow_id] = metric
        logger.debug(f"Started tracking workflow {workflow_id}")
        
        try:
            yield metric
            # Workflow completed successfully
            metric.status = "completed"
            
        except Exception as e:
            # Workflow failed
            metric.status = "failed"
            metric.error_message = str(e)
            logger.error(f"Workflow {workflow_id} failed: {e}")
            raise
        
        finally:
            metric.end_time = time.time()
            logger.debug(f"Finished tracking workflow {workflow_id}, duration: {metric.duration:.2f}s")
    
    def track_agent_task(self, agent_name: str, success: bool, duration: float):
        """Track individual agent task performance."""
        agent_stats = self.agent_performance[agent_name]
        agent_stats["total_tasks"] += 1
        agent_stats["total_duration"] += duration
        agent_stats["last_activity"] = time.time()
        
        if success:
            agent_stats["successful_tasks"] += 1
        else:
            agent_stats["failed_tasks"] += 1
        
        # Update average duration
        agent_stats["avg_duration"] = agent_stats["total_duration"] / agent_stats["total_tasks"]
    
    def get_performance_summary(self, hours: int = 1) -> Dict[str, Any]:
        """Get performance summary for the specified time period."""
        cutoff_time = time.time() - (hours * 3600)
        
        # Filter recent workflows
        recent_workflows = [
            m for m in self.workflow_metrics.values()
            if m.start_time > cutoff_time
        ]
        
        # Filter recent system metrics
        recent_system_metrics = [
            m for m in self.system_metrics_history
            if m.timestamp > cutoff_time
        ]
        
        # Calculate workflow statistics
        workflow_stats = {
            "total_workflows": len(recent_workflows),
            "completed_workflows": sum(1 for w in recent_workflows if w.status == "completed"),
            "failed_workflows": sum(1 for w in recent_workflows if w.status == "failed"),
            "running_workflows": sum(1 for w in recent_workflows if w.status == "running"),
            "avg_duration_seconds": 0.0,
            "success_rate": 0.0
        }
        
        completed_workflows = [w for w in recent_workflows if w.duration]
        if completed_workflows:
            workflow_stats["avg_duration_seconds"] = sum(w.duration for w in completed_workflows) / len(completed_workflows)
        
        if workflow_stats["total_workflows"] > 0:
            workflow_stats["success_rate"] = workflow_stats["completed_workflows"] / workflow_stats["total_workflows"]
        
        # Calculate system resource averages
        system_stats = {
            "avg_cpu_percent": 0.0,
            "avg_memory_percent": 0.0,
            "avg_memory_used_mb": 0.0,
            "avg_active_connections": 0.0,
            "max_cpu_percent": 0.0,
            "max_memory_percent": 0.0,
            "samples_count": len(recent_system_metrics)
        }
        
        if recent_system_metrics:
            system_stats["avg_cpu_percent"] = sum(m.cpu_percent for m in recent_system_metrics) / len(recent_system_metrics)
            system_stats["avg_memory_percent"] = sum(m.memory_percent for m in recent_system_metrics) / len(recent_system_metrics)
            system_stats["avg_memory_used_mb"] = sum(m.memory_used_mb for m in recent_system_metrics) / len(recent_system_metrics)
            system_stats["avg_active_connections"] = sum(m.active_connections for m in recent_system_metrics) / len(recent_system_metrics)
            system_stats["max_cpu_percent"] = max(m.cpu_percent for m in recent_system_metrics)
            system_stats["max_memory_percent"] = max(m.memory_percent for m in recent_system_metrics)
        
        return {
            "time_period_hours": hours,
            "generated_at": datetime.now().isoformat(),
            "uptime_seconds": time.time() - self.start_time,
            "workflow_stats": workflow_stats,
            "system_stats": system_stats,
            "agent_performance": dict(self.agent_performance),
            "monitoring_config": self.config
        }
    
    def get_real_time_metrics(self) -> Dict[str, Any]:
        """Get current real-time metrics."""
        latest_system = self.system_metrics_history[-1] if self.system_metrics_history else None
        
        return {
            "timestamp": time.time(),
            "system_metrics": latest_system.to_dict() if latest_system else {},
            "active_workflows": {
                wid: {
                    "workflow_id": metric.workflow_id,
                    "config_name": metric.config_name,
                    "session_id": metric.session_id,
                    "status": metric.status,
                    "duration": metric.duration,
                    "agents_used": metric.agents_used
                }
                for wid, metric in self.workflow_metrics.items()
                if not metric.is_completed
            },
            "connection_diagnostics": self.connection_manager.get_system_diagnostics() if self.connection_manager else {}
        }
    
    def cleanup_old_metrics(self, hours: int = None):
        """Clean up old metrics data."""
        hours = hours or self.config["metrics_retention_hours"]
        cutoff_time = time.time() - (hours * 3600)
        
        # Clean up old workflows
        old_workflows = [
            wid for wid, metric in self.workflow_metrics.items()
            if metric.end_time and metric.end_time < cutoff_time
        ]
        
        for wid in old_workflows:
            del self.workflow_metrics[wid]
        
        logger.info(f"Cleaned up {len(old_workflows)} old workflow metrics")
        
        # System metrics are automatically cleaned by deque maxlen
        # Agent performance is kept indefinitely for historical analysis