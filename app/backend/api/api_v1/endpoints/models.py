from fastapi import APIRouter
from fastapi.requests import Request

from schemas.models import ModelRequestSchema, ModelResponseSchema
from services.model import ModelService

router = APIRouter()


@router.post("/:cv", response_model=ModelResponseSchema)
async def get_vacancies_by_cv(request: Request, data: ModelRequestSchema):
    service: ModelService = request.app.state.model_service
    return service.get_vacancies_by_cv(data.text)

@router.post("/:vancancy", response_model=ModelResponseSchema)
async def get_cvs_by_vacancy(request: Request, data: ModelRequestSchema):
    service: ModelService = request.app.state.model_service
    return service.get_cvs_by_vacancy(data.text)
