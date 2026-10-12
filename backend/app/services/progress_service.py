from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import LessonNotFoundException
from app.models.user import User
from app.repositories.lesson_completion_repository import LessonCompletionRepository
from app.repositories.quiz_attempt_repository import QuizAttemptRepository
from app.repositories.user_repository import UserRepository
from app.schemas.progress import ProgressRead
from app.services.content_loader import ContentLoader


class ProgressService:
    def __init__(self, session: AsyncSession, content_loader: ContentLoader):
        self.session = session
        self.completion_repo = LessonCompletionRepository(session)
        self.quiz_repo = QuizAttemptRepository(session)
        self.user_repo = UserRepository(session)
        self.content_loader = content_loader

    async def get_progress(self, user: User) -> ProgressRead:
        completed_slugs = await self.completion_repo.get_completed_slugs(user.id)
        quiz_stats = await self.quiz_repo.get_stats(user.id)

        all_lessons = self.content_loader.get_course_tree()
        total_lessons = sum(len(ch.lessons) for track in all_lessons for ch in track.chapters)

        last_lesson = None
        if user.last_lesson_slug:
            try:
                lesson = self.content_loader.get_lesson(user.last_lesson_slug)
                last_lesson = user.last_lesson_slug
            except LessonNotFoundException:
                pass

        return ProgressRead(
            completed_lessons=completed_slugs,
            total_lessons=total_lessons,
            completion_percentage=(len(completed_slugs) / total_lessons * 100) if total_lessons > 0 else 0,
            last_lesson_slug=last_lesson,
            quiz_stats=quiz_stats,
        )

    async def mark_complete(self, user: User, lesson_slug: str) -> None:
        lesson = self.content_loader.get_lesson(lesson_slug)
        exists = await self.completion_repo.exists(user.id, lesson_slug)
        if not exists:
            await self.completion_repo.create(user.id, lesson_slug)
            await self.session.commit()

        await self.user_repo.update_last_lesson(user.id, lesson_slug)
        await self.session.commit()

    async def mark_incomplete(self, user: User, lesson_slug: str) -> None:
        deleted = await self.completion_repo.delete(user.id, lesson_slug)
        if deleted:
            await self.session.commit()

        current_user = await self.user_repo.get_by_id(user.id)
        if current_user and current_user.last_lesson_slug == lesson_slug:
            await self.user_repo.update_last_lesson(user.id, None)
            await self.session.commit()