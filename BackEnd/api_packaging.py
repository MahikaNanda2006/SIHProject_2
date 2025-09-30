from fastapi import APIRouter, File, Form, UploadFile, HTTPException
from database import db_access as db
import os
import time
import random
import os

router = APIRouter()
def generate_unique_batch_id() -> str:
    """Generate a unique numeric batch ID based on timestamp + random digits."""
    timestamp = int(time.time() * 1000)  # milliseconds
    rand_suffix = random.randint(100, 999)
    return f"{timestamp}{rand_suffix}"

@router.post("/submit/packaging")
async def submit_packaging(
    #parentbatch_id: str = Form(...),
    parent_batch_id: str = Form(...),   # parent batch
    #crop_name: str = Form(...),
    #weight: str = Form(...),
    stakeholder: str = Form(...),       # should be "packaging"
    report: UploadFile = File(...),     # PDF file
):
    # Ensure valid PDF format
    if not report.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid file format. Must be PDF.")
    batch_id = generate_unique_batch_id()
    # Save PDF temporarily
    temp_path = f"temp_{batch_id}.pdf"
    with open(temp_path, "wb") as f:
        f.write(await report.read())

    # Optional extra data
    #extra_data = {"crop_name": crop_name}

    try:
        batch_id, metadata, hash_key = db.insert_batch(
            batch_id=batch_id,
            stakeholder=stakeholder,
            parent_batch_id=parent_batch_id,  # store parent batch
            weight=None,
            latitude=None,
            longitude=None,
            image_path=None,       # No image
            pdf_path=temp_path,    # Store PDF
            extra_data={}
        )
    finally:
        os.remove(temp_path)

    return {"batch_id": batch_id, "metadata": metadata, "hash": hash_key}
