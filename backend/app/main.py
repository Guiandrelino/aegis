from fastapi import FastAPI

app = FastAPI(
    title="Aegis API",
    version="0.1.0",
    description="Production-oriented AI Agent Runtime",
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "aegis-api",
    }