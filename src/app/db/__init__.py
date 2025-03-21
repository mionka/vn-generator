from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base


convention = {
    "all_column_names": lambda constraint, table: "_".join(str(column.name) for column in constraint.columns.values()),
    "ix": "ix__%(table_name)s__%(all_column_names)s",
    "uq": "uq__%(table_name)s__%(all_column_names)s",
    "ck": "ck__%(table_name)s__%(constraint_name)s",
    "fk": ("fk__%(table_name)s__%(all_column_names)s__" "%(referred_table_name)s"),
    "pk": "pk__%(table_name)s",
}

metadata = MetaData(naming_convention=convention)
DeclarativeBase = declarative_base(metadata=metadata)

__all__ = [
    "DeclarativeBase",
]
