from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from auth_utils import hash_password, verify_password, create_access_token, get_current_user
from config import settings
from database import get_db
from models.user import User
from schemas.user import UserCreate, UserResponse, Token, LoginRequest
from services.session import create_session, invalidate_session

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token, status_code=201)
async def register(request: Request, data: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check if email exists
    existing = await db.execute(select(User).where(User.email == data.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    # Determine role
    user_count = await db.execute(select(func.count()).select_from(User))
    count = user_count.scalar()

    if count == 0:
        # First user: must provide admin_secret to bootstrap
        if data.admin_secret != settings.ADMIN_SECRET:
            raise HTTPException(status_code=403, detail="Admin secret inválido para primeiro usuário")
        role = "admin"
    else:
        # Subsequent users: admin_secret required (only admins know it)
        if data.admin_secret != settings.ADMIN_SECRET:
            raise HTTPException(status_code=403, detail="Apenas administradores podem criar novos usuários")
        role = "vendas"

    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        name=data.name,
        role=role,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    token, jti = create_access_token(str(user.id))
    await create_session(str(user.id), jti)

    return Token(access_token=token, user=UserResponse.model_validate(user))


@router.post("/login", response_model=Token)
async def login(request: Request, data: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Email ou senha inválidos")

    token, jti = create_access_token(str(user.id))
    await create_session(str(user.id), jti)

    return Token(access_token=token, user=UserResponse.model_validate(user))


@router.get("/me", response_model=UserResponse)
async def me(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)


@router.post("/users", response_model=UserResponse, status_code=201)
async def create_user(
    data: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Admin creates a new user. No admin_secret needed - just be logged in as admin."""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Apenas administradores podem criar usuários")

    existing = await db.execute(select(User).where(User.email == data.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        name=data.name,
        role="vendas",
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return UserResponse.model_validate(user)


@router.post("/logout", status_code=204)
async def logout(current_user: User = Depends(get_current_user)):
    await invalidate_session(str(current_user.id))
