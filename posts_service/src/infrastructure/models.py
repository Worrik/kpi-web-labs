from uuid import UUID, uuid4
import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship


Base = declarative_base()
metadata = Base.metadata


class PostModel(Base):
    __tablename__ = "posts"

    id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(sa.UUID, nullable=True)
    text: Mapped[str] = mapped_column(sa.Text, nullable=False)
    image_url: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        sa.DateTime, default=datetime.datetime.utcnow
    )

    comments: Mapped[list["CommentModel"]] = relationship(back_populates="post")
    likes: Mapped[list["LikeModel"]] = relationship(back_populates="post")


class CommentModel(Base):
    __tablename__ = "comments"

    id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True, default=uuid4)
    post_id: Mapped[UUID] = mapped_column(sa.UUID, sa.ForeignKey("posts.id"))
    user_id: Mapped[UUID] = mapped_column(sa.UUID, nullable=True)
    text: Mapped[str] = mapped_column(sa.Text, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        sa.DateTime, default=datetime.datetime.utcnow
    )

    post: Mapped[PostModel] = relationship("PostModel", back_populates="comments")


class LikeModel(Base):
    __tablename__ = "likes"
    __table_args__ = (sa.UniqueConstraint("post_id", "user_id"),)

    id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True, default=uuid4)
    post_id: Mapped[UUID] = mapped_column(sa.UUID, sa.ForeignKey("posts.id"))
    user_id: Mapped[UUID] = mapped_column(sa.UUID, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        sa.DateTime, default=datetime.datetime.utcnow
    )

    post: Mapped[PostModel] = relationship("PostModel", back_populates="likes")
