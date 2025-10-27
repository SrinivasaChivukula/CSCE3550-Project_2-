import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

def test_auth_valid():
    client = app.test_client()
    res = client.post("/auth")
    assert res.status_code == 200
    data = res.get_json()
    assert "token" in data


def test_auth_valid():
    client = app.test_client()
    res = client.post("/auth")
    assert res.status_code == 200
    data = res.get_json()
    assert "token" in data

def test_auth_expired():
    client = app.test_client()
    res = client.post("/auth?expired=1")
    assert res.status_code == 200
    data = res.get_json()
    assert "token" in data

def test_jwks():
    client = app.test_client()
    res = client.get("/.well-known/jwks.json")
    assert res.status_code == 200
    data = res.get_json()
    assert "keys" in data
    assert len(data["keys"]) >= 1
    for k in data["keys"]:
        assert "kid" in k
        assert "n" in k
        assert "e" in k
