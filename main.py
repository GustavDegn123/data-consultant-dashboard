# main.py (opdatering)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import reports, customers

app = FastAPI(
    title="Data Consultant Report API",
    version="0.1.0",
    description="Automatisk PDF-rapportgenerering og kundehåndtering"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inkludér routes
app.include_router(reports.router)
app.include_router(customers.router)

@app.get("/")
def root():
    return {"message": "FastAPI server kører 🎉"}