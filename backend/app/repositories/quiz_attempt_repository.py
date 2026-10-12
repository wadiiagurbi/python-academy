from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.quiz_attempt import QuizAttempt


class QuizAttemptRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, attempt: QuizAttempt) -> QuizAttempt:
        self.session.add(attempt)
        await self.session.flush()
        await self.session.refresh(attempt)
        return attempt

    async def get_by_user_and_lesson(self, user_id: int, lesson_slug: str) -> list[QuizAttempt]:
        result = await self.session.execute(
            select(QuizAttempt)
            .where(QuizAttempt.user_id == user_id, QuizAttempt.lesson_slug == lesson_slug)
            .order_by(QuizAttempt.attempted_at.desc())
        )
        return list(result.scalars().all())

    async def get_stats(self, user_id: int) -> dict:
        result = await self.session.execute(
            select(QuizAttempt).where(QuizAttempt.user_id == user_id)
        )
        attempts = list(result.scalars().all())
        if not attempts:
            return {"total_attempts": 0, "average_score": 0, "best_score": 0}
        percentages = [a.score / a.total_questions * 100 for a in attempts]
        return {
            "total_attempts": len(attempts),
            "average_score": sum(percentages) / len(percentages),
            "best_score": max(percentages),
        }