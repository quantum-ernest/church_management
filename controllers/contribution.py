from typing import List

from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

from core import NotFound, get_db_session
from models import (ContributionMapper, ContributionTypeMapper, MemberMapper,
                    UserMapper)
from schemas import (ContributionSchemaIn, ContributionSchemaOut,
                     ContributionSchemaUpdate, ContributionTypeSchemaIn,
                     ContributionTypeSchemaOut, ContributionTypeSchemaUpdate)
from services import IsAuthenticated

contribution_router = APIRouter(
    prefix="/api/contributions",
    tags=["CONTRIBUTION"],
)


@contribution_router.get("/types", response_model=List[ContributionTypeSchemaOut], dependencies=[Security(IsAuthenticated())])
async def get_all_type(session: Session = Depends(get_db_session)):
    return ContributionTypeMapper.get_all(session)


@contribution_router.get("/types/{id}", response_model=ContributionTypeSchemaOut, dependencies=[Security(IsAuthenticated())])
async def get_type(id: int, session: Session = Depends(get_db_session)):
    NotFound(session, {ContributionTypeMapper: [id]}).__call__()
    return ContributionTypeMapper.get_by_id(session, id)


@contribution_router.post("/types", response_model=ContributionTypeSchemaOut, dependencies=[Security(IsAuthenticated())])
async def post_type(data: ContributionTypeSchemaIn, session: Session = Depends(get_db_session)):
    return ContributionTypeMapper.create(session=session, data=data.model_dump())


@contribution_router.put("/types", response_model=ContributionTypeSchemaOut, dependencies=[Security(IsAuthenticated())])
async def update_type(data: ContributionTypeSchemaUpdate, session: Session = Depends(get_db_session)):
    NotFound(session, {ContributionTypeMapper: [data.id]}).__call__()
    return ContributionTypeMapper.update(session=session, data=data.model_dump())


@contribution_router.delete("/types/{id}", dependencies=[Security(IsAuthenticated())])
async def delete_type(id: int, session: Session = Depends(get_db_session)):
    NotFound(session, {ContributionTypeMapper: id}).__call__()
    return ContributionTypeMapper.delete(session, id)



@contribution_router.get("", response_model=List[ContributionSchemaOut], dependencies=[Security(IsAuthenticated())])
async def get_all(session: Session = Depends(get_db_session)):
    return ContributionMapper.get_all(session)


@contribution_router.get("/{id}", response_model=ContributionSchemaOut, dependencies=[Security(IsAuthenticated())])
async def get(id: int, session: Session = Depends(get_db_session)):
    NotFound(session, {ContributionMapper: [id]}).__call__()
    return ContributionMapper.get_by_id(session, id)


@contribution_router.get("/members/{member_id}", response_model=List[ContributionSchemaOut], dependencies=[Security(IsAuthenticated())])
async def get_user_(member_id: int, session: Session = Depends(get_db_session)):
    return ContributionMapper.get_by_user_id(session, member_id)


@contribution_router.get("/reports/{year}", dependencies=[Security(IsAuthenticated())])
async def get_by_year(year: str, type_id: int, session: Session = Depends(get_db_session)):
    return ContributionMapper.get_by_year(session, year, type_id)


@contribution_router.post("", response_model=ContributionSchemaOut, dependencies=[Security(IsAuthenticated())])
async def post(
        data: ContributionSchemaIn,
        user: dict = Depends(IsAuthenticated()),
        session: Session = Depends(get_db_session)
):
    model_data = []
    NotFound(session, {UserMapper: [user.get('user_id')], MemberMapper: [data.member_id]}).__call__()
    for date in data.date:
        model_data.append({
            "amount": data.amount,
            "date": date,
            "type_id": data.type_id,
            "member_id": data.member_id,
            "user_id": user.get('user_id'),
        })
    return ContributionMapper.create(session=session, data=model_data)


@contribution_router.put("", response_model=ContributionSchemaOut, dependencies=[Security(IsAuthenticated())])
async def update(data: ContributionSchemaUpdate, session: Session = Depends(get_db_session)):
    NotFound(session, {ContributionMapper: [data.id]}).__call__()
    return ContributionMapper.update(session=session, data=data)


@contribution_router.delete("/{id}", dependencies=[Security(IsAuthenticated())])
async def delete(id: int, session: Session = Depends(get_db_session)):
    NotFound(session, {ContributionMapper: [id]}).__call__()
    return ContributionMapper.delete(session, id)
