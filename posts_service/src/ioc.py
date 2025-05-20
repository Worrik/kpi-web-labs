from typing import AsyncIterable
from dishka import AnyOf, Provider, Scope, from_context, provide
from faststream.rabbit import RabbitBroker
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.application.interactors import (
    ChangeImageInteractor,
    CreateCommentInteractor,
    CreateLikeInteractor,
    CreatePostInteractor,
    GetPostsInteractor,
    GetCommentsInteractor,
)

from src.application.interfaces import CommentRepo, DBSession, LikeRepo, PostRepo
from src.config import Config
from src.infrastructure.database import new_session_maker
from src.infrastructure.repositories import CommentRepoImpl, LikeRepoImpl, PostRepoImpl


class AppProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)
    broker = from_context(provides=RabbitBroker, scope=Scope.APP)

    post_repo = provide(PostRepoImpl, scope=Scope.REQUEST, provides=PostRepo)
    comment_repo = provide(CommentRepoImpl, scope=Scope.REQUEST, provides=CommentRepo)
    like_repo = provide(LikeRepoImpl, scope=Scope.REQUEST, provides=LikeRepo)

    create_post_interactor = provide(CreatePostInteractor, scope=Scope.REQUEST)
    get_posts_interactor = provide(GetPostsInteractor, scope=Scope.REQUEST)
    create_like_interactor = provide(CreateLikeInteractor, scope=Scope.REQUEST)
    create_comment_interactor = provide(CreateCommentInteractor, scope=Scope.REQUEST)
    change_image_interactor = provide(ChangeImageInteractor, scope=Scope.REQUEST)
    get_comments_interactor = provide(GetCommentsInteractor, scope=Scope.REQUEST)

    @provide(scope=Scope.APP)
    def get_session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config.postgres)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AnyOf[AsyncSession, DBSession]]:
        async with session_maker() as session:
            yield session
