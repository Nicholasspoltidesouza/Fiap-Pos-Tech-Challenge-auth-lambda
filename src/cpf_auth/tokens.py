import os
from datetime import datetime, timedelta, timezone

import jwt

ISSUER = os.getenv("JWT_ISSUER", "oficina-auth")
ALGORITHM = "HS512"


def _secret() -> str:
    secret = os.getenv("JWT_SECRET")
    if not secret:
        raise RuntimeError("JWT_SECRET is required")
    return secret


def issue_access_token(client: dict) -> str:
    now = datetime.now(timezone.utc)
    expires_minutes = int(os.getenv("JWT_ACCESS_EXPIRATION_MINUTES", "60"))
    payload = {
        "sub": client["cpf"],
        "userId": client["id"],
        "profile": "CLIENTE",
        "tokenType": "ACCESS",
        "iss": ISSUER,
        "cpf": client["cpf"],
        "clientStatus": client["status"],
        "iat": now,
        "exp": now + timedelta(minutes=expires_minutes),
    }
    return jwt.encode(payload, _secret(), algorithm=ALGORITHM)
