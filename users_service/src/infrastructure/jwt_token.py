import datetime
import jwt

from src.application.interfaces import JWTTokenGenerator
from src.domain.entities import UserDM


class JWTTokenGeneratorImpl(JWTTokenGenerator):
    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        expiration_delta: datetime.timedelta = datetime.timedelta(hours=1),
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expiration_delta = expiration_delta

    def generate_for_user(self, user: UserDM) -> str:
        expiration = datetime.datetime.utcnow() + self.expiration_delta
        payload = {"sub": str(user.id), "exp": expiration}
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token
