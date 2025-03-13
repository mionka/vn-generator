# pylint: disable=not-callable
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.sql import func


class UUIDMixin:
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
        unique=True,
        comment="Unique index of element (type UUID)",
    )


class TimestampMixin:
    dt_created = Column(
        TIMESTAMP(timezone=True),
        server_default=func.current_timestamp(),
        nullable=False,
        comment="Date and time of create (type TIMESTAMP)",
    )
    dt_updated = Column(
        TIMESTAMP(timezone=True),
        server_default=func.current_timestamp(),
        nullable=False,
        comment="Date and time of last update (type TIMESTAMP)",
    )
