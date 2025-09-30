from fastapi import APIRouter, File, Form, UploadFile, HTTPException
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
    
@router.post("/submit/processing2")
async def submit_processing2(
    #batch_id: str = Form(...),
    parent_batch_id: str = Form(...),
    weight: str = Form(...),
    stakeholder: str = Form(...),   # should be "processing2"
    report: UploadFile = File(...), # PDF file
):
    # Ensure valid PDF format
    if not report.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid file format. Must be PDF.")
    batch_id = generate_unique_batch_id()
    # Save PDF temporarily
    temp_path = f"temp_{batch_id}.pdf"
    with open(temp_path, "wb") as f:
        f.write(await report.read())

    try:
        batch_id, metadata, hash_key = db.insert_batch(
            batch_id=batch_id,
            stakeholder=stakeholder,
            parent_batch_id=parent_batch_id,
            weight=weight,
            latitude=None,
            longitude=None,
            image_path=None,     # No image
            pdf_path=temp_path,  # Store PDF
            extra_data={}        # No extra data needed
        )
    finally:
        os.remove(temp_path)

    return {"batch_id": batch_id, "metadata": metadata, "hash": hash_key}
