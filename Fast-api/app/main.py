from fastapi import FastAPI
from app.api.v1 import home

app = FastAPI(
    title="Enmaz Analytics API",
    version="1.0.0"
)

app.include_router(home.router)

@app.get("/")
def root():
    return {"message": "Enmaz Analytics API is running "}
