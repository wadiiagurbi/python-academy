from tests.conftest import auth_headers

# backend/courses/python-fundamentals/getting-started/01-what-is-python.md
LESSON_SLUG = "what-is-python"
CORRECT_ANSWERS = [1, 2]


async def test_quiz_attempt_all_correct(client):
    headers = await auth_headers(client, "quiz1@example.com")

    resp = await client.post(
        f"/api/quizzes/{LESSON_SLUG}/attempt",
        json={"answers": CORRECT_ANSWERS},
        headers=headers,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["score"] == len(CORRECT_ANSWERS)
    assert data["total_questions"] == len(CORRECT_ANSWERS)
    assert data["percentage"] == 100.0
    assert all(r["is_correct"] for r in data["results"])


async def test_quiz_attempt_all_wrong(client):
    headers = await auth_headers(client, "quiz2@example.com")
    wrong_answers = [(a + 1) % 4 for a in CORRECT_ANSWERS]

    resp = await client.post(
        f"/api/quizzes/{LESSON_SLUG}/attempt",
        json={"answers": wrong_answers},
        headers=headers,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["score"] == 0
    assert data["percentage"] == 0.0
    assert not any(r["is_correct"] for r in data["results"])


async def test_quiz_attempt_wrong_answer_count(client):
    headers = await auth_headers(client, "quiz3@example.com")

    resp = await client.post(
        f"/api/quizzes/{LESSON_SLUG}/attempt",
        json={"answers": [1]},
        headers=headers,
    )
    assert resp.status_code == 400


async def test_quiz_attempt_unknown_lesson(client):
    headers = await auth_headers(client, "quiz4@example.com")

    resp = await client.post(
        "/api/quizzes/does-not-exist/attempt",
        json={"answers": [0]},
        headers=headers,
    )
    assert resp.status_code == 404


async def test_progress_quiz_stats_are_percentages(client):
    # Regression test: aggregate quiz_stats must report percentages (0-100),
    # not raw correct-answer counts (e.g. 2/2 correct should read 100, not 2).
    headers = await auth_headers(client, "quiz5@example.com")

    await client.post(
        f"/api/quizzes/{LESSON_SLUG}/attempt",
        json={"answers": CORRECT_ANSWERS},
        headers=headers,
    )

    progress = (await client.get("/api/progress", headers=headers)).json()
    stats = progress["quiz_stats"]
    assert stats["total_attempts"] == 1
    assert stats["average_score"] == 100.0
    assert stats["best_score"] == 100.0
