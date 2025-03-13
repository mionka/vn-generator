# pylint: disable=not-callable
from app.db import DeclarativeBase


class BaseTable(DeclarativeBase):
    __abstract__ = True

    def __repr__(self) -> str:
        columns = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        return f"<{self.__tablename__}: {', '.join(map(lambda x: f'{x[0]}={x[1]}', columns.items()))}>"
