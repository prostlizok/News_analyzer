from fastapi import APIRouter
from src.modules.api.v1.services import CollectService

router = APIRouter(prefix="/v1")

service = CollectService()


@router.post(path="/collect_info")
async def generate_pipeline_response():
    return await service.get_pipeline_response()
