from faststream.rabbit import RabbitBroker

from src.application import interfaces
from src.application.dto import ChangeImageDTO, CreateCommentDTO, CreateLikeDTO, CreatePostDTO
from src.domain.entities import PostDM
from src.exceptions.database_exceptions import IntegrityError


class CreatePostInteractor:
    def __init__(self, post_repo: interfaces.PostRepo, broker: RabbitBroker) -> None:
        self.post_repo = post_repo
        self.broker = broker

    async def __call__(self, dto: CreatePostDTO) -> PostDM:
        if dto.image_data:
            image_url_res = await self.broker.request(
                queue="image_processing.optimize_image",
                message={"data": dto.image_data},
                timeout=5,
            )
            image_url = await image_url_res.decode()
        else:
            image_url = None
        return await self.post_repo.create_post(
            user_id=dto.user_id,
            text=dto.text,
            image_url=str(image_url),
        )


class GetPostsInteractor:
    def __init__(self, post_repo: interfaces.PostRepo) -> None:
        self.post_repo = post_repo

    async def __call__(self) -> list[PostDM]:
        return await self.post_repo.get_posts()


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
