"""Entry point FastAPI untuk website Gow! Tennis."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .routers import contact, profile, social

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description=(
        "API untuk landing page Gow! Tennis: profil klub, program, "
        "dan feed Instagram/TikTok."
    ),
    version="1.0.0",
    docs_url="/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(profile.router, prefix="/api")
app.include_router(social.router, prefix="/api")
app.include_router(contact.router, prefix="/api")


@app.get("/api/health", tags=["sistem"], summary="Health check")
async def health() -> dict:
    return {"status": "ok", "environment": settings.environment}
