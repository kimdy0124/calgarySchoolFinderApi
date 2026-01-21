from fastapi import FastAPI
from app.routers import schools, districts, programs, geocode
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Calgary School Finder API", version="0.1.0")

@app.get("/health")
def health():
    return {"ok": True}

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://calgary-school-finder-api-dy5o.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(schools.router)
app.include_router(districts.router)
app.include_router(programs.router)
app.include_router(geocode.router)