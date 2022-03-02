import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..base import Base


class Worker(Base):
    __tablename__ = "workers"

    id = sa.Column(UUID(as_uuid=True), primary_key=True, server_default=sa.func.uuid_generate_v1())
    surname = sa.Column(sa.String, nullable=False)
    name = sa.Column(sa.String, nullable=False)
    department_id = sa.Column(
        UUID(as_uuid=True),
        ForeignKey("departments.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    position_id = sa.Column(
        UUID(as_uuid=True),
        ForeignKey("positions.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    birth_date = sa.Column(sa.DateTime, nullable=False)
    created_at = sa.Column(sa.DateTime, nullable=False, server_default=sa.func.now())
    updated_at = sa.Column(sa.DateTime, nullable=False, server_default=sa.func.now())

    department = relationship("Department", back_populates="workers")
    position = relationship("Position")
    skills = relationship("Skill", secondary="worker_skills", back_populates="workers")

    def __repr__(self):
        return f"<Worker id={self.id}>"
