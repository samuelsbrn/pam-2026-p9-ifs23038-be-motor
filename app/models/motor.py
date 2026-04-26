from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.extensions import Base


class Motor(Base):
    __tablename__ = "motors"

    id = Column(Integer, primary_key=True)
    title = Column(String(150), nullable=False)
    genre = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    popularity_reason = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
