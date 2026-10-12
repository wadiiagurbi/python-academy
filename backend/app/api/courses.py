from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.lesson import Track, LessonContent
from app.services.auth_service import get_current_user_optional
from app.services.content_loader import ContentLoader
from app.models.user import User

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("", response_model=list[Track])
async def get_courses(
    current_user: User | None = Depends(get_current_user_optional),
):
    loader = ContentLoader()
    return loader.get_course_tree()


@router.get("/search")
async def search_lessons(
    q: str = Query(..., min_length=1),
    current_user: User | None = Depends(get_current_user_optional),
):
    loader = ContentLoader()
    results = loader.search(q)
    return [
        {"lesson": summary.model_dump(), "excerpt": excerpt}
        for summary, excerpt in results
    ]


@router.get("/lessons/{slug}", response_model=LessonContent)
async def get_lesson(
    slug: str,
    current_user: User | None = Depends(get_current_user_optional),
):
    loader = ContentLoader()
    return loader.get_lesson(slug)