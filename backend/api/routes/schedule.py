from fastapi import APIRouter, UploadFile, File, HTTPException
import tempfile
import shutil
import os

from agents.schedule.service import ScheduleService

router = APIRouter()

service = ScheduleService()


@router.post("/schedule-risk")
async def analyze_schedule(
    file: UploadFile = File(...)
):

    if not file.filename.endswith(
        (".xlsx", ".xls", ".csv", ".xml")
    ):
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format."
        )

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=os.path.splitext(file.filename)[1]
    ) as temp:

        shutil.copyfileobj(file.file, temp)

        temp_path = temp.name

    try:

        result = service.analyze_schedule(temp_path)

        return result

    finally:

        if os.path.exists(temp_path):
            os.remove(temp_path)