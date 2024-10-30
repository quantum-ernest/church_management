from typing import List

from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

from core import NotFound, get_db_session
from models import DepartmentMapper
from schemas import (DepartmentSchemaIn, DepartmentSchemaOut,
                     DepartmentSchemaUpdate)
from services import IsAuthenticated

department_router = APIRouter(
    prefix="/api/departments",
    tags=["DEPARTMENT"],
)


@department_router.get("", response_model=List[DepartmentSchemaOut], dependencies=[Security(IsAuthenticated())])
async def get_all(session: Session = Depends(get_db_session)):
    return DepartmentMapper.get_all(session)


@department_router.get("/{id}", response_model=DepartmentSchemaOut, dependencies=[Security(IsAuthenticated())])
async def get(id: int, session: Session = Depends(get_db_session)):
    NotFound(session, {DepartmentMapper: [id]}).__call__()
    return DepartmentMapper.get_by_id(session, id)


@department_router.post("", response_model=List[DepartmentSchemaOut], dependencies=[Security(IsAuthenticated())])
async def post(data: DepartmentSchemaIn, session: Session = Depends(get_db_session)):
    return DepartmentMapper.create(session=session, data=data.model_dump())


@department_router.put("", response_model=List[DepartmentSchemaOut], dependencies=[Security(IsAuthenticated())])
async def update(data: DepartmentSchemaUpdate, session: Session = Depends(get_db_session)):
    NotFound(session, {DepartmentMapper: data.id}).__call__()
    return DepartmentMapper.update(session=session, data=data.model_dump())


@department_router.delete("/{id}", dependencies=[Security(IsAuthenticated())])
async def delete(id: int, session: Session = Depends(get_db_session)):
    NotFound(session, {DepartmentMapper: [id]}).__call__()
    return DepartmentMapper.delete(session, id)
