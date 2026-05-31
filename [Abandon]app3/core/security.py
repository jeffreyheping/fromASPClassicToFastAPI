"""安全工具 - 密码加密和JWT处理"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import OAuth2PasswordBearer
import hashlib

# JWT配置
SECRET_KEY = "your-secret-key-here-change-in-production"  # 生产环境要修改
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 标准：token端点路径
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


def hash_password(password: str) -> str:
    """哈希密码 - 使用SHA256（简单教学用，生产环境请用bcrypt）"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return hash_password(plain_password) == hashed_password


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建JWT访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """解码JWT令牌，返回payload或None"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


# ============================================================
# FastAPI 依赖注入：OAuth2 JWT 认证（供 Vue 版 API 路由使用）
# ============================================================

async def get_current_user_oauth2(token: str = Depends(oauth2_scheme)) -> dict:
    """OAuth2 标准：从 Bearer token 中解析用户信息"""
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭据",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {
        "id": int(payload["sub"]),
        "username": payload["username"],
        "role": payload["role"],
    }


# ============================================================
# FastAPI 依赖注入：Session 认证（供 HTMX 版 Web 路由使用）
# ============================================================

def get_current_user_session(request: Request) -> dict:
    """从 Session 中获取用户信息，未登录返回401"""
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未登录，请先登录",
        )
    return {
        "id": user_id,
        "username": request.session.get("username"),
        "role": request.session.get("role"),
    }
