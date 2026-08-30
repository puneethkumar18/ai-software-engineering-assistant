from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector

from app.db.models.base import Base


class VectorChunk(Base):

    __tablename__ = "knowledge_chunks"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    repository_id: Mapped[int] = mapped_column(
        ForeignKey(
            "repositories.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    source: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    document_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    language: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    chunk_index: Mapped[int] = mapped_column(
        nullable=False,
    )

    start_line: Mapped[int | None] = mapped_column(
        nullable=True,
    )

    end_line: Mapped[int | None] = mapped_column(
        nullable=True,
    )

    embedding: Mapped[list[float]] = mapped_column(
        Vector(3072),
        nullable=False,
    )

    repository = relationship(
        "Repository",
        back_populates="chunks",
    )