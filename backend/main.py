""" Description: Main entry point for the FastAPI application. """

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import api_router
from database import engine
from models import Base
from config import configure_logging, DEBUG, ALLOWED_HOSTS

configure_logging()

app = FastAPI(
    title="Peannut Butter Payroll API",
    description="An API for managing payroll for Peanut Butter company",
    version="0.1.0",
    debug=DEBUG,
    host="0.0.0.0",
    port=8080,
    url_prefix="/api",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()


app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
