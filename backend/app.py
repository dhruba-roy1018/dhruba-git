from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from legallens import router as legallens_router
from scamshield import router as scamshield_router

app = FastAPI(title="Legal Safety Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(legallens_router, prefix="/legallens", tags=["LegalLens"])
app.include_router(scamshield_router, prefix="/scamshield", tags=["ScamShield"])

@app.get("/")
def root():
    return {"status": "Backend is running"}