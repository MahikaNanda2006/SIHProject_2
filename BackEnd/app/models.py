from pydantic import BaseModel
from typing import Optional, List

class CollectionEvent(BaseModel):
    batch_id: str
    species: str
    collector_id: str
    gps_lat: float
    gps_lon: float
    timestamp: str
    moisture: float
    prev_hash: Optional[str] = None

class ProvenanceResponse(BaseModel):
    batch_id: str
    events: List[dict]
