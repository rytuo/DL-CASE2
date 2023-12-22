from fastapi import APIRouter, Depends

from api.api_v1.deps import valid_content_length
from api.api_v1.endpoints.models import router as models_router
from api.api_v1.endpoints.probes import router as probes_router

router = APIRouter()


router.include_router(models_router, prefix="/models", dependencies=[Depends(valid_content_length)])
router.include_router(probes_router, prefix="/~")
