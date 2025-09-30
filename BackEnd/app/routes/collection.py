from fastapi import APIRouter
from models import CollectionEvent
from blockchain import add_collection_event
from qr_generator import generate_qr

router = APIRouter()

@router.post("/")
def submit_collection(event: CollectionEvent):
    tx_hash = add_collection_event(event.dict())
    return {
        "message": "Collection event submitted successfully",
        "transaction_hash": tx_hash,
        "qr_code_endpoint": f"/collection/qr/{event.batch_id}"
    }

@router.get("/qr/{batch_id}")
def get_qr(batch_id: str):
    return generate_qr(batch_id)
