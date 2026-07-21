from sqlalchemy.orm import Session
from sqlalchemy import or_

from backend.app.db.models import Project
from backend.app.schemas.project import ProjectCreate


def create_project(db: Session, project: ProjectCreate):
    db_project = Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def get_projects(db: Session):
    return db.query(Project).all()


def get_project(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()


def update_project(db: Session, project_id: int, project: ProjectCreate):
    db_project = db.query(Project).filter(Project.id == project_id).first()

    if not db_project:
        return None

    update_data = project.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_project, key, value)

    db.commit()
    db.refresh(db_project)

    return db_project


def delete_project(db: Session, project_id: int):
    db_project = db.query(Project).filter(Project.id == project_id).first()

    if not db_project:
        return None

    db.delete(db_project)
    db.commit()

    return db_project


def search_projects(db: Session, query: str):
    return (
        db.query(Project)
        .filter(
            or_(
                Project.name.ilike(f"%{query}%"),
                Project.location.ilike(f"%{query}%"),
                Project.status.ilike(f"%{query}%")
            )
        )
        .all()
    )