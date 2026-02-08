from ..base import Base
from datetime import datetime, timezone
import uuid
from sqlalchemy import String, Boolean, Float, DateTime, Enum as SQLEnum
from enum import Enum as PyEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

# hur ska jag implementera roller?


class UserEnum(str, PyEnum):
    admin = "admin"
    user = "user"


class BaseUser(Base):
    __tablename__ = "users"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[UserEnum] = mapped_column(
        SQLEnum(UserEnum, name="user_role_enum"),
        nullable=False,
        default=UserEnum.user
    )
    created: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    last_updated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),)
