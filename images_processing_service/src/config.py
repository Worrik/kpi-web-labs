from typing import Self

from environs import Env
from pydantic import BaseModel, Field


class RabbitMQConfig(BaseModel):
    host: str = Field(alias="RABBITMQ_HOST")
    port: int = Field(alias="RABBITMQ_PORT")
    login: str = Field(alias="RABBITMQ_USER")
    password: str = Field(alias="RABBITMQ_PASS")

    @classmethod
    def from_env(cls) -> Self:
        env = Env()
        env.read_env()
        return cls(
            RABBITMQ_HOST=env("RABBITMQ_HOST"),
            RABBITMQ_PORT=env.int("RABBITMQ_PORT"),
            RABBITMQ_USER=env("RABBITMQ_USER"),
            RABBITMQ_PASS=env("RABBITMQ_PASS"),
        )


class StaticFilesConfig(BaseModel):
    static_dir: str = Field(alias="STATIC_DIR")
    static_route: str = Field(alias="STATIC_ROUTE", default="/static")

    @classmethod
    def from_env(cls) -> Self:
        env = Env()
        env.read_env()
        return cls(
            STATIC_DIR=env.str("STATIC_DIR"),
            STATIC_ROUTE=env.str("STATIC_ROUTE", default="/static"),
        )


class Config(BaseModel):
    rabbitmq: RabbitMQConfig = Field()
    static_files: StaticFilesConfig = Field()

    @classmethod
    def from_env(cls) -> Self:
        return cls(
            rabbitmq=RabbitMQConfig.from_env(),
            static_files=StaticFilesConfig.from_env(),
        )
