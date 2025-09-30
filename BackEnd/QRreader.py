import hashlib
import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime
from PIL import Image
from pyzbar.pyzbar import decode
import asyncpg

# --- PostgreSQL Configuration ---
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "user": "postgres",
    "password": "Root",
    "database": "Srunkhala"
}

db_pool: Optional[asyncpg.pool.Pool] = None

# --- Database Access ---
async def get_db_record(batch_id: str) -> Optional[Dict[str, Any]]:
    global db_pool
    if db_pool is None:
        raise RuntimeError("Database connection pool is not initialized.")
    record = await db_pool.fetchrow("SELECT * FROM batches WHERE batch_id = $1", batch_id)
    return dict(record) if record else None

# --- Utilities and Models ---
def generate_hash(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()

class TraceRecordResponse(BaseModel):
    batch_id: str
    stakeholder: str
    parent_batch_id: Optional[str] = None
    weight: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    timestamp: datetime
    hash_key: str
    extra_data: Dict[str, Any]

# --- Trace Logic ---
async def trace_batch_info(starting_batch_id: str) -> List[Dict[str, Any]]:
    trace_history: List[Dict[str, Any]] = []
    current_id = starting_batch_id

    for _ in range(100):  # safety limit
        record = await get_db_record(current_id)
        if not record:
            if not trace_history:
                raise ValueError(f"Batch ID '{starting_batch_id}' not found.")
            break

        extra_data = record.get("extra_data")
        if extra_data is None:
            record["extra_data"] = {}
        elif isinstance(extra_data, str):
            record["extra_data"] = json.loads(extra_data)

        trace_history.append(record)
        current_id = record.get("parent_batch_id")
        if current_id is None:
            break

    return trace_history

# --- QR Decoding and Stakeholder Grouping ---
async def trace_from_qr(file) -> Dict[str, List[Dict[str, Any]]]:
    try:
        image = Image.open(file)
        decoded_objs = decode(image)
        if not decoded_objs:
            raise ValueError("No QR code found in the image")
        batch_id = decoded_objs[0].data.decode("utf-8")
    except Exception as e:
        raise ValueError(f"Failed to decode QR: {e}")

    history = await trace_batch_info(batch_id)
    history.reverse()  # Farmer -> Customer

    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for record in history:
        stakeholder = record.get("stakeholder", "Unknown")
        grouped.setdefault(stakeholder, []).append(record)

    return grouped

# --- Database Pool Helpers ---
async def init_db_pool():
    global db_pool
    db_pool = await asyncpg.create_pool(**DB_CONFIG)

async def close_db_pool():
    global db_pool
    if db_pool:
        await db_pool.close()
        db_pool = None
