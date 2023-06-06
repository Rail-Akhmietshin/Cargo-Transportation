from fastapi import FastAPI
from src.transportation.router import router as transportation_router

app = FastAPI(
    title="Transportation"
)

app.include_router(transportation_router)


