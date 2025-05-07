from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Depends

from src.schemas.posts import CreateCommentSchema, CreatePostSchema, PostSchema
from src.dependencies.jwt_auth import get_user_id
from src.utils.broker_provider import BrokerProvider


router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/")
@inject
async def get_posts(
    broker_provider: FromDishka[BrokerProvider],
) -> list[PostSchema]:
    """
    Get all posts
    """
    result = await broker_provider.rpc(
        queue="posts.get_all",
        payload={},
    )
    return [PostSchema(**post) for post in result]


@router.post("/")
@inject
async def create_post(
    post: CreatePostSchema,
    broker_provider: FromDishka[BrokerProvider],
    user_id: str = Depends(get_user_id),
) -> PostSchema:
    """
    Create a new post
    """
    result = await broker_provider.rpc(
        queue="posts.create",
        payload={
            "user_id": user_id,
            "text": post.text,
            "image_url": post.image_url,
        },
    )
    return PostSchema(**result)


@router.post("/{post_id}/like", status_code=201)
@inject
async def like_post(
    post_id: str,
    broker_provider: FromDishka[BrokerProvider],
    user_id: str = Depends(get_user_id),
) -> bool:
    """
    Like a post
    """
    result = await broker_provider.rpc(
        queue="posts.like",
        payload={
            "user_id": user_id,
            "post_id": post_id,
        },
    )
    return result


@router.post("/{post_id}/comment", status_code=201)
@inject
async def comment_post(
    post_id: str,
    data: CreateCommentSchema,
    broker_provider: FromDishka[BrokerProvider],
    user_id: str = Depends(get_user_id),
) -> bool:
    """
    Comment on a post
    """
    await broker_provider.rpc(
        queue="posts.comment",
        payload={
            "user_id": user_id,
            "post_id": post_id,
            "text": data.text,
        },
    )
    return True
