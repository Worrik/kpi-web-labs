from dataclasses import dataclass
from uuid import UUID
import datetime


@dataclass
class UserDM:
    id: UUID
    created_at: datetime.datetime
    name: str
    email: str
