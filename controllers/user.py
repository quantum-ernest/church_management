from typing import List

from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

from core import NotFound, get_db_session
from models import UserMapper
from schemas import UserSchemaIn, UserSchemaOut, UserSchemaUpdate
from services import IsAuthenticated

user_router = APIRouter(
    prefix="/api/users",
    tags=["USER"],
)


@user_router.get("", response_model=List[UserSchemaOut], dependencies=[Security(IsAuthenticated())])
async def get_all(session: Session = Depends(get_db_session)):
    return UserMapper.get_all(session)


@user_router.get("/{id}", response_model=UserSchemaOut, dependencies=[Security(IsAuthenticated())])
async def get(id: int, session: Session = Depends(get_db_session)):
    NotFound(session, {UserMapper: [id]}).__call__()
    return UserMapper.get_by_id(session, id)


@user_router.post("", response_model=UserSchemaOut, dependencies=[Security(IsAuthenticated())])
async def post(data: UserSchemaIn, session: Session = Depends(get_db_session)):
    return UserMapper.create(session=session, data=data.model_dump())


@user_router.put("", response_model=List[UserSchemaOut], dependencies=[Security(IsAuthenticated())])
async def update(data: UserSchemaUpdate, session: Session = Depends(get_db_session)):
    NotFound(session, {UserMapper: [data.id]}).__call__()
    return UserMapper.update(session=session, data=data.model_dump())


@user_router.delete("/{id}", dependencies=[Security(IsAuthenticated())])
async def delete(id: int, session: Session = Depends(get_db_session)):
    NotFound(session, {UserMapper: [id]}).__call__()
    return UserMapper.delete(session, id)
