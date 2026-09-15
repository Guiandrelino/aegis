from fastapi import FastAPI

from app.api.v1.routes.tasks import router as tasks_router


app = FastAPI(
    title="Aegis API",
    version="0.1.0",
    description="Production-oriented AI Agent Runtime",
)


app.include_router(
    tasks_router,
    prefix="/api/v1",
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "aegis-api",
    }