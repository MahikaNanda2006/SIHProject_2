from fastapi import FastAPI
from routes import collection, provenance

app = FastAPI(title="Ayurvedic Herb Traceability MVP")

# Include API routers
app.include_router(collection.router, prefix="/collection", tags=["Collection"])
app.include_router(provenance.router, prefix="/provenance", tags=["Provenance"])

# Root endpoint for quick check
@app.get("/")
def root():
    return {"message": "Ayurvedic Herb Traceability MVP Backend is running"}
