from typing import Optional
from pydantic import BaseModel, Field


class QuizAttemptCreate(BaseModel):
    answers: list[int] = Field(min_length=1)  # List of selected option indices


class QuizQuestionResult(BaseModel):
    question: str
    options: list[str]
    selected: int
    correct: int
    is_correct: bool
    explanation: str


class QuizAttemptRead(BaseModel):
    score: int
    total_questions: int
    percentage: float
    results: list[QuizQuestionResult]
    attempted_at: str