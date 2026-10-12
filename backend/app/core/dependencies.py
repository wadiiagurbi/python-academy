from functools import lru_cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.content_loader import ContentLoader
from app.services.progress_service import ProgressService
from app.services.quiz_service import QuizService
from app.services.pipeline_service import PipelineService


@lru_cache
def get_content_loader() -> ContentLoader:
    return ContentLoader()


async def get_progress_service(
    session: AsyncSession = Depends(get_db),
    content_loader: ContentLoader = Depends(get_content_loader),
) -> ProgressService:
    return ProgressService(session, content_loader)


async def get_quiz_service(
    session: AsyncSession = Depends(get_db),
    content_loader: ContentLoader = Depends(get_content_loader),
) -> QuizService:
    return QuizService(session, content_loader)


async def get_pipeline_service(
    session: AsyncSession = Depends(get_db),
) -> PipelineService:
    return PipelineService(session)