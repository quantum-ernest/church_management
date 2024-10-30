from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import (DeclarativeBase, Mapped, Session, declared_attr,
                            mapped_column)

from utils import camel_to_snake


class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(self):
        return camel_to_snake(self.__name__.replace("Mapper", ""))

    def __repr__(self):
        columns_names = [column.name for column in self.__table__.columns.keys()]
        return f"{self.__name__}({', '.join(columns_names)})"

    id: Mapped[int] = mapped_column(primary_key=True)

    @classmethod
    def get_all(cls, session: Session):
        return session.scalars(select(cls)).all()

    @classmethod
    def get_by_id(cls, session: Session, pk_id):
        return session.scalars(select(cls).where(cls.id == pk_id)).first()

    @classmethod
    def create(cls, session: Session, **kwargs):
        data = kwargs.get("data")
        create_stmt = session.scalars(insert(cls).returning(cls), data).first()
        session.commit()
        return create_stmt

    @classmethod
    def update(cls, session: Session, **kwargs):
        data = kwargs.get("data")
        update_stmt = session.scalars(update(cls).where(cls.id == data.get('id')).returning(cls), data).first()
        session.commit()
        return update_stmt

    @classmethod
    def delete(cls, session: Session, pk_id):
        session.execute(delete(cls).where(cls.id == pk_id))
        session.commit()
        return True

    @classmethod
    def check_if_id_exists(cls, session: Session, pk_id):
        return True if cls.get_by_id(session, pk_id) else False
