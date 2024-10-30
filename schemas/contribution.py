from datetime import date
from typing import List, Optional

from pydantic import BaseModel

from schemas import MemberSchemaOut, UserSchemaOut


class ContributionTypeSchemaIn(BaseModel):
    name: str


class ContributionTypeSchemaUpdate(BaseModel):
    id: int
    name: Optional[str] = None


class ContributionTypeSchemaOut(ContributionTypeSchemaIn):
    id: int


class ContributionSchemaIn(BaseModel):
    amount: float
    date: List[date]
    type_id: int
    member_id: int


class ContributionSchemaUpdate(BaseModel):
    id: int
    amount: Optional[float] = None
    date: Optional[date] = None
    type_id: Optional[int] = None
    member_id: Optional[int] = None
    user_id: Optional[int] = None


class ContributionSchemaOut(BaseModel):
    id: int
    amount: float
    date: date
    type: ContributionTypeSchemaOut
    member: MemberSchemaOut
    user: Optional[UserSchemaOut] = None
