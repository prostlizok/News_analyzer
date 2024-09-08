from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.common.logger import init_logger
from src.modules.api.v1.router import router as api_v1_router
from src.modules.db.services import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_logger()
    await init_db()
    yield


app = FastAPI(
    title="Pipeline API",
    version="1",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=api_v1_router)
