from typing import Optional

from pydantic import BaseModel


class DepartmentSchemaIn(BaseModel):
    name: str

class DepartmentSchemaUpdate(BaseModel):
    id: int
    name: Optional[str] = None

class DepartmentSchemaOut(DepartmentSchemaIn):
    id: int
