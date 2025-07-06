import time
import os
import requests
from pathlib import Path
from app.database import jobs

screenshot_dir = Path("screenshots")
screenshot_dir.mkdir(exist_ok=True)

def simulate_screenshot_capture(job_id: str, url: str, webhook_url: str):
    try:
        time.sleep(5)
        screenshot_path = screenshot_dir / f"{job_id}.png"
        with open(screenshot_path, "wb") as f:
            f.write(os.urandom(1024))
        jobs[job_id]["status"] = "completed"
        requests.post(webhook_url, json={
            "job_id": job_id,
            "status": "completed",
            "screenshot_url": f"http://localhost:8000/screenshots/{job_id}"
        })
    except Exception:
        jobs[job_id]["status"] = "failed"