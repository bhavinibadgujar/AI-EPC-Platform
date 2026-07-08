from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.db.database import Base
from app.db.models import Project

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String, nullable=False)

    filepath = Column(String, nullable=False)

    filetype = Column(String)

    filesize = Column(Integer)

    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    project_id = Column(Integer, ForeignKey("projects.id"))