from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.db.database import get_db
from backend.app.schemas.project import ProjectCreate
from backend.app.services.project_service import (
    create_project,
    get_projects,
    get_project,
    update_project,
    delete_project,
    search_projects,
)

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


@router.post("/")
def create_new_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):
    return create_project(db, project)


@router.get("/")
def get_all_projects(
    db: Session = Depends(get_db)
):
    return get_projects(db)


@router.get("/{project_id}")
def get_single_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    project = get_project(db, project_id)

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return project


@router.put("/{project_id}")
def update_existing_project(
    project_id: int,
    project: ProjectCreate,
    db: Session = Depends(get_db)
):
    updated_project = update_project(
        db,
        project_id,
        project
    )

    if not updated_project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return updated_project


@router.delete("/{project_id}")
def delete_existing_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    deleted_project = delete_project(
        db,
        project_id
    )

    if not deleted_project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return {
        "message": "Project deleted successfully"
    }


@router.get("/search/")
def search_project(
    query: str,
    db: Session = Depends(get_db)
):
    return search_projects(db, query)