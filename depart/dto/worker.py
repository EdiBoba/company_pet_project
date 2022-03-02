from uuid import UUID

from .position import Position
from .base import BaseModel


class Worker(BaseModel):
    id: UUID
    surname: str
    name: str
    position: Position
