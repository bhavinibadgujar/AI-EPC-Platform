import os

from sqlalchemy.orm import Session
from sqlalchemy import and_

from backend.app.db.models import Document


def create_document(
    db: Session,
    filename: str,
    filepath: str,
    filetype: str,
    filesize: int,
    project_id: int = None
):
    document = Document(
        filename=filename,
        filepath=filepath,
        filetype=filetype,
        filesize=filesize,
        project_id=project_id
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document


def get_documents(db: Session):
    return db.query(Document).all()


def get_document(db: Session, document_id: int):
    return db.query(Document).filter(
        Document.id == document_id
    ).first()


def delete_document(db: Session, document_id: int):
    document = db.query(Document).filter(
        Document.id == document_id
    ).first()

    if not document:
        return None

    if os.path.exists(document.filepath):
        os.remove(document.filepath)

    db.delete(document)
    db.commit()

    return document


def search_documents(db: Session, query: str):
    return (
        db.query(Document)
        .filter(
            Document.filename.ilike(f"%{query}%")
        )
        .all()
    )


def filter_documents(
    db: Session,
    project_id: int = None,
    filetype: str = None
):
    query = db.query(Document)

    filters = []

    if project_id is not None:
        filters.append(Document.project_id == project_id)

    if filetype is not None:
        filters.append(Document.filetype == filetype)

    if filters:
        query = query.filter(and_(*filters))

    return query.all()