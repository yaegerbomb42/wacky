from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import get_db
from app.models.auth import Organization, User
from app.models.governance import BillingQuota
from app.schemas.auth import RegisterIn, LoginIn, TokenOut
from app.auth.security import hash_password, verify_password, create_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post('/register', response_model=TokenOut)
def register(payload: RegisterIn, db: Session = Depends(get_db)):
    if db.scalar(select(User).where(User.email == payload.email)):
        raise HTTPException(status_code=400, detail="Email already registered")
    org = Organization(name=payload.org_name)
    db.add(org); db.commit(); db.refresh(org)
    user = User(email=payload.email, hashed_password=hash_password(payload.password), org_id=org.id, role="admin")
    db.add(user)
    db.add(BillingQuota(org_id=org.id))
    db.commit()
    return TokenOut(access_token=create_token(payload.email, org.id, user.role))

@router.post('/login', response_model=TokenOut)
def login(payload: LoginIn, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == payload.email))
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Bad credentials")
    return TokenOut(access_token=create_token(user.email, user.org_id, user.role))
