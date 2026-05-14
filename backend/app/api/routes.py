from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import get_db
from app.models.task import Task
from app.models.event import TaskEvent
from app.models.governance import AuditLog, ApprovalRequest, BillingQuota
from app.schemas.task import TaskCreate, TaskOut, AnnotationPayload
from app.services.planner import derive_plan
from app.services.policy import validate_task
from app.worker.queue import queue
from app.worker.jobs import execute_task
from app.api.deps import current_claims
from app.services.rbac import require_role

router = APIRouter(tags=["tasks"])

@router.post('/tasks', response_model=TaskOut)
def create_task(payload: TaskCreate, claims=Depends(current_claims), db: Session = Depends(get_db)):
    if not require_role(claims["role"], "operator"):
        raise HTTPException(status_code=403, detail="Insufficient role")

    quota = db.scalar(select(BillingQuota).where(BillingQuota.org_id == claims["org_id"]))
    if quota and float(quota.monthly_spend_usd) >= float(quota.monthly_usd_limit):
        raise HTTPException(status_code=402, detail="Monthly quota exceeded")

    ok, reason = validate_task(payload.prompt)
    if not ok:
        raise HTTPException(status_code=400, detail=reason)

    task = Task(org_id=claims["org_id"], title=payload.title, prompt=payload.prompt, autonomy_mode=payload.autonomy_mode,
                time_budget_minutes=payload.time_budget_minutes, priority=payload.priority, status="PLANNED",
                plan=derive_plan(payload.prompt, payload.time_budget_minutes))
    db.add(task); db.commit(); db.refresh(task)
    db.add(TaskEvent(task_id=task.id, type="planned", payload=task.plan))
    db.add(AuditLog(org_id=claims["org_id"], user_id=0, action="task_created", payload={"task_id": task.id}))

    if payload.autonomy_mode == "FULL":
        db.add(ApprovalRequest(task_id=task.id, org_id=claims["org_id"], action="full_autonomy_execute"))
        task.status = "NEEDS_CONFIRMATION"
    else:
        queue.enqueue(execute_task, task.id)
    db.commit()
    return task

@router.get('/tasks', response_model=list[TaskOut])
def list_tasks(claims=Depends(current_claims), db: Session = Depends(get_db)):
    tasks = db.scalars(select(Task).where(Task.org_id == claims["org_id"]).order_by(Task.priority.asc(), Task.created_at.asc())).all()
    return list(tasks)

@router.post('/tasks/{task_id}/annotations')
def add_annotation(task_id: int, payload: AnnotationPayload, claims=Depends(current_claims), db: Session = Depends(get_db)):
    task = db.scalar(select(Task).where(Task.id == task_id, Task.org_id == claims["org_id"]))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.add(TaskEvent(task_id=task_id, type="annotation", payload=payload.model_dump()))
    db.add(AuditLog(org_id=claims["org_id"], user_id=0, action="task_annotated", payload={"task_id": task_id}))
    task.status = "REVISION_REQUESTED"
    db.commit()
    queue.enqueue(execute_task, task.id)
    return {"ok": True}

@router.post('/approvals/{approval_id}/decision')
def decide_approval(approval_id: int, approve: bool, claims=Depends(current_claims), db: Session = Depends(get_db)):
    approval = db.scalar(select(ApprovalRequest).where(ApprovalRequest.id == approval_id, ApprovalRequest.org_id == claims["org_id"]))
    if not approval:
        raise HTTPException(status_code=404, detail="Approval not found")
    approval.status = "APPROVED" if approve else "REJECTED"
    if approve:
        queue.enqueue(execute_task, approval.task_id)
    db.add(AuditLog(org_id=claims["org_id"], user_id=0, action="approval_decision", payload={"approval_id": approval.id, "approve": approve}))
    db.commit()
    return {"ok": True, "status": approval.status}
