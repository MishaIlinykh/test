from flask import Flask
from redis import Redis
from flasgger import Swagger
from core.config import GeneralConfig
from core.config import SwaggerParam
from api.v1.events import api_v1 as events_router
from middleware.rate_limit import RateLimitMiddleware
from dependencies.cache import get_cache_storage
from api.v1.events import api_v1 as events_namespace
from pathlib import Path

config = GeneralConfig()
cache = get_cache_storage()


def create_app():

    app = Flask(
        __name__,
        static_url_path="/flasgger_static",
        static_folder=str(Path(__file__).resolve().parent.parent / "static/swagger"),
    )
    app.config.from_object(config)

    swagger = Swagger(
        app, template=SwaggerParam.swagger_template, config=SwaggerParam.swagger_config
    )

    # Подключаем middleware
    app.wsgi_app = RateLimitMiddleware(
        app.wsgi_app,
        cache=cache,
        limit=config.LIMIT_REQUESTS_ONE_IP,
        window_sec=config.WINDOW_SIZE_LIMIT_REQUESTS,
    )

    app.cache = cache
    # подключаем ручки
    app.register_blueprint(events_router, url_prefix="/api/v1/events")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9001, debug=False)
