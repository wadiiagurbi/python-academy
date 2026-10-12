from fastapi import APIRouter, Depends

from app.schemas.quiz import QuizAttemptCreate, QuizAttemptRead
from app.services.auth_service import get_current_user
from app.services.quiz_service import QuizService
from app.core.dependencies import get_quiz_service
from app.models.user import User

router = APIRouter(prefix="/quizzes", tags=["quizzes"])


@router.post("/{slug}/attempt", response_model=QuizAttemptRead)
async def attempt_quiz(
    slug: str,
    data: QuizAttemptCreate,
    current_user: User = Depends(get_current_user),
    quiz_service: QuizService = Depends(get_quiz_service),
):
    return await quiz_service.attempt_quiz(current_user, slug, data)