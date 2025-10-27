# 🔐 Project 2 — JWKS Server with SQLite Persistence

## 📌 Overview

This project extends a standard JWKS (JSON Web Key Set) server by adding **SQLite-backed storage** for private RSA keys. Persisting keys in a database ensures they remain available across server restarts, increasing reliability and supporting secure authentication flows.

Additionally, this implementation protects against **SQL injection** using parameterized database queries. JWTs can be issued with either valid or intentionally expired keys (controlled via query parameters), enabling testing of expiration logic.

Public keys are made available through a `.well-known` JWKS endpoint for third-party verification.

---

## ✨ Key Features

- ✅ SQLite persistence for RSA private keys  
- ✅ Automatically generates one expired & one valid key on startup (if DB empty)  
- ✅ JWT issuance via `/auth` endpoint  
- ✅ Expired key selection via `?expired=1`  
- ✅ Public keys exposed in JWKS format at `/.well-known/jwks.json`  
- ✅ Parameterized DB queries (SQLi mitigation)  
- ✅ Includes Pytest test suite & coverage instructions  
- ✅ Gradebot-compatible  

---

## 🗄 Database Schema

Database filename:
```
totally_not_my_privateKeys.db
```

Table schema:
```sql
CREATE TABLE IF NOT EXISTS keys(
    kid INTEGER PRIMARY KEY AUTOINCREMENT,
    key BLOB NOT NULL,
    exp INTEGER NOT NULL
);
```

- `kid` — Unique key identifier  
- `key` — Serialized PEM private key (stored as BLOB)  
- `exp` — Expiration UNIX timestamp

Keys are stored as serialized PEM so they can be reloaded on demand.

---

## 🔑 Endpoints

### `POST /auth`

Issues a JWT signed with:
- Valid (non-expired) private key by default
- Expired key when `?expired=1` is present

**Example:**
```bash
curl -X POST http://127.0.0.1:8080/auth
```

Expired key:
```bash
curl -X POST "http://127.0.0.1:8080/auth?expired=1"
```

Response:
```json
{ "token": "<jwt-here>" }
```

---

### `GET /.well-known/jwks.json`

Returns all **valid** public keys in JWKS format.

**Example:**
```bash
curl http://127.0.0.1:8080/.well-known/jwks.json
```

Response example:
```json
{
  "keys": [
    {
      "kid": "1",
      "kty": "RSA",
      "alg": "RS256",
      "use": "sig",
      "n": "...",
      "e": "AQAB"
    }
  ]
}
```

Only **non-expired** keys are included.

---

## 🛡 Security Protections

### SQL Injection Mitigation
All SQL database operations use **parameterized queries**, for example:
```python
cur.execute("SELECT kid, key, exp FROM keys WHERE exp > ?", (now,))
```
Never construct SQL using untrusted string concatenation.

### Private Keys
Private keys are stored on the server only. Only public keys are exposed through JWKS.

---

## ▶️ Running Locally (Windows / Linux / Mac)

1. **Clone the repo** (replace `YOUR_REPO_URL` with your GitHub link):
```bash
git clone YOUR_REPO_URL
cd CSCE3550-Project_2
```

2. **Create virtual environment (recommended)**:
```bash
python3 -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```
_If `requirements.txt` is not provided_, install manually:
```bash
pip install Flask pyjwt cryptography pytest pytest-cov
```

4. **Run the server**:
```bash
python main.py
```
By default the server listens on `http://127.0.0.1:8080`.

5. **Smoke test** (in another terminal):
```bash
curl -X POST http://127.0.0.1:8080/auth
curl -X POST "http://127.0.0.1:8080/auth?expired=1"
curl http://127.0.0.1:8080/.well-known/jwks.json
```

---

## 🧪 Tests & Coverage

Add the included tests (folder `tests/`) and run:

```bash
pytest --cov=. -q
```

Expect output showing coverage percent. The project requires **>80%** coverage.

If pytest reports "No tests collected", ensure:
- Tests are in `tests/` directory
- Test files begin with `test_` (e.g., `tests/test_api.py`)
- You run pytest from the project root

Example minimal test file `tests/test_api.py`:
```python
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app

def test_auth_valid():
    client = app.test_client()
    res = client.post("/auth")
    assert res.status_code == 200
    assert "token" in res.get_json()

def test_auth_expired():
    client = app.test_client()
    res = client.post("/auth?expired=1")
    assert res.status_code == 200
    assert "token" in res.get_json()

def test_jwks():
    client = app.test_client()
    res = client.get("/.well-known/jwks.json")
    assert res.status_code == 200
    data = res.get_json()
    assert "keys" in data
```

---

## 🤖 Gradebot (Project 2) Instructions

With the server running on port `8080`, run the Gradebot client that was supplied with the class:

```bash
# from the project folder, where the gradebot script is present
project2 --port 8080
```

You should see an ASCII rubric showing items and points. Take a screenshot and include it in `/screenshots/gradebot.png`.

---

## 📂 Repository Structure

```
CSCE3550-Project_2/
│
├── main.py
├── requirements.txt
├── totally_not_my_privateKeys.db
├── README_Project2.md  <-- this file
├── tests/
│   └── test_api.py
└── screenshots/
    ├── gradebot.png
    └── coverage.png
```

---

## 📝 Notes & Best Practices

- The server will generate keys on first run if the DB is empty. Keys will accumulate on each fresh DB or if you delete the DB.
- For production use: never store unencrypted private keys in plaintext; use an HSM or encrypted key store.
- Keep `totally_not_my_privateKeys.db` out of public repos if keys are real — for this assignment it's acceptable.

---

## 👤 Author / Submission Info

**Name:** _Srinivasa Chivukula_  
**EUID:** _ssc0167_  
**Course:** CSCE 3550 — Cybersecurity  
**Instructor:** _Jacob Hochstetler_  

---

## 📎 Additional Resources

- SQLite docs: https://www.sqlite.org/docs.html  
- PyJWT: https://pyjwt.readthedocs.io/  
- cryptography: https://cryptography.io/  
- Flask: https://flask.palletsprojects.com/
