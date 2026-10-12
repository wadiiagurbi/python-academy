from tests.conftest import auth_headers

LESSON_SLUG = "what-is-python"


async def test_progress_starts_at_zero(client):
    headers = await auth_headers(client, "progress1@example.com")

    resp = await client.get("/api/progress", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["completed_lessons"] == []
    assert data["completion_percentage"] == 0
    assert data["total_lessons"] > 0


async def test_mark_lesson_complete_and_incomplete(client):
    headers = await auth_headers(client, "progress2@example.com")

    complete_resp = await client.post(f"/api/progress/lessons/{LESSON_SLUG}/complete", headers=headers)
    assert complete_resp.status_code == 204

    progress = (await client.get("/api/progress", headers=headers)).json()
    assert LESSON_SLUG in progress["completed_lessons"]
    assert progress["completion_percentage"] > 0
    assert progress["last_lesson_slug"] == LESSON_SLUG

    incomplete_resp = await client.delete(f"/api/progress/lessons/{LESSON_SLUG}/complete", headers=headers)
    assert incomplete_resp.status_code == 204

    progress_after = (await client.get("/api/progress", headers=headers)).json()
    assert LESSON_SLUG not in progress_after["completed_lessons"]


async def test_mark_unknown_lesson_returns_404(client):
    headers = await auth_headers(client, "progress3@example.com")

    resp = await client.post("/api/progress/lessons/does-not-exist/complete", headers=headers)
    assert resp.status_code == 404
