import logging
from src.modules.pipeline.services import collect_info

logger = logging.getLogger(__name__)


class CollectService:
    async def get_pipeline_response(self):
        return collect_info()
