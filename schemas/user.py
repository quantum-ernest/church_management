from typing import Optional

from pydantic import BaseModel

from schemas import MemberSchemaOut


class UserSchemaIn(BaseModel):
    member_id: int
    username: str
    password: str
    role: str


class UserSchemaUpdate(BaseModel):
    id: int
    role: Optional[str] = None
    username: Optional[str] = None


class UserSchemaOut(BaseModel):
    id: int
    username: str
    role: str
    member: MemberSchemaOut
