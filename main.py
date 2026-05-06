from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routes import keys, protected
from app.db.models import create_tables
import os

app = FastAPI(
    title="API Key Manager",
    description="Generate, store, and validate API keys securely.",
    version="1.0.0"
)

# CORS — allow all origins (change in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_tables()
    print("✅ Database initialized")

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", include_in_schema=False)
def dashboard():
    return FileResponse("static/index.html")

app.include_router(keys.router,      prefix="/keys",  tags=["API Keys"])
app.include_router(protected.router, prefix="/api",   tags=["Protected"])

@app.get("/health", tags=["System"])
def health():
    return {"status": "ok", "service": "API Key Manager"}