from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


class Difficulty(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class Navigation(BaseModel):
    previous: Optional["LessonSummary"] = None
    next: Optional["LessonSummary"] = None


class LessonSections(BaseModel):
    learning_objective: str
    explanation: str
    why_it_matters: str
    example: str
    code: str
    code_language: str
    code_explanation: str
    common_mistakes: str
    best_practices: str
    exercise: str
    solution: str


class QuizQuestionPublic(BaseModel):
    question: str
    options: list[str]
    explanation: str


class QuizQuestion(BaseModel):
    question: str
    options: list[str]
    answer: int
    explanation: str = ""


class LessonSummary(BaseModel):
    slug: str
    title: str
    track: str
    chapter: str
    chapter_title: str
    difficulty: Difficulty
    order: int
    global_order: int


class LessonContent(BaseModel):
    slug: str
    track: str
    track_title: str
    chapter: str
    chapter_title: str
    title: str
    difficulty: Difficulty
    order: int
    estimated_minutes: int
    tags: list[str]
    sections: LessonSections
    quiz: list[QuizQuestionPublic]
    navigation: Navigation


class Chapter(BaseModel):
    key: str
    title: str
    order: int
    lessons: list[LessonSummary]


class Track(BaseModel):
    key: str
    title: str
    order: int
    chapters: list[Chapter]


# Update forward references
LessonSummary.model_rebuild()
Navigation.model_rebuild()