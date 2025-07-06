
from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from uuid import uuid4
from pathlib import Path
from app.models import ScreenshotRequest
from app.database import jobs
from app.tasks import simulate_screenshot_capture

router = APIRouter()
screenshot_dir = Path("screenshots")

@router.post("/screenshots")
def submit_screenshot(req: ScreenshotRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid4())
    jobs[job_id] = {"status": "pending", "url": req.url, "webhook_url": req.webhook_url}
    background_tasks.add_task(simulate_screenshot_capture, job_id, req.url, req.webhook_url)
    return {"job_id": job_id, "status": "queued"}

@router.get("/screenshots/{job_id}/status")
def check_status(job_id: str):
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"job_id": job_id, "status": job["status"]}

@router.get("/screenshots/{job_id}")
def get_screenshot(job_id: str):
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    screenshot_path = screenshot_dir / f"{job_id}.png"
    if not screenshot_path.exists():
        raise HTTPException(status_code=404, detail="Screenshot not available")
    return FileResponse(screenshot_path, media_type="image/png")