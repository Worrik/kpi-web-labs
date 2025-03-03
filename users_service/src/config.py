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


class PostgresConfig(BaseModel):
    host: str = Field(alias="POSTGRES_HOST")
    port: int = Field(alias="POSTGRES_PORT")
    login: str = Field(alias="POSTGRES_USER")
    password: str = Field(alias="POSTGRES_PASSWORD")
    database: str = Field(alias="POSTGRES_DB")

    @classmethod
    def from_env(cls) -> Self:
        env = Env()
        env.read_env()
        return cls(
            POSTGRES_HOST=env("POSTGRES_HOST"),
            POSTGRES_PORT=env.int("POSTGRES_PORT"),
            POSTGRES_USER=env("POSTGRES_USER"),
            POSTGRES_PASSWORD=env("POSTGRES_PASSWORD"),
            POSTGRES_DB=env("POSTGRES_DB"),
        )


class JWTConfig(BaseModel):
    secret_key: str = Field(alias="JWT_SECRET_KEY")
    algorithm: str = Field(alias="JWT_ALGORITHM", default="HS256")
    expiration_delta: int = Field(alias="JWT_EXPIRATION_DELTA", default=3600)

    @classmethod
    def from_env(cls) -> Self:
        env = Env()
        env.read_env()
        return cls(
            JWT_SECRET_KEY=env("JWT_SECRET_KEY"),
            JWT_ALGORITHM=env("JWT_ALGORITHM", default="HS256"),
            JWT_EXPIRATION_DELTA=env.int("JWT_EXPIRATION_DELTA", default=3600),
        )


class Config(BaseModel):
    rabbitmq: RabbitMQConfig = Field()
    postgres: PostgresConfig = Field()
    jwt: JWTConfig = Field()

    @classmethod
    def from_env(cls) -> Self:
        return cls(
            rabbitmq=RabbitMQConfig.from_env(),
            postgres=PostgresConfig.from_env(),
            jwt=JWTConfig.from_env(),
        )
