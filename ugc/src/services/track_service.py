from uuid import UUID, uuid4
from datetime import datetime, timezone
from db.storages.cache_storage import CacheStorage
from services.base import BaseTokenService
from core.config import GeneralConfig
from typing import Any
from flask import request
from werkzeug.exceptions import Unauthorized, BadRequest
import json

settings = GeneralConfig()


class TrackService(BaseTokenService):
    def __init__(self, cache: CacheStorage):
        super().__init__(cache=cache)

    def get_token_from_header(self) -> str:
        """
        Получение токена из заголовка Authorization.
        """
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise Unauthorized(description="Missing or invalid Authorization header")

        token = auth_header.split(" ", 1)[1]
        if not token:
            raise Unauthorized(description="Authorization token is empty")

        return token

    def verify_token(self) -> None:
        token = self.get_token_from_header()
        self.payload = self.get_token_payload(token)
        if self.payload is None:
            raise BadRequest(description="Error in payload content")

    def get_params(self) -> None:
        try:
            self.event_type = request.args.get("event_type")
            self.content_raw = request.args.get("content")

        except:
            raise BadRequest(description="Error in args")

    def collect_info(self) -> dict[str, Any]:
        self.get_params()
        self.collected_data = {"content": {}}
        if not self.content_raw is None:
            try:
                self.collected_data["content"] = json.loads(self.content_raw)
            except:
                raise BadRequest(description="json format error")

        self.collected_data["user_id"] = self.payload["user_id"]
        self.collected_data["event_type"] = self.event_type
        self.collected_data["timestamp"] = datetime.now()
        return self.collected_data
