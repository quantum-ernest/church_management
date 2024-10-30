from collections import defaultdict
from datetime import date

from sqlalchemy import ForeignKey, String, cast, select
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship
from typing_extensions import Optional

from models import Base


class ContributionMapper(Base):
    amount: Mapped[float]
    date: Mapped[date]
    type_id: Mapped[Optional[int]] = mapped_column(ForeignKey("contribution_type.id", ondelete="SET NULL"))
    member_id: Mapped[Optional[int]] = mapped_column(ForeignKey("member.id", ondelete="SET NULL"))
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id", ondelete="SET NULL"))

    type: Mapped["ContributionTypeMapper"] = relationship(back_populates="contribution", passive_deletes="all")
    member: Mapped["MemberMapper"] = relationship(back_populates="contribution", passive_deletes="all")
    user: Mapped["UserMapper"] = relationship(back_populates="contribution", passive_deletes="all")

    @classmethod
    def get_by_year(cls, session: Session, year: str, type_id):
        contributions = session.scalars(
            select(cls).where(cls.type_id == type_id, cast(cls.date, String).ilike(f"%{year}%"))).all()
        monthly_total = defaultdict(int)
        for contribution in contributions:
            month = contribution.date.month
            monthly_total[month] += contribution.amount
        return monthly_total

    @classmethod
    def get_by_user_id(cls, session: Session, member_id: int):
        return session.scalars(select(cls).where(cls.member_id == member_id)).all()


class ContributionTypeMapper(Base):
    name: Mapped[str]

    contribution: Mapped["ContributionMapper"] = relationship(back_populates="type")
