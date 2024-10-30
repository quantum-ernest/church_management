import redis
from fastapi import HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from core import envConfig
from schemas import OtpEmailLoginSchemaIn
from services import MailService
from utils import generate_otp, login_otp_template

_redis = redis.Redis(
    host=envConfig.REDIS_URL, port=envConfig.REDIS_PORT, decode_responses=True
)
mail_service = MailService()


class AuthService:
    pwd_context = CryptContext(schemes=["sha256_crypt"])

    @classmethod
    def hash_password(cls, password: str) -> str:
        return cls.pwd_context.hash(password)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def create_access_token(cls, data: dict) -> str:
        encoded_jwt = jwt.encode(
            data.copy(), envConfig.AUTH_SECRETE_KEY, algorithm=envConfig.AUTH_ALGORITHM
        )
        return encoded_jwt

    @classmethod
    def get_access_token(cls, user) -> dict:
        token = cls.create_access_token(
            data={
                "user_id": user.id,
                "role": user.role,
            }
        )
        return {"token": token, "user": user}

    @classmethod
    def decode_token(cls, token: str):
        try:
            return jwt.decode(
                token, envConfig.AUTH_SECRETE_KEY, algorithms=[envConfig.AUTH_ALGORITHM]
            )
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid Token: {e}"
            )

    @classmethod
    def otp_login_via_email(cls, credential: OtpEmailLoginSchemaIn, user) -> dict:
        verified_otp = cls.verity_email_otp(credential)
        if verified_otp:
            return cls.get_access_token(user)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect Verification Code",
            )

    @classmethod
    async def generate_otp_via_email(cls, email: EmailStr) -> dict:
        await cls.send_otp_via_email(email)
        return {"message": "OTP sent successfully"}

    @classmethod
    async def send_otp_via_email(cls, email: EmailStr) -> bool:
        otp = generate_otp()
        _redis.setex(name=email, value=otp, time=300)
        mail_massage = login_otp_template.replace("{{otp}}", otp).replace(
            "{{email}}", email
        )
        await mail_service.send_mail(email, mail_massage)
        return True

    @classmethod
    def verity_email_otp(cls, credential: OtpEmailLoginSchemaIn) -> bool:
        if _redis.get(name=credential.email) == credential.otp:
            return True
        return False


class UserAuthenticated(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(UserAuthenticated, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        token: HTTPAuthorizationCredentials = await super(
            UserAuthenticated, self
        ).__call__(request)
        if token:
            return AuthService.decode_token(token.credentials)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Token"
            )


class IsAuthenticated(UserAuthenticated):
    async def __call__(self, request: Request):
        user: dict = await UserAuthenticated.__call__(self, request)
        return user
