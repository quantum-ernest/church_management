from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base


class DepartmentMapper(Base):
    name: Mapped[str] = mapped_column(unique=True)

    member: Mapped["MemberMapper"] = relationship(back_populates="department")
