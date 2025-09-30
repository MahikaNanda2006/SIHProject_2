from fastapi import APIRouter, File, Form, UploadFile, HTTPException
from database import db_access as db
from BackEnd.utils.extract_gps_from_image import extract_gps_from_image 
import time
import random
import os
from supabase import create_client, Client
import uuid

router = APIRouter()

# Initialize Supabase client (set these as environment variables)
import os
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def generate_unique_batch_id() -> str:
    """Generate a unique numeric batch ID based on timestamp + random digits."""
    timestamp = int(time.time() * 1000)  # milliseconds
    rand_suffix = random.randint(100, 999)
    return f"{timestamp}{rand_suffix}"

@router.post("/submit/farmer")
async def submit_farmer(
    stakeholder: str = Form(...),  # should be "farmer"
    image: UploadFile = File(...)
):
    # 1️⃣ Validate image
    if not image.filename.lower().endswith((".jpg", ".jpeg", ".png")):
        raise HTTPException(status_code=400, detail="Invalid image format. Must be JPG or PNG.")
    
    batch_id = generate_unique_batch_id()

    # 2️⃣ Save to a temporary local file for GPS extraction
    temp_path = f"temp_{batch_id}.jpg"
    content = await image.read()
    with open(temp_path, "wb") as f:
        f.write(content)

    # 3️⃣ Extract GPS coordinates (if available)
    latitude, longitude = extract_gps_from_image(temp_path)

    # 4️⃣ Upload image to Supabase storage
    try:
        supabase_file_name = f"{uuid.uuid4()}_{image.filename}"
        upload_response = supabase.storage.from_("uploads").upload(supabase_file_name, content)
        if upload_response.get("error"):
            raise HTTPException(status_code=500, detail=upload_response["error"]["message"])
        # Optional: get public URL
        public_url = supabase.storage.from_("uploads").get_public_url(supabase_file_name)
    finally:
        # 5️⃣ Remove temp file
        os.remove(temp_path)

    # 6️⃣ Call database function
    try:
        batch_id, metadata, hash_key = db.insert_batch(
            batch_id=batch_id,
            stakeholder=stakeholder,
            parent_batch_id=None,
            weight=None,
            latitude=latitude,
            longitude=longitude,
            image_path=public_url,  # save the Supabase URL instead of local path
            pdf_path=None,
            extra_data={}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # 7️⃣ Return response
    return {"batch_id": batch_id, "metadata": metadata, "hash": hash_key, "image_url": public_url}
