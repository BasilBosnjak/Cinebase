from pydantic import BaseModel, EmailStr
from .user import UserResponse

class LoginRequest(BaseModel):
    email: EmailStr

class LoginResponse(BaseModel):
    user: UserResponse
