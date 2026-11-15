from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from patients.router import router as patient_router
from view import router as index_router

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="МедРейтинг")

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

app.include_router(patient_router)
app.include_router(index_router)
