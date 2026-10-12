from tests.conftest import auth_headers


async def test_pipeline_crud_happy_path(client):
    headers = await auth_headers(client, "pipeline1@example.com")

    create_resp = await client.post(
        "/api/pipelines",
        json={"name": "My Pipeline", "description": "A test pipeline", "config": {}},
        headers=headers,
    )
    assert create_resp.status_code == 201
    pipeline = create_resp.json()
    pipeline_id = pipeline["id"]
    assert pipeline["name"] == "My Pipeline"
    assert pipeline["status"] == "draft"

    list_resp = await client.get("/api/pipelines", headers=headers)
    assert list_resp.status_code == 200
    assert any(p["id"] == pipeline_id for p in list_resp.json())

    get_resp = await client.get(f"/api/pipelines/{pipeline_id}", headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == pipeline_id

    update_resp = await client.put(
        f"/api/pipelines/{pipeline_id}",
        json={"name": "Renamed Pipeline"},
        headers=headers,
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["name"] == "Renamed Pipeline"

    delete_resp = await client.delete(f"/api/pipelines/{pipeline_id}", headers=headers)
    assert delete_resp.status_code == 204

    missing_resp = await client.get(f"/api/pipelines/{pipeline_id}", headers=headers)
    assert missing_resp.status_code == 404


async def test_pipeline_execute_runs_configured_steps(client):
    headers = await auth_headers(client, "pipeline2@example.com")

    create_resp = await client.post(
        "/api/pipelines",
        json={
            "name": "Executable Pipeline",
            "config": {
                "steps": [
                    {"type": "ingest", "name": "Load sample data", "config": {"source": "sample"}},
                    {"type": "clean", "name": "Clean data", "config": {}},
                ]
            },
        },
        headers=headers,
    )
    pipeline_id = create_resp.json()["id"]

    execute_resp = await client.post(
        f"/api/pipelines/{pipeline_id}/execute", json={}, headers=headers
    )
    assert execute_resp.status_code == 200
    data = execute_resp.json()
    assert data["success"] is True
    assert len(data["steps_executed"]) == 2

    final = (await client.get(f"/api/pipelines/{pipeline_id}", headers=headers)).json()
    assert final["status"] == "completed"


async def test_pipeline_isolated_per_user(client):
    headers_a = await auth_headers(client, "owner-a@example.com")
    headers_b = await auth_headers(client, "owner-b@example.com")

    create_resp = await client.post(
        "/api/pipelines", json={"name": "Owner A Pipeline"}, headers=headers_a
    )
    pipeline_id = create_resp.json()["id"]

    resp = await client.get(f"/api/pipelines/{pipeline_id}", headers=headers_b)
    assert resp.status_code == 404
