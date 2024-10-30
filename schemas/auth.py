from pydantic import BaseModel, EmailStr

from schemas import UserSchemaOut


class LoginSchemaIn(BaseModel):
    email: EmailStr
    password: str


class LoginSchemaOut(BaseModel):
    token: str
    user: UserSchemaOut


class OtpEmailLoginSchemaIn(BaseModel):
    email: EmailStr
    otp: str


class OtpEmailGenerateSchemaIn(BaseModel):
    email: EmailStr


class OtpGenerateSchemaOut(BaseModel):
    message: str


class ChangePasswordSchemaIn(BaseModel):
    new_password: str


class ChangePasswordSchemaOut(BaseModel):
    message: str
