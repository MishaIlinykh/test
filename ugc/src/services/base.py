from datetime import datetime, timezone
from typing import Any
from uuid import UUID
import jwt
from db.storages.cache_storage import CacheStorage
from core.config import GeneralConfig
from werkzeug.exceptions import Unauthorized

settings = GeneralConfig()


class BaseTokenService:
    def __init__(self, cache: CacheStorage):
        self.cache = cache

    def get_token_payload(self, token: str) -> dict[str, Any]:
        try:
            payload = jwt.decode(
                token, settings.AUTHJWT_SECRET_KEY, algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            raise Unauthorized("Token has expired")
        except jwt.InvalidTokenError as e:
            raise Unauthorized(f"Invalid token: {str(e)}")

        required_fields = {
            "user_id",
            "session_id",
            "service_name",
            "created_at",
            "expires_at",
            "token_type",
        }
        if not required_fields.issubset(payload):
            raise Unauthorized("Token payload is incomplete")

        # Дополнительная проверка для access-токенов
        if payload.get("token_type") == "access":
            token_created_at = datetime.fromtimestamp(
                payload["created_at"], tz=timezone.utc
            )
            redis_key = f"{payload['user_id']}:{payload['session_id']}"
            redis_data = self.cache.get(redis_key)

            if redis_data:
                redis_issued_at = datetime.fromisoformat(redis_data)
                if token_created_at != redis_issued_at:
                    raise Unauthorized("Token has been revoked")

        return payload
