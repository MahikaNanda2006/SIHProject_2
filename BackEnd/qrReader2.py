from typing import List, Dict, Any, Optional
import json
import base64
from fastapi import APIRouter, HTTPException
from database.db_access import get_record  # Make sure this exists

router = APIRouter()  # <-- This MUST exist

async def trace_batch_info(starting_batch_id: str) -> List[Dict[str, Any]]:
    """
    Trace a batch back through its parent IDs until no parent exists.
    Returns a list of records in reverse order (most recent first).
    """
    trace_history: List[Dict[str, Any]] = []
    current_id: Optional[str] = starting_batch_id

    for _ in range(100):  # safety limit
        if not current_id:
            break

        record = await get_record(current_id)
        if not record:
            if not trace_history:  # nothing found at all
                raise HTTPException(status_code=404, detail=f"Batch ID '{starting_batch_id}' not found.")
            break

        # Encode images and PDFs for frontend use
        # Encode images and PDFs for frontend use
        if record.get("image"):
            record["image_base64"] = f"data:image/png;base64,{base64.b64encode(record['image']).decode('ascii')}"
        else:
            record["image_base64"] = None

        if record.get("pdf"):
            record["pdf_base64"] = f"data:application/pdf;base64,{base64.b64encode(record['pdf']).decode('ascii')}"
        else:
            record["pdf_base64"] = None
        record.pop("image", None)
        record.pop("pdf", None)

        # Ensure extra_data is a dictionary
        extra_data = record.get("extra_data")
        if extra_data is None:
            record["extra_data"] = {}
        elif isinstance(extra_data, str):
            try:
                record["extra_data"] = json.loads(extra_data)
            except json.JSONDecodeError:
                record["extra_data"] = {}

        trace_history.append(record)

        # Move to parent
        current_id = record.get("parent_batch_id")
        if not current_id or current_id in ["0", "null", "None"]:
            break

    return trace_history  # Most recent first

# --- Endpoint ---
@router.get("/trace/{batch_id}")
async def trace_batch(batch_id: str):
    """
    API endpoint to trace a batch's full history by its batch_id.
    """
    history = await trace_batch_info(batch_id)
    if not history:
        raise HTTPException(status_code=404, detail=f"No records found for batch ID {batch_id}")
    return {"trace": history}
