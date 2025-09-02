import uuid
from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    UUID,
)
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()

class WorkflowSession(Base):
    __tablename__ = 'workflow_sessions'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    process_name = Column(String(100), nullable=False)
    session_type = Column(String(50), nullable=False) # 'standard' or 'interactive'
    current_stage = Column(String(50))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class HITLCheckpoint(Base):
    __tablename__ = 'hitl_checkpoints'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey('workflow_sessions.id'), nullable=False)
    stage_name = Column(String(50), nullable=False)
    status = Column(String(50), default='pending') # 'pending', 'approved', 'rejected', 'timeout'
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    resolved_at = Column(DateTime)

class ScaffoldedArtifact(Base):
    __tablename__ = 'artifacts_scaffolded'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey('workflow_sessions.id'), nullable=False)
    artifact_name = Column(String(200), nullable=False)
    stage_name = Column(String(50), nullable=False)
    status = Column(String(50), default='scaffolded') # 'scaffolded', 'in_progress', 'completed'
    file_path = Column(String(500))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
