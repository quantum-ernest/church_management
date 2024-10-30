from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr


class MemberSchemaIn(BaseModel):
    picture: Optional[str]
    fullname: Optional[str]
    phone: Optional[str]
    email: Optional[EmailStr]
    dob: Optional[date]
    occupation: Optional[str]
    emergency_contact_name: Optional[str]
    emergency_contact_phone: Optional[str]
    marital_status: Optional[str]
    address: Optional[str]
    number_of_children: Optional[int]
    department_id: Optional[int]

class MemberSchemaUpdate(MemberSchemaIn):
    id: int


class MemberSchemaOut(MemberSchemaIn):
    id: int
