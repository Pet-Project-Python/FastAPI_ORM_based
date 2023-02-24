from fastapi import APIRouter

from app.models.schemas.health import HealthCheckResponse

router = APIRouter()


@router.get(
    "/",
    response_model=HealthCheckResponse,
    summary="Health check",
)
async def health():
    return HealthCheckResponse(status="OK")
