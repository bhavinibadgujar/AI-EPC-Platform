import os

from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.document_model import Document

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

UPLOAD_FOLDER = "app/uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    file_location = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(file_location, "wb") as f:
        f.write(await file.read())

    document = Document(
        filename=file.filename,
        filepath=file_location,
        filetype=file.content_type,
        filesize=os.path.getsize(file_location)
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return {
        "message": "File uploaded successfully",
        "document_id": document.id
    }
@router.get("/")
def get_documents(db: Session = Depends(get_db)):
    return db.query(Document).all()

@router.get("/{document_id}")
def get_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    return db.query(Document).filter(
        Document.id == document_id
    ).first()

@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    document = db.query(Document).filter(
        Document.id == document_id
    ).first()

    if not document:
        return {"message": "Document not found"}

    if os.path.exists(document.filepath):
        os.remove(document.filepath)

    db.delete(document)
    db.commit()

    return {"message": "Document deleted successfully"}










