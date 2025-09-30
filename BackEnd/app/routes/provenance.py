from fastapi import APIRouter
from app.models import ProvenanceResponse
from app.blockchain import get_event, get_event_count
import json

router = APIRouter()

@router.get("/{batch_id}")
def get_provenance(batch_id: str):
    count = get_event_count()
    events = []
    for i in range(count):
        e = get_event(i)
        data = json.loads(e["data"])
        if data["batch_id"] == batch_id:
            events.append(data)
    if not events:
        return {"message": "No events found for this batch"}
    return ProvenanceResponse(batch_id=batch_id, events=events)
