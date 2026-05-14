from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import get_db
from app.models.governance import ToolPermission, BillingQuota, AuditLog
from app.api.deps import current_claims
from app.services.rbac import require_role

router = APIRouter(prefix='/admin', tags=['admin'])

@router.post('/tool-permissions')
def set_tool_permission(tool_name: str, mode: str, requires_human_approval: int = 1, claims=Depends(current_claims), db: Session = Depends(get_db)):
    if not require_role(claims['role'], 'admin'):
        raise HTTPException(status_code=403, detail='Admin required')
    perm = ToolPermission(org_id=claims['org_id'], tool_name=tool_name, mode=mode, requires_human_approval=requires_human_approval)
    db.add(perm)
    db.add(AuditLog(org_id=claims['org_id'], user_id=0, action='tool_permission_set', payload={'tool_name': tool_name, 'mode': mode}))
    db.commit()
    return {'ok': True}

@router.get('/billing')
def get_billing(claims=Depends(current_claims), db: Session = Depends(get_db)):
    quota = db.scalar(select(BillingQuota).where(BillingQuota.org_id == claims['org_id']))
    return {'monthly_limit': float(quota.monthly_usd_limit), 'monthly_spend': float(quota.monthly_spend_usd), 'rpm_limit': quota.rpm_limit}

@router.get('/audit')
def audit_logs(claims=Depends(current_claims), db: Session = Depends(get_db)):
    logs = db.scalars(select(AuditLog).where(AuditLog.org_id == claims['org_id']).order_by(AuditLog.id.desc()).limit(200)).all()
    return [{'id': l.id, 'action': l.action, 'payload': l.payload, 'created_at': l.created_at.isoformat()} for l in logs]
