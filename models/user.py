from datetime import datetime
from enum import member
from typing import Optional

from pydantic import EmailStr
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship

from models import Base, MemberMapper


class UserMapper(Base):
    member_id: Mapped[Optional[int]] = mapped_column(ForeignKey("member.id", ondelete="SET NULL"))
    username: Mapped[str]
    password: Mapped[str]
    role: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    member: Mapped["MemberMapper"] = relationship(back_populates="user")
    contribution: Mapped["ContributionMapper"] = relationship(back_populates="user")
    __table_args__ = (UniqueConstraint("username", "member_id", name="unique_user_username_member_id"),)

    @classmethod
    def get_by_email(cls, email: EmailStr, db: Session):
        _member = MemberMapper.get_by_email(email, db)
        return db.query(cls).filter_by(member_id=_member.id).first()

    @classmethod
    def update_password(cls, id: int, password: str, session: Session):
        user = cls.get_by_id(session, id)
        user.password = password
        session.commit()
        session.refresh(user)
        return True

    @classmethod
    def validate_by_email(cls, email: EmailStr, db: Session):
        user = cls.get_by_email(email, db)
        return True if user else False
