from typing import Optional
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.lesson_completion import LessonCompletion


class LessonCompletionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: int, lesson_slug: str) -> LessonCompletion:
        completion = LessonCompletion(user_id=user_id, lesson_slug=lesson_slug)
        self.session.add(completion)
        await self.session.flush()
        await self.session.refresh(completion)
        return completion

    async def delete(self, user_id: int, lesson_slug: str) -> bool:
        result = await self.session.execute(
            delete(LessonCompletion).where(
                LessonCompletion.user_id == user_id,
                LessonCompletion.lesson_slug == lesson_slug,
            )
        )
        return result.rowcount > 0

    async def exists(self, user_id: int, lesson_slug: str) -> bool:
        result = await self.session.execute(
            select(LessonCompletion).where(
                LessonCompletion.user_id == user_id,
                LessonCompletion.lesson_slug == lesson_slug,
            )
        )
        return result.scalar_one_or_none() is not None

    async def get_completed_slugs(self, user_id: int) -> list[str]:
        result = await self.session.execute(
            select(LessonCompletion.lesson_slug).where(LessonCompletion.user_id == user_id)
        )
        return [row[0] for row in result.all()]