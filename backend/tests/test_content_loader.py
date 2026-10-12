import tempfile
import pytest
from pathlib import Path

from app.services.content_loader import ContentLoader

SAMPLE_LESSON = """---
slug: test-lesson
track: python-fundamentals
trackTitle: "Python Fundamentals"
trackOrder: 1
chapter: getting-started
chapterTitle: "Chapter 1 — Getting Started"
chapterOrder: 1
title: "Test Lesson"
difficulty: beginner
order: 1
estimatedMinutes: 10
tags: [test]
---

## Learning Objective

This is the learning objective.

## Explanation

This is the explanation.

## Why It Matters

This is why it matters.

## Example

This is an example.

## Code

```python
print("hello")
```

## Code Explanation

This explains the code.

## Common Mistakes

Common mistakes here.

## Best Practices

Best practices here.

## Exercise

Do this exercise.

## Solution

The solution.

## Mini Quiz

```yaml
- question: "What is 2+2?"
  options: ["3", "4", "5", "6"]
  answer: 1
  explanation: "2+2=4"
```
"""

def test_content_loader_loads_lesson():
    with tempfile.TemporaryDirectory() as tmpdir:
        courses_dir = Path(tmpdir) / "courses" / "python-fundamentals" / "getting-started"
        courses_dir.mkdir(parents=True)
        
        lesson_file = courses_dir / "01-test-lesson.md"
        lesson_file.write_text(SAMPLE_LESSON, encoding="utf-8")
        
        loader = ContentLoader(str(Path(tmpdir) / "courses"))
        loader.load()
        
        lesson = loader.get_lesson("test-lesson")
        
        assert lesson.slug == "test-lesson"
        assert lesson.title == "Test Lesson"
        assert lesson.track == "python-fundamentals"
        assert lesson.chapter == "getting-started"
        assert lesson.difficulty.value == "beginner"
        assert lesson.order == 1
        assert lesson.estimated_minutes == 10
        assert "test" in lesson.tags
        
        # Check sections
        assert "learning objective" in lesson.sections.learning_objective.lower()
        assert "explanation" in lesson.sections.explanation.lower()
        
        # Check quiz (public view carries no answers by design)
        assert len(lesson.quiz) == 1
        assert lesson.quiz[0].question == "What is 2+2?"
        assert lesson.quiz[0].options == ["3", "4", "5", "6"]
        assert not hasattr(lesson.quiz[0], "answer")

        # Answers stay server-side via get_quiz_answers()
        answers = loader.get_quiz_answers("test-lesson")
        assert len(answers) == 1
        assert answers[0].answer == 1

def test_content_loader_course_tree():
    with tempfile.TemporaryDirectory() as tmpdir:
        courses_dir = Path(tmpdir) / "courses" / "python-fundamentals" / "getting-started"
        courses_dir.mkdir(parents=True)
        
        (courses_dir / "01-first.md").write_text(SAMPLE_LESSON.replace("test-lesson", "first-lesson").replace("Test Lesson", "First Lesson"), encoding="utf-8")
        (courses_dir / "02-second.md").write_text(SAMPLE_LESSON.replace("test-lesson", "second-lesson").replace("Test Lesson", "Second Lesson").replace("order: 1", "order: 2"), encoding="utf-8")
        
        loader = ContentLoader(str(Path(tmpdir) / "courses"))
        loader.load()
        
        tracks = loader.get_course_tree()
        
        assert len(tracks) == 1
        assert tracks[0].key == "python-fundamentals"
        assert len(tracks[0].chapters) == 1
        assert tracks[0].chapters[0].key == "getting-started"
        assert len(tracks[0].chapters[0].lessons) == 2
        
        lessons = tracks[0].chapters[0].lessons
        assert lessons[0].slug == "first-lesson"
        assert lessons[1].slug == "second-lesson"
        
        # Check navigation
        first_lesson = loader.get_lesson("first-lesson")
        assert first_lesson.navigation.next is not None
        assert first_lesson.navigation.next.slug == "second-lesson"
        assert first_lesson.navigation.previous is None
        
        second_lesson = loader.get_lesson("second-lesson")
        assert second_lesson.navigation.previous is not None
        assert second_lesson.navigation.previous.slug == "first-lesson"
        assert second_lesson.navigation.next is None

def test_content_loader_search():
    with tempfile.TemporaryDirectory() as tmpdir:
        courses_dir = Path(tmpdir) / "courses" / "python-fundamentals" / "getting-started"
        courses_dir.mkdir(parents=True)
        
        (courses_dir / "01-variables.md").write_text(SAMPLE_LESSON.replace("test-lesson", "variables").replace("Test Lesson", "Variables and Types").replace("learning objective", "Learn about variables"), encoding="utf-8")
        (courses_dir / "02-functions.md").write_text(SAMPLE_LESSON.replace("test-lesson", "functions").replace("Test Lesson", "Functions").replace("learning objective", "Learn about functions"), encoding="utf-8")
        
        loader = ContentLoader(str(Path(tmpdir) / "courses"))
        loader.load()
        
        results = loader.search("variables")
        
        assert len(results) == 1
        assert results[0][0].slug == "variables"
        assert "variables" in results[0][1].lower()

def test_content_loader_malformed():
    with tempfile.TemporaryDirectory() as tmpdir:
        courses_dir = Path(tmpdir) / "courses" / "python-fundamentals" / "getting-started"
        courses_dir.mkdir(parents=True)
        
        # Valid lesson
        (courses_dir / "01-valid.md").write_text(SAMPLE_LESSON, encoding="utf-8")
        
        # Malformed - missing frontmatter
        (courses_dir / "02-invalid.md").write_text("# No frontmatter\n\n## Learning Objective\nTest", encoding="utf-8")
        
        loader = ContentLoader(str(Path(tmpdir) / "courses"))
        loader.load()
        
        # Valid lesson should load
        assert "test-lesson" in loader._lessons_by_slug
        
        # Invalid should be in malformed
        malformed = loader.get_malformed_files()
        assert len(malformed) == 1
        assert "02-invalid.md" in list(malformed.keys())[0]

if __name__ == "__main__":
    pytest.main([__file__, "-v"])