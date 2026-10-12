from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import LessonNotFoundException, ValidationException
from app.models.user import User
from app.models.quiz_attempt import QuizAttempt
from app.repositories.quiz_attempt_repository import QuizAttemptRepository
from app.schemas.lesson import QuizQuestion
from app.schemas.quiz import QuizAttemptCreate, QuizAttemptRead, QuizQuestionResult
from app.services.content_loader import ContentLoader


class QuizService:
    def __init__(self, session: AsyncSession, content_loader: ContentLoader):
        self.session = session
        self.quiz_repo = QuizAttemptRepository(session)
        self.content_loader = content_loader

    async def attempt_quiz(self, user: User, lesson_slug: str, data: QuizAttemptCreate) -> QuizAttemptRead:
        lesson = self.content_loader.get_lesson(lesson_slug)

        quiz_questions = self._get_quiz_questions_with_answers(lesson_slug)

        if len(data.answers) != len(quiz_questions):
            raise ValidationException(
                f"Expected {len(quiz_questions)} answers, got {len(data.answers)}"
            )

        results = []
        score = 0
        for i, (submitted, question) in enumerate(zip(data.answers, quiz_questions)):
            is_correct = submitted == question.answer
            if is_correct:
                score += 1
            results.append(
                QuizQuestionResult(
                    question=question.question,
                    options=question.options,
                    selected=submitted,
                    correct=question.answer,
                    is_correct=is_correct,
                    explanation=question.explanation,
                )
            )

        attempt = QuizAttempt(
            user_id=user.id,
            lesson_slug=lesson_slug,
            score=score,
            total_questions=len(quiz_questions),
            answers=[
                {
                    "question_index": i,
                    "selected_option": r.selected,
                    "correct": r.correct,
                }
                for i, r in enumerate(results)
            ],
        )
        await self.quiz_repo.create(attempt)
        await self.session.commit()
        await self.session.refresh(attempt)

        attempted_at = attempt.attempted_at
        if attempted_at is None:
            attempted_at = datetime.now(timezone.utc)

        return QuizAttemptRead(
            score=score,
            total_questions=len(quiz_questions),
            percentage=round(score / len(quiz_questions) * 100, 1) if quiz_questions else 0,
            results=results,
            attempted_at=attempted_at.isoformat(),
        )

    def _get_quiz_questions_with_answers(self, lesson_slug: str) -> list[QuizQuestion]:
        return self.content_loader.get_quiz_answers(lesson_slug)