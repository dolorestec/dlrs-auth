"""
Health check endpoint.
"""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get(
    "/",
    summary="Health Check",
    description="Verifica se o serviço de autenticação está saudável e "
    "funcionando corretamente.",
    response_description="Status de saúde do serviço",
    responses={
        200: {
            "description": "Serviço saudável",
            "content": {
                "application/json": {
                    "example": {"status": "healthy", "service": "dlrs-auth"}
                }
            },
        }
    },
)  # type: ignore[misc]
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "service": "dlrs-auth"}
