from flask import Blueprint, request, jsonify
from http import HTTPStatus
from schemas.request.event import EventModel
from dependencies.services import get_track_service
from dependencies.services import get_kafka_service
from flasgger import swag_from
from pathlib import Path


api_v1 = Blueprint("api_v1", __name__)


@api_v1.route("/track", methods=["POST"])
@swag_from(str(Path(__file__).resolve().parent.parent.parent / "docs/track_event.yml"))
def track_event():
    try:
        track_service = get_track_service()
        track_service.verify_token()
        collected_data = track_service.collect_info()

        # верифицируем результат
        EventModel(**collected_data)

        # Вызов сервиса (можно прокинуть kafka producer, если нужно)
        broker_service = get_kafka_service()
        broker_service.send(collected_data)

        return jsonify({"message": "Event tracked successfully"}), HTTPStatus.CREATED

    except ValueError as ve:
        return jsonify({"detail": str(ve)}), HTTPStatus.BAD_REQUEST
