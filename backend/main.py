from fastapi import FastAPI

# Import your schedule router
from api.routes.schedule import router as schedule_router

app = FastAPI(
    title="AI EPC Platform"
)

# Register the Schedule API
app.include_router(
    schedule_router,
    prefix="/ai",
    tags=["Schedule"]
)