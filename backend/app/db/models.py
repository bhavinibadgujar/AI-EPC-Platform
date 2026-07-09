from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False)

    documents = relationship(
        "Document",
        back_populates="project",
        cascade="all, delete-orphan"
    )


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    filetype = Column(String)
    filesize = Column(Integer)

    uploaded_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    project_id = Column(
        Integer,
        ForeignKey("projects.id")
    )

    project = relationship(
        "Project",
        back_populates="documents"
    )