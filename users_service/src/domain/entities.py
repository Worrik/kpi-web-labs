from dataclasses import dataclass
from uuid import UUID
import datetime


@dataclass
class UserDM:
    id: UUID
    name: str
    email: str
    created_at: datetime.datetime
