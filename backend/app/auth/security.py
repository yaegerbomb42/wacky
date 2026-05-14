import os
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET = os.getenv("JWT_SECRET", "dev-secret")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


def create_token(sub: str, org_id: int, role: str) -> str:
    payload = {
        "sub": sub,
        "org_id": org_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=12),
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")


def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET, algorithms=["HS256"])
