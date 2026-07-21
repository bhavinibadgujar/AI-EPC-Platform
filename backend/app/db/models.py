from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from backend.app.db.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False)

    documents = relationship("Document", back_populates="project", cascade="all, delete-orphan")
    compliance_flags = relationship("ComplianceFlag", back_populates="project", cascade="all, delete-orphan")
    consequences = relationship("Consequence", back_populates="project", cascade="all, delete-orphan")
    schedule_risks = relationship("ScheduleRisk", back_populates="project", cascade="all, delete-orphan")
    supply_chain = relationship("SupplyChain", back_populates="project", cascade="all, delete-orphan")
    commissioning_items = relationship("Commissioning", back_populates="project", cascade="all, delete-orphan")
    chat_history = relationship("ChatHistory", back_populates="project", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="project", cascade="all, delete-orphan")


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    filetype = Column(String)
    filesize = Column(Integer)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    project_id = Column(Integer, ForeignKey("projects.id"), default=1)

    project = relationship("Project", back_populates="documents")


class ComplianceFlag(Base):
    __tablename__ = "compliance_flags"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String(50), index=True)
    parameter = Column(String(255), nullable=False)
    requirement = Column(Text)
    required_value = Column(String(255))
    submitted_value = Column(String(255))
    severity = Column(String(50), nullable=False)
    status = Column(String(50), default="Deviation")
    source = Column(String(255))
    page = Column(Integer)
    snippet = Column(Text)
    confidence = Column(Float, default=0.85)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    project_id = Column(Integer, ForeignKey("projects.id"), default=1)

    project = relationship("Project", back_populates="compliance_flags")


class Consequence(Base):
    __tablename__ = "consequences"

    id = Column(Integer, primary_key=True, index=True)
    compliance_flag_id = Column(Integer, ForeignKey("compliance_flags.id"), nullable=True)
    affected_trades = Column(Text)
    affected_milestones = Column(Text)
    severity_score = Column(Float, default=0)
    suggested_action = Column(Text)
    project_id = Column(Integer, ForeignKey("projects.id"), default=1)

    project = relationship("Project", back_populates="consequences")


class ScheduleRisk(Base):
    __tablename__ = "schedule_risks"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String(50), index=True)
    activity_id = Column(String(100))
    activity = Column(String(255), nullable=False)
    reason = Column(Text)
    severity = Column(String(50), nullable=False)
    eta = Column(String(100))
    owner = Column(String(100))
    confidence = Column(Float, default=1.0)
    project_id = Column(Integer, ForeignKey("projects.id"), default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    project = relationship("Project", back_populates="schedule_risks")


class SupplyChain(Base):
    __tablename__ = "supply_chain"

    id = Column(Integer, primary_key=True, index=True)
    vendor = Column(String(255), nullable=False)
    package = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False)
    eta = Column(String(100))
    project_id = Column(Integer, ForeignKey("projects.id"), default=1)

    project = relationship("Project", back_populates="supply_chain")


class Commissioning(Base):
    __tablename__ = "commissioning"

    id = Column(Integer, primary_key=True, index=True)
    item = Column(String(255), nullable=False)
    owner = Column(String(100))
    progress = Column(Integer, default=0)
    status = Column(String(50), nullable=False)
    recommendation = Column(Text)
    project_id = Column(Integer, ForeignKey("projects.id"), default=1)

    project = relationship("Project", back_populates="commissioning_items")


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    project_id = Column(Integer, ForeignKey("projects.id"), default=1)

    project = relationship("Project", back_populates="chat_history")


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), default=1, nullable=False)
    filename = Column(String(255), nullable=False)
    filepath = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    compliance_score = Column(Float, nullable=False)

    project = relationship("Project", back_populates="reports")

