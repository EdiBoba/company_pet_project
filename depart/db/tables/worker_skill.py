import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from ..base import Base


class WorkerSkill(Base):
    __tablename__ = "worker_skills"

    worker_id = sa.Column(
        UUID(as_uuid=True),
        ForeignKey("workers.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    skill_id = sa.Column(
        UUID(as_uuid=True),
        ForeignKey("skills.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    created_at = sa.Column(sa.DateTime, nullable=False, server_default=sa.func.now())
