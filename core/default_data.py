from sqlalchemy.dialects.postgresql import insert

from core import SessionLocal, envConfig
from models import MemberMapper, UserMapper
from services import AuthService


def set_default_data():
    with SessionLocal() as session:
        admin_member = session.scalars(
            insert(MemberMapper)
            .values(fullname="admin", email=envConfig.ADMIN_DEFAULT_EMAIL)
            .returning(MemberMapper)
            .on_conflict_do_update(
                constraint="unique_member_email_fullname",
                set_=dict(fullname="admin", email=envConfig.ADMIN_DEFAULT_EMAIL),
            )
        ).first()
        session.scalars(
            insert(UserMapper)
            .values(member_id=admin_member.id, username=envConfig.ADMIN_DEFAULT_USERNAME, role='admin',
                    password=AuthService.hash_password(envConfig.ADMIN_DEFAULT_PASSWORD))
            .on_conflict_do_update(
                constraint="unique_user_username_member_id",
                set_=dict(member_id=admin_member.id, username=envConfig.ADMIN_DEFAULT_USERNAME, role='admin',
                          password=AuthService.hash_password(envConfig.ADMIN_DEFAULT_PASSWORD)),
            )
        ).first()
        session.commit()
    return True
