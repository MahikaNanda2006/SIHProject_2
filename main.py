from fastapi import FastAPI
from BackEnd.api_farmer import router as farmer_router
from BackEnd.api_collector import router as collector_router
from BackEnd.api_packaging import router as packaging_router
from BackEnd.api_processing1 import router as p1_router
from BackEnd.api_processing2 import router as p2_router
from BackEnd.api_storage import router as storage_router
from BackEnd.qrReader2 import router as qr_router
from database.db_access import init_db_pool, close_db_pool
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from dotenv import load_dotenv



app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://127.0.0.1:5500"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


load_dotenv()  # loads .env file

DATABASE_URL = os.getenv("DATABASE_URL")



# Include all routers
app.include_router(farmer_router)
app.include_router(collector_router)
app.include_router(packaging_router)
app.include_router(p1_router)
app.include_router(p2_router)
app.include_router(storage_router)
app.include_router(qr_router, prefix="/api")

app.mount("/static", StaticFiles(directory="FrontEnd"), name="static")

@app.get("/")
async def root():
    return FileResponse("FrontEnd/farmer.html")

@app.on_event("startup")
async def startup_event():
    await init_db_pool()

# Shutdown event → close DB pool
@app.on_event("shutdown")
async def shutdown_event():
    await close_db_pool()
