from pydantic import BaseModel, EmailStr

class RegisterIn(BaseModel):
    org_name: str
    email: EmailStr
    password: str

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
