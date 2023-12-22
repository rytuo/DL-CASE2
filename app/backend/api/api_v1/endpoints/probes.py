from fastapi import APIRouter, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from services.model import ModelService

router = APIRouter()


@router.get("/liveness")
async def liveness_probe(request: Request):
    service: ModelService = request.app.state.model_service
    return JSONResponse({"model_loaded": service.model_loaded}, status_code=status.HTTP_200_OK)
