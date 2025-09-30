from fastapi import APIRouter, File, Form, UploadFile, HTTPException
from database import db_access as db
from supabase import create_client, Client
import time
import random
import os
import uuid

router = APIRouter()

# Supabase client
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def generate_unique_batch_id() -> str:
    timestamp = int(time.time() * 1000)
    rand_suffix = random.randint(100, 999)
    return f"{timestamp}{rand_suffix}"

@router.post("/submit/packaging")
async def submit_packaging(
    parent_batch_id: str = Form(...),
    stakeholder: str = Form(...),
    report: UploadFile = File(...)
):
    # 1️⃣ Validate PDF
    if not report.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid file format. Must be PDF.")
    
    batch_id = generate_unique_batch_id()
    content = await report.read()

    # 2️⃣ Upload PDF to Supabase storage
    pdf_file_name = f"{uuid.uuid4()}_{report.filename}"
    upload_response = supabase.storage.from_("uploads").upload(pdf_file_name, content)
    if upload_response.get("error"):
        raise HTTPException(status_code=500, detail=upload_response["error"]["message"])
    
    public_url = supabase.storage.from_("uploads").get_public_url(pdf_file_name)

    # 3️⃣ Insert into DB
    try:
        batch_id, metadata, hash_key = db.insert_batch(
            batch_id=batch_id,
            stakeholder=stakeholder,
            parent_batch_id=parent_batch_id,
            weight=None,
            latitude=None,
            longitude=None,
            image_path=None,
            pdf_path=public_url,  # Supabase URL instead of local file
            extra_data={}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # 4️⃣ Return response
    return {"batch_id": batch_id, "metadata": metadata, "hash": hash_key, "pdf_url": public_url}
