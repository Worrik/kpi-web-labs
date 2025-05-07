from uuid import UUID, uuid4
import datetime

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


metadata = sa.MetaData()


class Base(DeclarativeBase):
    metadata = metadata
