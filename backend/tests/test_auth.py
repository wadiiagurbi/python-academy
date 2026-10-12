async def test_register_returns_tokens(client):
    resp = await client.post(
        "/api/auth/register",
        json={"email": "alice@example.com", "display_name": "Alice", "password": "SecurePass123!"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


async def test_register_duplicate_email_returns_error_not_crash(client):
    payload = {"email": "bob@example.com", "display_name": "Bob", "password": "SecurePass123!"}
    first = await client.post("/api/auth/register", json=payload)
    assert first.status_code == 200

    # Regression test: AuthService.__init__ previously never set self.session,
    # so this path raised AttributeError -> 500 instead of a proper 401.
    second = await client.post("/api/auth/register", json=payload)
    assert second.status_code == 401
    assert second.json()["error"]["message"] == "Email already registered"


async def test_login_success(client):
    payload = {"email": "carol@example.com", "display_name": "Carol", "password": "SecurePass123!"}
    await client.post("/api/auth/register", json=payload)

    resp = await client.post(
        "/api/auth/login", json={"email": payload["email"], "password": payload["password"]}
    )
    assert resp.status_code == 200
    assert "access_token" in resp.json()


async def test_login_wrong_password(client):
    payload = {"email": "dave@example.com", "display_name": "Dave", "password": "SecurePass123!"}
    await client.post("/api/auth/register", json=payload)

    resp = await client.post(
        "/api/auth/login", json={"email": payload["email"], "password": "WrongPass123!"}
    )
    assert resp.status_code == 401


async def test_me_with_valid_token(client):
    payload = {"email": "erin@example.com", "display_name": "Erin", "password": "SecurePass123!"}
    register_resp = await client.post("/api/auth/register", json=payload)
    token = register_resp.json()["access_token"]

    resp = await client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["email"] == payload["email"]
    assert data["display_name"] == payload["display_name"]


async def test_me_without_token(client):
    resp = await client.get("/api/auth/me")
    assert resp.status_code == 401


async def test_me_with_invalid_token(client):
    resp = await client.get("/api/auth/me", headers={"Authorization": "Bearer not-a-real-token"})
    assert resp.status_code == 401
