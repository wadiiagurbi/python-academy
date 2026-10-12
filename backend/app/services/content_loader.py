import re
from pathlib import Path
from typing import Optional

import yaml
from pydantic import ValidationError

from app.core.config import settings
from app.core.exceptions import LessonNotFoundException, MalformedLessonException
from app.schemas.lesson import (
    Chapter,
    LessonContent,
    LessonSections,
    LessonSummary,
    Navigation,
    QuizQuestion,
    QuizQuestionPublic,
    Track,
    Difficulty,
)


class ContentLoader:
    REQUIRED_SECTIONS = {
        "Learning Objective": "learning_objective",
        "Explanation": "explanation",
        "Why It Matters": "why_it_matters",
        "Example": "example",
        "Code": "code",
        "Code Explanation": "code_explanation",
        "Common Mistakes": "common_mistakes",
        "Best Practices": "best_practices",
        "Exercise": "exercise",
        "Solution": "solution",
        "Mini Quiz": "mini_quiz",
    }

    def __init__(self, courses_dir: Optional[str] = None):
        self.courses_dir = Path(courses_dir or settings.courses_path)
        self._lessons_by_slug: dict[str, LessonContent] = {}
        self._quiz_answers: dict[str, list[QuizQuestion]] = {}
        self._summaries_in_order: dict[str, LessonSummary] = {}
        self._tracks: list[Track] = []
        self._malformed_files: dict[str, str] = {}
        self._loaded = False

    def load(self) -> None:
        if self._loaded:
            return

        self._lessons_by_slug = {}
        self._quiz_answers = {}
        self._malformed_files = {}
        raw_lessons = []

        if not self.courses_dir.is_dir():
            self._summaries_in_order = {}
            self._tracks = []
            self._loaded = True
            return

        md_files = sorted(self.courses_dir.rglob("*.md"))

        for file_path in md_files:
            try:
                raw_lesson = self._parse_lesson_file(file_path)
                raw_lessons.append(raw_lesson)
            except MalformedLessonException as e:
                self._malformed_files[str(file_path)] = str(e)

        raw_lessons.sort(key=lambda x: (x["track_order"], x["chapter_order"], x["order"]))

        summaries = {}
        for i, raw in enumerate(raw_lessons):
            summaries[raw["slug"]] = LessonSummary(
                slug=raw["slug"],
                title=raw["title"],
                track=raw["track"],
                chapter=raw["chapter"],
                chapter_title=raw["chapter_title"],
                difficulty=Difficulty(raw["difficulty"]),
                order=raw["order"],
                global_order=i + 1,
            )

        ordered_slugs = list(summaries.keys())

        for i, raw in enumerate(raw_lessons):
            slug = raw["slug"]
            prev_slug = ordered_slugs[i - 1] if i > 0 else None
            next_slug = ordered_slugs[i + 1] if i + 1 < len(ordered_slugs) else None

            prev = summaries[prev_slug] if prev_slug else None
            nxt = summaries[next_slug] if next_slug else None

            public_quiz = [
                QuizQuestionPublic(
                    question=q.question,
                    options=q.options,
                    explanation=q.explanation,
                )
                for q in raw["quiz"]
            ]

            content = LessonContent(
                slug=slug,
                track=raw["track"],
                track_title=raw["track_title"],
                chapter=raw["chapter"],
                chapter_title=raw["chapter_title"],
                title=raw["title"],
                difficulty=Difficulty(raw["difficulty"]),
                order=raw["order"],
                estimated_minutes=raw["estimated_minutes"],
                tags=raw["tags"],
                sections=raw["sections"],
                quiz=public_quiz,
                navigation=Navigation(previous=prev, next=nxt),
            )

            self._lessons_by_slug[slug] = content
            self._quiz_answers[slug] = raw["quiz"]

        self._summaries_in_order = summaries
        self._tracks = self._build_tree(raw_lessons, summaries)
        self._loaded = True

    def _build_tree(self, raw_lessons: list[dict], summaries: dict[str, LessonSummary]) -> list[Track]:
        tracks_by_key: dict[str, dict] = {}

        for raw in raw_lessons:
            track_key = raw["track"]
            chapter_key = raw["chapter"]

            if track_key not in tracks_by_key:
                tracks_by_key[track_key] = {
                    "title": raw["track_title"],
                    "order": raw["track_order"],
                    "chapters": {},
                }

            if chapter_key not in tracks_by_key[track_key]["chapters"]:
                tracks_by_key[track_key]["chapters"][chapter_key] = {
                    "title": raw["chapter_title"],
                    "order": raw["chapter_order"],
                    "lessons": [],
                }

            tracks_by_key[track_key]["chapters"][chapter_key]["lessons"].append(summaries[raw["slug"]])

        tracks = []
        for track_key, track_data in sorted(tracks_by_key.items(), key=lambda x: x[1]["order"]):
            chapters = []
            for chapter_key, chapter_data in sorted(track_data["chapters"].items(), key=lambda x: x[1]["order"]):
                chapters.append(
                    Chapter(
                        key=chapter_key,
                        title=chapter_data["title"],
                        order=chapter_data["order"],
                        lessons=chapter_data["lessons"],
                    )
                )
            tracks.append(
                Track(key=track_key, title=track_data["title"], order=track_data["order"], chapters=chapters)
            )

        return tracks

    def _parse_lesson_file(self, path: Path) -> dict:
        content = path.read_text(encoding="utf-8")

        if not content.startswith("---"):
            raise MalformedLessonException(str(path), "Missing YAML frontmatter block")

        parts = content.split("---", 2)
        if len(parts) < 3:
            raise MalformedLessonException(str(path), "Invalid frontmatter format")

        _, fm_raw, body = parts

        try:
            frontmatter = yaml.safe_load(fm_raw) or {}
        except yaml.YAMLError as e:
            raise MalformedLessonException(str(path), f"Invalid YAML frontmatter: {e}")

        required_fields = [
            "slug",
            "track",
            "trackTitle",
            "trackOrder",
            "chapter",
            "chapterTitle",
            "chapterOrder",
            "title",
            "difficulty",
            "order",
        ]
        for field in required_fields:
            if field not in frontmatter:
                raise MalformedLessonException(str(path), f'Missing frontmatter field "{field}"')

        if frontmatter["difficulty"] not in ("beginner", "intermediate", "advanced"):
            raise MalformedLessonException(
                str(path), f'Invalid difficulty "{frontmatter["difficulty"]}"'
            )

        sections = self._parse_sections(body)
        quiz = self._parse_quiz(sections.pop("mini_quiz"))

        return {
            "slug": frontmatter["slug"],
            "track": frontmatter["track"],
            "track_title": frontmatter["trackTitle"],
            "track_order": frontmatter["trackOrder"],
            "chapter": frontmatter["chapter"],
            "chapter_title": frontmatter["chapterTitle"],
            "chapter_order": frontmatter["chapterOrder"],
            "title": frontmatter["title"],
            "difficulty": frontmatter["difficulty"],
            "order": frontmatter["order"],
            "estimated_minutes": frontmatter.get("estimatedMinutes", 10) or 10,
            "tags": frontmatter.get("tags", []) or [],
            "sections": sections,
            "quiz": quiz,
        }

    def _parse_sections(self, body: str) -> dict[str, str]:
        pattern = r"^##\s+(.+?)\s*$"
        matches = list(re.finditer(pattern, body, re.MULTILINE))

        if not matches:
            raise MalformedLessonException("", 'No "## Section" headings found in lesson body')

        sections = {}
        for i, match in enumerate(matches):
            heading = match.group(1).strip()
            start = match.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
            content = body[start:end].strip()

            key = self.REQUIRED_SECTIONS.get(heading)
            if key:
                sections[key] = content

        missing = set(self.REQUIRED_SECTIONS.values()) - set(sections.keys())
        if missing:
            raise MalformedLessonException("", f"Missing required section(s): {', '.join(missing)}")

        if "code" in sections:
            code_lang, code = self._extract_code_block(sections["code"])
            sections["code_language"] = code_lang
            sections["code"] = code
        else:
            sections["code_language"] = "text"

        return sections

    def _extract_code_block(self, text: str) -> tuple[str, str]:
        text = text.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            lang = lines[0][3:].strip() or "text"
            code_lines = lines[1:]
            if code_lines and code_lines[-1].strip() == "```":
                code_lines = code_lines[:-1]
            return lang, "\n".join(code_lines)
        return "text", text

    def _parse_quiz(self, section_content: str) -> list[QuizQuestion]:
        code_lang, yaml_text = self._extract_code_block(section_content)
        if code_lang not in ("yaml", "yml"):
            raise MalformedLessonException("", "Mini Quiz section must contain a fenced yaml code block")

        try:
            items = yaml.safe_load(yaml_text) or []
        except yaml.YAMLError as e:
            raise MalformedLessonException("", f"Invalid YAML in Mini Quiz block: {e}")

        if not items:
            raise MalformedLessonException("", "Mini Quiz block must contain at least one question")

        questions = []
        for item in items:
            if not all(k in item for k in ("question", "options", "answer")):
                raise MalformedLessonException("", 'Each quiz question needs "question", "options" and "answer"')
            if not isinstance(item["options"], list) or len(item["options"]) < 2:
                raise MalformedLessonException("", "Each quiz question needs at least 2 options")
            if not isinstance(item["answer"], int) or item["answer"] < 0 or item["answer"] >= len(item["options"]):
                raise MalformedLessonException("", "Quiz answer index out of range")

            questions.append(
                QuizQuestion(
                    question=item["question"],
                    options=item["options"],
                    answer=item["answer"],
                    explanation=item.get("explanation", ""),
                )
            )

        return questions

    def get_course_tree(self) -> list[Track]:
        self.load()
        return self._tracks

    def get_lesson(self, slug: str) -> LessonContent:
        self.load()
        if slug not in self._lessons_by_slug:
            raise LessonNotFoundException(slug)
        return self._lessons_by_slug[slug]

    def get_quiz_answers(self, slug: str) -> list[QuizQuestion]:
        self.load()
        if slug not in self._quiz_answers:
            raise LessonNotFoundException(slug)
        return self._quiz_answers[slug]

    def get_malformed_files(self) -> dict[str, str]:
        self.load()
        return self._malformed_files

    def search(self, query: str) -> list[tuple[LessonSummary, str]]:
        self.load()
        needle = query.strip().lower()
        if not needle:
            return []

        results = []
        for slug in self._summaries_in_order:
            lesson = self._lessons_by_slug.get(slug)
            if not lesson:
                continue

            haystacks = [
                lesson.title.lower(),
                lesson.chapter_title.lower(),
                " ".join(lesson.tags).lower(),
                " ".join(
                    [
                        lesson.sections.learning_objective,
                        lesson.sections.explanation,
                        lesson.sections.why_it_matters,
                        lesson.sections.example,
                        lesson.sections.code,
                        lesson.sections.code_explanation,
                        lesson.sections.common_mistakes,
                        lesson.sections.best_practices,
                        lesson.sections.exercise,
                        lesson.sections.solution,
                    ]
                ).lower(),
            ]

            for haystack in haystacks:
                if needle in haystack:
                    pos = haystack.find(needle)
                    start = max(0, pos - 40)
                    excerpt = haystack[start : pos + 100]
                    if start > 0:
                        excerpt = "..." + excerpt
                    if pos + 100 < len(haystack):
                        excerpt = excerpt + "..."

                    summary = self._summaries_in_order[slug]
                    results.append((summary, excerpt.strip()))
                    break

            if len(results) >= 20:
                break

        return results