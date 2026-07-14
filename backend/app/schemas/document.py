from datetime import datetime
from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: int
    filename: str
    filepath: str
    filetype: str | None
    filesize: int | None
    uploaded_at: datetime

    class Config:
        from_attributes = True