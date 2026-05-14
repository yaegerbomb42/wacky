from sqlalchemy import select
from app.db.session import SessionLocal
from app.models.task import Task
from app.models.event import TaskEvent


def execute_task(task_id: int):
    db = SessionLocal()
    try:
        task = db.scalar(select(Task).where(Task.id == task_id))
        if not task:
            return
        task.status = "RUNNING"
        db.add(TaskEvent(task_id=task.id, type="status", payload={"status": "RUNNING"}))
        db.commit()

        # Placeholder for orchestrator execution
        task.result = {
            "message": "Execution completed by worker scaffold.",
            "confirm_fix": {
                "confirm": True,
                "fix_endpoint": f"/tasks/{task.id}/annotations"
            }
        }
        task.status = "NEEDS_CONFIRMATION"
        db.add(TaskEvent(task_id=task.id, type="status", payload={"status": "NEEDS_CONFIRMATION"}))
        db.commit()
    finally:
        db.close()
