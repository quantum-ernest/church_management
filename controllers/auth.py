from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core import get_db_session
from models import MemberMapper, UserMapper
from schemas import (ChangePasswordSchemaIn, ChangePasswordSchemaOut,
                     LoginSchemaIn, LoginSchemaOut, OtpEmailGenerateSchemaIn,
                     OtpEmailLoginSchemaIn, OtpGenerateSchemaOut)
from services import AuthService, IsAuthenticated

auth_router = APIRouter(prefix="/api/auth", tags=["AUTH"])


@auth_router.post("/email/login", response_model=LoginSchemaOut)
async def login(credential: LoginSchemaIn, db: Session = Depends(get_db_session)):
    val_user = MemberMapper.validate_by_email(credential.email, db)
    if val_user is False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {credential.email} not found",
        )
    user = UserMapper.get_by_email(credential.email, db)
    if AuthService.verify_password(credential.password, user.password) is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )
    return AuthService.get_access_token(user)


@auth_router.post("/otp/email/login", response_model=LoginSchemaOut)
async def login_otp_email(
    credential: OtpEmailLoginSchemaIn, db: Session = Depends(get_db_session)
):
    val_user = MemberMapper.validate_by_email(credential.email, db)
    if val_user is False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {credential.email} not found",
        )
    user = MemberMapper.get_by_email(credential.email, db)
    return AuthService.otp_login_via_email(credential, user)


@auth_router.post("/otp/email/generate", response_model=OtpGenerateSchemaOut)
async def generate_otp_email(
    credential: OtpEmailGenerateSchemaIn, db: Session = Depends(get_db_session)
):
    user = MemberMapper.validate_by_email(credential.email, db)
    if user is False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {credential.email} not found",
        )
    return await AuthService.generate_otp_via_email(credential.email)


@auth_router.post("/password/change", response_model=ChangePasswordSchemaOut)
def change_password(
    credential: ChangePasswordSchemaIn,
    db: Session = Depends(get_db_session),
    authenticated_user: dict = Depends(IsAuthenticated()),
):
    user = UserMapper.get_by_id(authenticated_user.get("user_id"), db)

    new_hashed_password = AuthService.hash_password(credential.new_password)
    UserMapper.update_password(user.id, new_hashed_password, db)
    return {"message": "Password changed successfully"}
