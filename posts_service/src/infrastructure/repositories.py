from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
import sqlalchemy as sa

from src.application.interfaces import CommentRepo, LikeRepo, PostRepo
from src.domain.entities import CommentDM, LikeDM, PostDM
from src.exceptions.database_exceptions import IntegrityError
from src.infrastructure.models import CommentModel, LikeModel, PostModel


class PostRepoImpl(PostRepo):
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    def model_to_entity(
        self,
        post: PostModel,
        likes_count: int | None = None,
        comments_count: int | None = None,
    ) -> PostDM:
        return PostDM(
            id=post.id,
            user_id=post.user_id,
            text=post.text,
            image_url=post.image_url,
            created_at=post.created_at,
            likes_count=likes_count,
            comments_count=comments_count,
        )

    async def create_post(
        self,
        user_id: UUID,
        text: str,
        image_url: str | None,
    ) -> PostDM:
        post = PostModel(
            user_id=user_id,
            text=text,
            image_url=image_url,
        )
        self.db_session.add(post)
        try:
            await self.db_session.commit()
        except sa.exc.IntegrityError:
            await self.db_session.rollback()
            raise IntegrityError
        return self.model_to_entity(post)

    async def get_posts(self) -> list[PostDM]:
        comment_cnt_sq = (
            sa.select(
                CommentModel.post_id,
                sa.func.count(CommentModel.id).label("comments_count"),
            )
            .group_by(CommentModel.post_id)
            .subquery()
        )
        like_cnt_sq = (
            sa.select(
                LikeModel.post_id,
                sa.func.count(LikeModel.id).label("likes_count"),
            )
            .group_by(LikeModel.post_id)
            .subquery()
        )
        query = (
            sa.select(
                PostModel,
                sa.func.coalesce(comment_cnt_sq.c.comments_count, 0).label(
                    "comments_count"
                ),
                sa.func.coalesce(like_cnt_sq.c.likes_count, 0).label("likes_count"),
            )
            .outerjoin(comment_cnt_sq, comment_cnt_sq.c.post_id == PostModel.id)
            .outerjoin(like_cnt_sq, like_cnt_sq.c.post_id == PostModel.id)
        )
        result = await self.db_session.execute(query)
        posts = result.all()
        return [
            self.model_to_entity(post, likes, comments)
            for post, comments, likes in posts
        ]

    async def get_post_by_id(self, post_id: UUID) -> PostDM | None:
        query = sa.select(PostModel).where(PostModel.id == post_id)
        result = await self.db_session.execute(query)
        post = result.scalar_one_or_none()
        return self.model_to_entity(post) if post else None

    async def update_post_image(self, post_id: UUID, image_url: str) -> PostDM:
        post = await self.get_post_by_id(post_id)
        if not post:
            raise ValueError("Post not found")
        query = (
            sa.update(PostModel)
            .where(PostModel.id == post_id)
            .values(image_url=image_url)
        )
        await self.db_session.execute(query)
        await self.db_session.commit()
        post.image_url = image_url
        return post


class CommentRepoImpl(CommentRepo):
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    def model_to_entity(self, comment: CommentModel) -> CommentDM:
        return CommentDM(
            id=comment.id,
            post_id=comment.post_id,
            user_id=comment.user_id,
            text=comment.text,
            created_at=comment.created_at,
        )

    async def create_comment(
        self,
        post_id: UUID,
        user_id: UUID,
        text: str,
    ) -> CommentDM:
        comment = CommentModel(
            post_id=post_id,
            user_id=user_id,
            text=text,
        )
        self.db_session.add(comment)
        try:
            await self.db_session.commit()
        except sa.exc.IntegrityError:
            await self.db_session.rollback()
            raise IntegrityError
        return self.model_to_entity(comment)


class LikeRepoImpl(LikeRepo):
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    def model_to_entity(self, like: LikeModel) -> LikeDM:
        return LikeDM(
            id=like.id,
            post_id=like.post_id,
            user_id=like.user_id,
            created_at=like.created_at,
        )

    async def create_like(self, post_id: UUID, user_id: UUID) -> LikeDM:
        like = LikeModel(
            post_id=post_id,
            user_id=user_id,
        )
        self.db_session.add(like)
        try:
            await self.db_session.commit()
        except sa.exc.IntegrityError:
            await self.db_session.rollback()
            raise IntegrityError
        return self.model_to_entity(like)
