from datetime import datetime
from sqlalchemy import String, DateTime, Integer, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    org_id: Mapped[int] = mapped_column(Integer, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    autonomy_mode: Mapped[str] = mapped_column(String(20), default="SEMI")
    status: Mapped[str] = mapped_column(String(40), default="NEW", index=True)
    priority: Mapped[int] = mapped_column(Integer, default=100)
    time_budget_minutes: Mapped[int] = mapped_column(Integer, default=60)
    plan: Mapped[dict] = mapped_column(JSON, default=dict)
    result: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
