"""Pydantic 数据模型（请求/响应验证）"""
from pydantic import BaseModel
from typing import Optional


class TodoCreate(BaseModel):
    info: str


class TodoUpdate(BaseModel):
    info: Optional[str] = None


class TodoSchema(BaseModel):
    id: int
    info: str
    status: int

    model_config = {"from_attributes": True}
