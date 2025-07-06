
from pydantic import BaseModel

class ScreenshotRequest(BaseModel):
    url: str
    webhook_url: str

class ScreenshotStatus(BaseModel):
    job_id: str
    status: str

class ScreenshotResult(BaseModel):
    file_name: str
    timestamp: str
    url: str
    