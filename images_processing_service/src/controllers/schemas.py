from pydantic import BaseModel


class OptimizeImageSchema(BaseModel):
    data: str
