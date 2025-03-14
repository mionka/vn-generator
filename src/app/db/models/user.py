from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TEXT

from .base import BaseTable
from .mixins import TimestampMixin, UUIDMixin


class User(UUIDMixin, TimestampMixin, BaseTable):
    __tablename__ = "users"

    uid = Column(
        "uid",
        TEXT,
        nullable=False,
        unique=True,
        index=True,
        comment="User id in Firebase.",
    )
    email = Column(
        "email",
        TEXT,
        nullable=False,
        unique=True,
        index=True,
        comment="User email.",
    )
