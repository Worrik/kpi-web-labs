from faststream.rabbit import RabbitBroker
from uuid import UUID

from src.application import interfaces
from src.application.dto import ChangeImageDTO, CreateCommentDTO, CreateLikeDTO, CreatePostDTO
from src.domain.entities import PostDM, CommentDM, AuthorDM
from src.exceptions.database_exceptions import IntegrityError


class CreatePostInteractor:
    def __init__(self, post_repo: interfaces.PostRepo, broker: RabbitBroker) -> None:
        self.post_repo = post_repo
        self.broker = broker

    async def get_author(self, user_id: UUID) -> AuthorDM | None:
        res = await self.broker.request(
            queue="users.get_by_ids",
            message=[user_id],
            timeout=5,
        )
        if authors := await res.decode():
            return AuthorDM(**authors[0])

    async def __call__(self, dto: CreatePostDTO) -> PostDM:
        if dto.image_data:
            image_url_res = await self.broker.request(
                queue="image_processing.optimize_image",
                message={"data": dto.image_data},
                timeout=5,
            )
            res = await image_url_res.decode()
            image_url = str(res)
        else:
            image_url = None
        post = await self.post_repo.create_post(
            user_id=dto.user_id,
            text=dto.text,
            image_url=image_url,
        )
        post.author = await self.get_author(dto.user_id)
        post.comments_count = 0
        post.likes_count = 0
        return post

class GetPostsInteractor:
    def __init__(self, post_repo: interfaces.PostRepo, broker: RabbitBroker) -> None:
        self.post_repo = post_repo
        self.broker = broker

    async def __call__(self) -> list[PostDM]:
        posts = await self.post_repo.get_posts()
        user_ids = list({post.user_id for post in posts})
        users_response = await self.broker.request(
            queue="users.get_by_ids",
            message=user_ids,
            timeout=5,
        )
        users = await users_response.decode()
        users_map = {
            str(user["id"]): AuthorDM(
                id=user["id"],
                name=user["name"],
                email=user["email"],
                created_at=user["created_at"]
            )
            for user in users
        }
        for post in posts:
            post.author = users_map[str(post.user_id)]
        return posts


class CreateLikeInteractor:
    def __init__(self, like_repo: interfaces.LikeRepo) -> None:
        self.like_repo = like_repo

    async def __call__(self, dto: CreateLikeDTO) -> bool:
        try:
            await self.like_repo.create_like(
                post_id=dto.post_id,
                user_id=dto.user_id,
            )
        except IntegrityError:
            return False
        return True


class CreateCommentInteractor:
    def __init__(self, comment_repo: interfaces.CommentRepo) -> None:
        self.comment_repo = comment_repo

    async def __call__(self, dto: CreateCommentDTO) -> None:
        await self.comment_repo.create_comment(
            post_id=dto.post_id,
            user_id=dto.user_id,
            text=dto.text,
        )


class GetCommentsInteractor:
    def __init__(self, comment_repo: interfaces.CommentRepo, broker: RabbitBroker) -> None:
        self.comment_repo = comment_repo
        self.broker = broker

    async def __call__(self, post_id: UUID) -> list[CommentDM]:
        comments = await self.comment_repo.get_comments(post_id)
        user_ids = list({comment.user_id for comment in comments})
        users_response = await self.broker.request(
            queue="users.get_by_ids",
            message=user_ids,
            timeout=5,
        )
        users = await users_response.decode()
        users_map = {
            str(user["id"]): AuthorDM(
                id=user["id"],
                name=user["name"],
                email=user["email"],
                created_at=user["created_at"]
            )
            for user in users
        }
        for comment in comments:
            comment.author = users_map[str(comment.user_id)]
        return comments


class ChangeImageInteractor:
    def __init__(self, post_repo: interfaces.PostRepo) -> None:
        self.post_repo = post_repo

    async def __call__(self, dto: ChangeImageDTO) -> PostDM:
        post = await self.post_repo.get_post_by_id(dto.post_id)
        if post.user_id != dto.user_id:
            raise PermissionError
        return await self.post_repo.update_post_image(
            post_id=dto.post_id,
            image_url=dto.image_url,
        )
