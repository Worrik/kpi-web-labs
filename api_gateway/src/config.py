from functools import lru_cache
from typing import Self
from pydantic import BaseModel

import yaml


class Service(BaseModel):
    name: str
    url: str


class Config(BaseModel):
    services: list[Service]


    @classmethod
    def parse(cls) -> Self:
        with open("services.yaml") as f:
            services = yaml.safe_load(f)

        services = [Service(name=service["name"], url=service["url"]) for service in services["services"]]
        return cls(services=services)


@lru_cache
def get_config() -> Config:
    return Config.parse()
