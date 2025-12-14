# routers/auth.py
from datetime import timedelta
from typing import Any, Dict, Optional
import inspect

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr

from auth import (
    verify_password,
    create_access_token,
    get_user_by_email,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    # Support both async and sync implementations of get_user_by_email
    if inspect.iscoroutinefunction(get_user_by_email):
        user = await get_user_by_email(request.email)
    else:
        user = get_user_by_email(request.email)

    # If user not found or password hash missing -> 401
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    password_hash = user.get("passwordHash") or user.get("password") or user.get(
        "hashed_password"
    )

    if not password_hash or not verify_password(request.password, password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    token_data = {
        "sub": user.get("email"),
        "role": user.get("role", "user"),
        "userId": str(user.get("_id")),
    }

    access_token = create_access_token(
        data=token_data,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    # sanitize user object for response
    user_safe = {
        "id": str(user.get("_id")),
        "name": user.get("name"),
        "email": user.get("email"),
        "role": user.get("role", "user"),
    }

    return LoginResponse(access_token=access_token, user=user_safe)
