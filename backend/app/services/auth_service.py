from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.exceptions import AuthenticationException, AuthorizationException
from app.core.security import decode_token, get_password_hash, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import Token, TokenPayload, UserCreate, UserRead

security = HTTPBearer(auto_error=False)


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)

    async def register(self, data: UserCreate) -> UserRead:
        existing = await self.user_repo.get_by_email(data.email)
        if existing:
            raise AuthenticationException("Email already registered")

        user = User(
            email=data.email,
            hashed_password=get_password_hash(data.password),
            display_name=data.display_name,
        )
        user = await self.user_repo.create(user)
        await self.session.commit()
        return UserRead.model_validate(user)

    async def login(self, email: str, password: str) -> Token:
        user = await self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise AuthenticationException("Invalid credentials")
        if not user.is_active:
            raise AuthenticationException("Account is disabled")

        access_token = self._create_access_token(user.id)
        refresh_token = self._create_refresh_token(user.id)
        return Token(access_token=access_token, refresh_token=refresh_token)

    async def refresh(self, refresh_token: str) -> Token:
        try:
            payload = decode_token(refresh_token)
            if payload.get("type") != "refresh":
                raise AuthenticationException("Invalid token type")
            user_id = int(payload["sub"])
        except Exception:
            raise AuthenticationException("Invalid or expired token")

        user = await self.user_repo.get_by_id(user_id)
        if not user or not user.is_active:
            raise AuthenticationException("User not found or inactive")

        access_token = self._create_access_token(user.id)
        new_refresh_token = self._create_refresh_token(user.id)
        return Token(access_token=access_token, refresh_token=new_refresh_token)

    async def get_current_user(
        self, credentials: HTTPAuthorizationCredentials = Depends(security)
    ) -> User:
        if not credentials:
            raise AuthenticationException("Not authenticated")

        try:
            payload = decode_token(credentials.credentials)
            if payload.get("type") != "access":
                raise AuthenticationException("Invalid token type")
            user_id = int(payload["sub"])
        except Exception:
            raise AuthenticationException("Invalid or expired token")

        user = await self.user_repo.get_by_id(user_id)
        if not user or not user.is_active:
            raise AuthenticationException("User not found or inactive")

        return user

    async def get_current_user_optional(
        self, credentials: HTTPAuthorizationCredentials = Depends(security)
    ) -> User | None:
        if not credentials:
            return None
        try:
            return await self.get_current_user(credentials)
        except AuthenticationException:
            return None

    def _create_access_token(self, user_id: int) -> str:
        from app.core.security import create_access_token
        return create_access_token(str(user_id))

    def _create_refresh_token(self, user_id: int) -> str:
        from app.core.security import create_refresh_token
        return create_refresh_token(str(user_id))


async def get_auth_service(session: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(session)


async def get_current_user(
    auth_service: AuthService = Depends(get_auth_service),
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> User:
    return await auth_service.get_current_user(credentials)


async def get_current_user_optional(
    auth_service: AuthService = Depends(get_auth_service),
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> User | None:
    return await auth_service.get_current_user_optional(credentials)