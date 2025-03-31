# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Opret app
app = FastAPI(
    title="Data Consultant Report API",
    version="0.1.0",
    description="Automatisk PDF-rapportgenerering og kundehåndtering"
)

# (Valgfrit) Tillad adgang fra frontend / Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Skift til specifikke domæner i prod!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def root():
    return {"message": "FastAPI server kører 🎉"}

# Klar til at inkludere routes, fx:
# from api.routes import reports, customers
# app.include_router(reports.router)
# app.include_router(customers.router)
