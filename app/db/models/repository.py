from datetime import datetime

from sqlalchemy import DateTime, String,Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base


class Repository(Base):

    __tablename__ = "repositories"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    url: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
        unique=True,
    )

    status: Mapped[str]= mapped_column(
        String(30),
        nullable=False,
        default="PENDING"
    )

    indexed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    chunks = relationship(
        "VectorChunk",
        back_populates="repository",
        cascade="all, delete-orphan",
    )