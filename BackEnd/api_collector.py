from fastapi import APIRouter, Form, HTTPException
from database import db_access as db
import time
import random
import os

router = APIRouter()
def generate_unique_batch_id() -> str:
    """Generate a unique numeric batch ID based on timestamp + random digits."""
    timestamp = int(time.time() * 1000)  # milliseconds
    rand_suffix = random.randint(100, 999)
    return f"{timestamp}{rand_suffix}"

@router.post("/submit/collector")
async def submit_collector(
    parent_batch_id: str = Form(...),
    crop_name: str = Form(...),
    weight: str = Form(...),
    stakeholder: str = Form(...),  # should be "collector"
):
    # 1️⃣ Simulate GPS coordinates (or replace with real logic if needed)
    latitude, longitude = None, None  # or some fixed/default value if needed
    batch_id = generate_unique_batch_id()
    # 2️⃣ Prepare extra_data
    extra_data = {"crop_name": crop_name}

    # 3️⃣ Insert into DB
    try:
        batch_id, metadata, hash_key = db.insert_batch(
            batch_id=batch_id,
            stakeholder=stakeholder,
            parent_batch_id = parent_batch_id,
            weight=weight,
            latitude=latitude,
            longitude=longitude,
            image_path=None,  # No image for collector
            pdf_path=None,
            extra_data=extra_data
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # 4️⃣ Return response
    return {"batch_id": batch_id, "metadata": metadata, "hash": hash_key}
