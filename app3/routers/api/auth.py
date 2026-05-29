"""API认证路由 - OAuth2标准JWT登录注册（供Vue前端使用）"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel

from core.database import get_db
from core.models import User
from core import security

router = APIRouter(prefix="/api/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    role: str

    model_config = {"from_attributes": True}


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    """用户注册 - 默认role为guest"""
    # 检查用户名是否已存在
    existing = db.query(User).filter(User.username == data.username).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    
    # 创建新用户
    user = User(
        username=data.username,
        password_hash=security.hash_password(data.password),
        role="guest"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """OAuth2标准登录端点 - 返回JWT令牌
    
    使用表单格式 (username, password)，Swagger UI 会自动显示锁图标
    """
    # 查找用户
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 创建JWT令牌
    access_token = security.create_access_token(
        data={"sub": str(user.id), "username": user.username, "role": user.role}
    )
    
    # OAuth2 标准返回格式
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("/me", response_model=UserResponse)
def get_current_user(
    user: dict = Depends(security.get_current_user_oauth2),
    db: Session = Depends(get_db)
):
    """获取当前登录用户信息（需要OAuth2认证）"""
    db_user = db.query(User).filter(User.id == user["id"]).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    return db_user
