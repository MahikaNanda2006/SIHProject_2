import os
import psycopg2
import psycopg2.extras
import asyncpg
import hashlib
import json
from datetime import datetime
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()  # loads variables from .env

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Check your .env file.")

if "localhost" in DATABASE_URL or "127.0.0.1" in DATABASE_URL:
    conn = psycopg2.connect(DATABASE_URL)
else:
    conn = psycopg2.connect(DATABASE_URL, sslmode="require")

# -------- Sync Connection (psycopg2) --------


DATABASE_URL = os.getenv("DATABASE_URL")

# If local, remove SSL requirement
if "localhost" in DATABASE_URL or "127.0.0.1" in DATABASE_URL:
    conn = psycopg2.connect(DATABASE_URL)
else:
    conn = psycopg2.connect(DATABASE_URL, sslmode="require")


# -------- Utility: SHA-256 hash --------
def generate_hash(batch_data: Dict[str, Any]) -> str:
    data_string = str(batch_data)
    return hashlib.sha256(data_string.encode("utf-8")).hexdigest()

# -------- Utility: Read file as bytes --------
def read_file_bytes(file_path: Optional[str]) -> Optional[bytes]:
    if not file_path:
        return None
    with open(file_path, "rb") as f:
        return f.read()

# -------- Insert a new batch (sync) --------
def insert_batch(
    batch_id: str,
    stakeholder: str,
    parent_batch_id: Optional[str],
    weight: str,
    latitude: Optional[float],
    longitude: Optional[float],
    image_path: Optional[str],
    pdf_path: Optional[str],
    extra_data: Dict[str, Any]
):
    image_bytes = read_file_bytes(image_path)
    pdf_bytes = read_file_bytes(pdf_path)

    batch_data = {
        "batch_id": batch_id,
        "stakeholder": stakeholder,
        "parent_batch_id": parent_batch_id,
        "weight": weight,
        "latitude": latitude,
        "longitude": longitude,
        "extra_data": extra_data,
        "timestamp": str(datetime.now())
    }

    hash_key = generate_hash(batch_data)

    conn.execute(
        """
        INSERT INTO batches (
            batch_id, stakeholder, parent_batch_id,
            weight, latitude, longitude,
            image, pdf, extra_data,
            timestamp, hash_key
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            batch_id, stakeholder, parent_batch_id,
            weight, latitude, longitude,
            psycopg2.Binary(image_bytes) if image_bytes else None,
            psycopg2.Binary(pdf_bytes) if pdf_bytes else None,
            json.dumps(extra_data), batch_data["timestamp"], hash_key
        )
    )
    conn.commit()
    return batch_id, extra_data, hash_key

# -------- Async DB Pool (asyncpg) --------
db_pool: Optional[asyncpg.pool.Pool] = None

async def init_db_pool():
    global db_pool
    if db_pool is None:
        db_pool = await asyncpg.create_pool(DATABASE_URL, ssl="require")

async def close_db_pool():
    global db_pool
    if db_pool:
        await db_pool.close()
        db_pool = None

# -------- Async Get Record by ID --------
async def get_record(batch_id: str) -> Optional[Dict[str, Any]]:
    global db_pool
    if db_pool is None:
        raise RuntimeError("DB pool not initialized. Call init_db_pool() first.")

    record = await db_pool.fetchrow("SELECT * FROM batches WHERE batch_id = $1", batch_id)
    if not record:
        return None

    result = dict(record)
    extra_data = result.get("extra_data")
    if isinstance(extra_data, str):
        try:
            result["extra_data"] = json.loads(extra_data)
        except json.JSONDecodeError:
            result["extra_data"] = {}
    return result
