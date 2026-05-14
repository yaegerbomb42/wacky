from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey, JSON, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    org_id: Mapped[int] = mapped_column(Integer, index=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True)
    action: Mapped[str] = mapped_column(String(80), index=True)
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class ToolPermission(Base):
    __tablename__ = "tool_permissions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    org_id: Mapped[int] = mapped_column(Integer, index=True)
    tool_name: Mapped[str] = mapped_column(String(120), index=True)
    mode: Mapped[str] = mapped_column(String(20), default="SEMI")
    requires_human_approval: Mapped[int] = mapped_column(Integer, default=1)

class ApprovalRequest(Base):
    __tablename__ = "approval_requests"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), index=True)
    org_id: Mapped[int] = mapped_column(Integer, index=True)
    action: Mapped[str] = mapped_column(String(120))
    status: Mapped[str] = mapped_column(String(20), default="PENDING")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class BillingQuota(Base):
    __tablename__ = "billing_quotas"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    org_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    monthly_usd_limit: Mapped[float] = mapped_column(Numeric(10, 2), default=100.0)
    monthly_spend_usd: Mapped[float] = mapped_column(Numeric(10, 2), default=0.0)
    rpm_limit: Mapped[int] = mapped_column(Integer, default=60)
