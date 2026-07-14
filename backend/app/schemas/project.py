from pydantic import BaseModel

class ProjectBase(BaseModel):
    name: str
    location: str
    status: str

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int

    class Config:
        from_attributes = True