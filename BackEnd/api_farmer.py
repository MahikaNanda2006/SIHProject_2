from fastapi import APIRouter, File, Form, UploadFile, HTTPException, FastAPI
from database import db_access as db
from BackEnd.utils.extract_gps_from_image import extract_gps_from_image 
import time
import random
import os

router = APIRouter()
def generate_unique_batch_id() -> str:
    """Generate a unique numeric batch ID based on timestamp + random digits."""
    timestamp = int(time.time() * 1000)  # milliseconds
    rand_suffix = random.randint(100, 999)
    return f"{timestamp}{rand_suffix}"

#app.include_router(router)
@router.post("/submit/farmer")
async def submit_farmer(
    #batch_id: str = Form(...),
    #crop_name: str = Form(...),
    #weight: str = Form(...),
    stakeholder: str = Form(...),  # should be "farmer"
    image: UploadFile = File(...)
):
    # 1️⃣ Validate image
    if not image.filename.lower().endswith((".jpg", ".jpeg", ".png")):
        raise HTTPException(status_code=400, detail="Invalid image format. Must be JPG or PNG.")
    batch_id = generate_unique_batch_id()
    # 2️⃣ Save temp file
    temp_path = f"temp_{batch_id}.jpg"
    with open(temp_path, "wb") as f:
        f.write(await image.read())

    # 3️⃣ Extract GPS coordinates (if available)
    latitude, longitude = extract_gps_from_image(temp_path)
    
    # 4️⃣ Prepare extra_data
    #extra_data = {"crop_name": crop_name}

    # 5️⃣ Call database function
    try:
        batch_id, metadata, hash_key = db.insert_batch(
            batch_id=batch_id,
            stakeholder=stakeholder,
            parent_batch_id= None,
            weight=None,
            latitude=latitude,
            longitude=longitude,
            image_path=temp_path,
            pdf_path=None,  # No PDF for farmers
            extra_data={}
        )
    finally:
        # Clean up temp file
        os.remove(temp_path)

    # 6️⃣ Return response
    return {"batch_id": batch_id, "metadata": metadata, "hash": hash_key}
