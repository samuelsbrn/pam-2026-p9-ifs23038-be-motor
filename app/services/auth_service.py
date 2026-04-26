from datetime import datetime, timedelta, timezone

import jwt
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from app.config import Config
from app.extensions import SessionLocal
from app.models.user import User


def seed_default_user():
    session = SessionLocal()

    try:
        username = Config.DEFAULT_ADMIN_USERNAME.strip()
        password = Config.DEFAULT_ADMIN_PASSWORD
        role = Config.DEFAULT_ADMIN_ROLE.strip() or "admin"

        user = session.query(User).filter(User.username == username).first()

        if user:
            return user

        user = User(
            username=username,
            password_hash=generate_password_hash(password),
            role=role,
        )
        session.add(user)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            user = session.query(User).filter(User.username == username).first()

        return user

    finally:
        session.close()


def authenticate_user(username: str, password: str):
    session = SessionLocal()

    try:
        user = session.query(User).filter(User.username == username).first()

        if not user:
            return None

        if not check_password_hash(user.password_hash, password):
            return None

        return user

    finally:
        session.close()


def generate_auth_token(user: User):
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user.id),
        "username": user.username,
        "role": user.role,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(hours=Config.JWT_EXPIRES_IN_HOURS)).timestamp()),
    }
    return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm="HS256")


def verify_auth_token(token: str):
    payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
    user_id = int(payload["sub"])

    session = SessionLocal()

    try:
        user = session.query(User).filter(User.id == user_id).first()
        return user
    finally:
        session.close()


def serialize_user(user: User):
    return {
        "id": user.id,
        "username": user.username,
        "role": user.role,
        "created_at": user.created_at.isoformat(),
    }
