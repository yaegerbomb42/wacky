from fastapi import FastAPI
from app.db.session import Base, engine
from app.api.routes import router as task_router
from app.api.auth_routes import router as auth_router
from app.api.admin_routes import router as admin_router
# Ensure model metadata registration
from app.models import task, event, auth, governance  # noqa: F401

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Agent O")
app.include_router(auth_router)
app.include_router(task_router)
app.include_router(admin_router)

@app.get('/health')
def health():
    return {"status": "ok"}
