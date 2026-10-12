from typing import Optional
from pydantic import BaseModel


class ProgressRead(BaseModel):
    completed_lessons: list[str]
    total_lessons: int
    completion_percentage: float
    last_lesson_slug: Optional[str] = None
    quiz_stats: dict = {}


class LessonCompletionCreate(BaseModel):
    pass  # Empty body, just needs the slug in path