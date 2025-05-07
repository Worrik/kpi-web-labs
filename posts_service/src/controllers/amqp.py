from dishka import FromDishka
from faststream.rabbit import RabbitRouter
from src.application.dto import ChangeImageDTO, CreateCommentDTO, CreateLikeDTO, CreatePostDTO
from src.application.interactors import (
    ChangeImageInteractor,
    CreateCommentInteractor,
    CreateLikeInteractor,
    CreatePostInteractor,
    GetPostsInteractor,
)

from src.controllers.schemas import (
    ChangeImageSchema,
    CreateCommentSchema,
    CreateLikeSchema,
    CreatePostSchema,
    PostSchema,
)


amqp_router = RabbitRouter()


@amqp_router.subscriber("posts.create")
async def create_post(
    data: CreatePostSchema,
    interactor: FromDishka[CreatePostInteractor],
) -> PostSchema:
    dto = CreatePostDTO(
        user_id=data.user_id,
        text=data.text,
        image_data=data.image_data,
    )
    post = await interactor(dto)
    return PostSchema(
        id=post.id,
        user_id=post.user_id,
        text=post.text,
        created_at=post.created_at,
        image_url=post.image_url,
        likes_count=post.likes_count,
        comments_count=post.comments_count,
    )


@amqp_router.subscriber("posts.get_all")
async def get_posts(interactor: FromDishka[GetPostsInteractor]) -> list[PostSchema]:
    posts = await interactor()
    return [
        PostSchema(
            id=post.id,
            user_id=post.user_id,
            text=post.text,
            created_at=post.created_at,
            image_url=post.image_url,
            likes_count=post.likes_count,
            comments_count=post.comments_count,
        )
        for post in posts
    ]


@amqp_router.subscriber("posts.like")
async def create_like(
    data: CreateLikeSchema,
    interactor: FromDishka[CreateLikeInteractor],
) -> bool:
    dto = CreateLikeDTO(
        post_id=data.post_id,
        user_id=data.user_id,
    )
    return await interactor(dto)


@amqp_router.subscriber("posts.comment")
async def create_comment(
    data: CreateCommentSchema,
    interactor: FromDishka[CreateCommentInteractor],
) -> None:
    dto = CreateCommentDTO(
        post_id=data.post_id,
        user_id=data.user_id,
        text=data.text,
    )
    await interactor(dto)


@amqp_router.subscriber("posts.change_image")
async def change_image(
    data: ChangeImageSchema,
    interactor: FromDishka[ChangeImageInteractor],
) -> PostSchema:
    dto = ChangeImageDTO(
        post_id=data.post_id,
        user_id=data.user_id,
        image_url=data.image_url,
    )
    post = await interactor(dto)
    return PostSchema(
        id=post.id,
        user_id=post.user_id,
        text=post.text,
        created_at=post.created_at,
        image_url=post.image_url,
        likes_count=post.likes_count,
        comments_count=post.comments_count,
    )
