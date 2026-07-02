"""
TEMPLATE -- FastAPI entrypoint. Run from the backend root:
    uv run uvicorn api.main:app --reload --port 8000
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import config

# TODO: import your routers
# from api.routers import dashboard, entities, recommendations

app = FastAPI(title="[PRODUCT NAME] API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,  # confirm this matches your frontend's actual dev port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO: app.include_router(dashboard.router)
# TODO: app.include_router(entities.router)
# TODO: app.include_router(recommendations.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}


# -----------------------------------------------------------------------
# TEMPLATE -- a single router, for reference. Copy this pattern per screen.
# -----------------------------------------------------------------------
"""
from fastapi import APIRouter
from api import data_store
from api.schemas import Entity

router = APIRouter(prefix="/api/entities", tags=["entities"])

@router.get("", response_model=list[Entity])
def list_entities():
    return data_store.get_entities()
"""
