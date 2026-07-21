import os

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.db.database import get_db
from backend.app.services.document_service import (
    create_document,
    get_documents,
    get_document,
    delete_document,
    search_documents,
    filter_documents,
)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

UPLOAD_FOLDER = "app/uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    project_id: int = None,
    db: Session = Depends(get_db)
):
    file_location = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(file_location, "wb") as f:
        f.write(await file.read())

    document = create_document(
        db=db,
        filename=file.filename,
        filepath=file_location,
        filetype=file.content_type,
        filesize=os.path.getsize(file_location),
        project_id=project_id
    )

    return {
        "message": "File uploaded successfully",
        "document_id": document.id
    }


@router.get("/")
def get_all_documents(
    db: Session = Depends(get_db)
):
    return get_documents(db)


@router.get("/{document_id}")
def get_single_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    document = get_document(db, document_id)

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return document


@router.delete("/{document_id}")
def delete_single_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    document = delete_document(db, document_id)

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return {
        "message": "Document deleted successfully"
    }


@router.get("/search/")
def search_document(
    query: str,
    db: Session = Depends(get_db)
):
    return search_documents(db, query)


@router.get("/filter/")
def filter_document(
    project_id: int = None,
    filetype: str = None,
    db: Session = Depends(get_db)
):
    return filter_documents(
        db,
        project_id,
        filetype
    )