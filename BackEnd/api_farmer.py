from fastapi import APIRouter, Form, HTTPException
from database import db_access as db
import time
import random

router = APIRouter()

def generate_unique_batch_id() -> str:
    """Generate a unique numeric batch ID based on timestamp + random digits."""
    timestamp = int(time.time() * 1000)  # milliseconds
    rand_suffix = random.randint(100, 999)
    return f"{timestamp}{rand_suffix}"

@router.post("/submit/farmer")
async def submit_farmer(
    stakeholder: str = Form(...),  # should be "farmer"
):
    batch_id = generate_unique_batch_id()

    # 6️⃣ Call database function without image upload
    try:
        batch_id, metadata, hash_key = db.insert_batch(
            batch_id=batch_id,
            stakeholder=stakeholder,
            parent_batch_id=None,
            weight=None,
            latitude=None,
            longitude=None,
            image_path=None,  # no image
            pdf_path=None,
            extra_data={}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # 7️⃣ Return response
    return {"batch_id": batch_id, "metadata": metadata, "hash": hash_key}
