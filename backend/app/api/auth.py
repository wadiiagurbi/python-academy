from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.user import UserCreate, UserRead, Token, LoginRequest, RefreshRequest
from app.services.auth_service import AuthService, get_auth_service, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token)
async def register(data: UserCreate, auth_service: AuthService = Depends(get_auth_service)):
    try:
        await auth_service.register(data)
    except Exception:
        raise
    return await auth_service.login(data.email, data.password)


@router.post("/login", response_model=Token)
async def login(data: LoginRequest, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.login(data.email, data.password)


@router.post("/refresh", response_model=Token)
async def refresh(data: RefreshRequest, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.refresh(data.refresh_token)


@router.get("/me", response_model=UserRead)
async def get_me(current_user = Depends(get_current_user)):
    return UserRead.model_validate(current_user)