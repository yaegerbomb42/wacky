from pydantic import BaseModel
from typing import Literal, Optional

class TaskCreate(BaseModel):
    title: str
    prompt: str
    autonomy_mode: Literal["MANUAL", "SEMI", "FULL"] = "SEMI"
    time_budget_minutes: int = 60
    priority: int = 100

class TaskOut(BaseModel):
    id: int
    title: str
    prompt: str
    autonomy_mode: str
    status: str
    time_budget_minutes: int
    priority: int
    plan: dict
    result: dict

    class Config:
        from_attributes = True

class AnnotationPayload(BaseModel):
    task_id: int
    comment: str
    x: Optional[float] = None
    y: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
    dom_selector: Optional[str] = None
