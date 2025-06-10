import time
import json
from flask import request
from werkzeug.wrappers import Request as WSGIRequest


class RateLimitMiddleware:
    def __init__(self, app, cache, limit=100, window_sec=60):
        self.app = app
        self.cache = cache
        self.limit = limit
        self.window_sec = window_sec

    def __call__(self, environ, start_response):
        req = WSGIRequest(environ)
        ip = req.remote_addr or "unknown"
        now = int(time.time())
        window = now // self.window_sec
        key = f"requests_limit:{ip}:{window}"

        try:
            count = self.cache.incr(key)
            if count == 1:
                self.cache.expire(key, self.window_sec)
        except Exception:
            # Redis недоступен — пропускаем
            return self.app(environ, start_response)

        if count > self.limit:
            retry_after = self.window_sec - (now % self.window_sec)
            response_data = {"detail": "Too many requests"}
            response_body = json.dumps(response_data).encode("utf-8")
            headers = [
                ("Content-Type", "application/json"),
                ("Content-Length", str(len(response_body))),
                ("Retry-After", str(retry_after)),
                ("X-RateLimit-Limit", str(self.limit)),
                ("X-RateLimit-Remaining", "0"),
            ]
            start_response("429 TOO MANY REQUESTS", headers)
            return [response_body]

        remaining = self.limit - count

        def custom_start_response(status, headers, exc_info=None):
            headers.append(("X-RateLimit-Limit", str(self.limit)))
            headers.append(("X-RateLimit-Remaining", str(remaining)))
            return start_response(status, headers, exc_info)

        return self.app(environ, custom_start_response)
