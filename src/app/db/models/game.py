from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import TEXT, UUID
from sqlalchemy.orm import relationship

from sqlalchemy.orm import Mapped
from .base import BaseTable
from .user import User
from .mixins import TimestampMixin, UUIDMixin


class Game(UUIDMixin, TimestampMixin, BaseTable):
    __tablename__ = "games"

    title = Column(
        "title",
        TEXT,
        nullable=False,
        comment="Game title.",
    )
    description = Column(
        "description",
        TEXT,
        comment="Game description.",
    )
    cover_image = Column(
        "cover_image",
        TEXT,
        nullable=False,
        comment="Game cover image url.",
    )
    author_id = Column(
        "author_id",
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        comment="Author identifier.",
    )

    author: Mapped["User"] = relationship("User", viewonly=True)
