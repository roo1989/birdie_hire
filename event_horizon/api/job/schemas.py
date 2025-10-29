import uuid
from datetime import datetime
from pydantic import BaseModel, Field

from event_horizon.db.models.job import JobStatus

class UploadResponse(BaseModel):
    job_id: uuid.UUID = Field(..., description="Job ID")

class JobStatusResponse(BaseModel):
    job_id: uuid.UUID
    file_name: str
    status: JobStatus
    created_at: datetime | None = None
    completed_at: datetime | None = None

    class Config:
        orm_mode = True