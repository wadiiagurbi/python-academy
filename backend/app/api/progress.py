from fastapi import APIRouter, Depends, status

from app.schemas.progress import ProgressRead
from app.services.auth_service import get_current_user
from app.services.progress_service import ProgressService
from app.core.dependencies import get_progress_service
from app.models.user import User

router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("", response_model=ProgressRead)
async def get_progress(
    current_user: User = Depends(get_current_user),
    progress_service: ProgressService = Depends(get_progress_service),
):
    return await progress_service.get_progress(current_user)


@router.post("/lessons/{slug}/complete", status_code=status.HTTP_204_NO_CONTENT)
async def mark_lesson_complete(
    slug: str,
    current_user: User = Depends(get_current_user),
    progress_service: ProgressService = Depends(get_progress_service),
):
    await progress_service.mark_complete(current_user, slug)


@router.delete("/lessons/{slug}/complete", status_code=status.HTTP_204_NO_CONTENT)
async def mark_lesson_incomplete(
    slug: str,
    current_user: User = Depends(get_current_user),
    progress_service: ProgressService = Depends(get_progress_service),
):
    await progress_service.mark_incomplete(current_user, slug)