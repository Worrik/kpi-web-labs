from functools import lru_cache
from typing import Self

from pydantic import BaseModel
from environs import Env
import yaml


class JWTConfig(BaseModel):
    algorithm: str
    secret_key: str
    access_token_expire_minutes: int


class RabbitMQConfig(BaseModel):
    host: str
    port: int
    username: str
    password: str

    @property
    def url(self) -> str:
        return f"amqp://{self.username}:{self.password}@{self.host}:{self.port}/"


class Service(BaseModel):
    name: str
    url: str


class Config(BaseModel):
    jwt: JWTConfig
    rabbitmq: RabbitMQConfig
    services: list[Service]

    @classmethod
    def parse(cls) -> Self:
        env = Env()
        env.read_env()

        with open("services.yaml") as f:
            services = yaml.safe_load(f)

        services = [
            Service(name=service["name"], url=service["url"])
            for service in services["services"]
        ]

        jwt = JWTConfig(
            algorithm=env.str("JWT_ALGORITHM", "HS256"),
            secret_key=env.str("JWT_SECRET"),
            access_token_expire_minutes=env.int("JWT_EXPIRE_MINUTES", 60),
        )
        rabbitmq = RabbitMQConfig(
            host=env.str("RABBITMQ_HOST"),
            port=env.int("RABBITMQ_PORT"),
            username=env.str("RABBITMQ_USER"),
            password=env.str("RABBITMQ_PASS"),
        )
        return cls(services=services, jwt=jwt, rabbitmq=rabbitmq)
