import datetime
import jwt

from src.config import JWTConfig


def parse_jwt_token(token: str, jwt_config: JWTConfig) -> dict:
    try:
        payload = jwt.decode(
            token,
            jwt_config.secret_key,
            algorithms=[jwt_config.algorithm],
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")


class JWTTokenGenerator:
    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        expiration_delta: datetime.timedelta = datetime.timedelta(hours=1),
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expiration_delta = expiration_delta

    def generate_for_user(self, user_id: str) -> str:
        expiration = datetime.datetime.utcnow() + self.expiration_delta
        payload = {"sub": user_id, "exp": expiration}
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token


class JWTTokenValidator:
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def validate(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")
