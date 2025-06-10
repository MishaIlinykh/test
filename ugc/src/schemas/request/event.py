from pydantic import BaseModel, Field
from typing import Dict, Any
from uuid import UUID
from datetime import datetime
from enum import Enum


class EventType(str, Enum):
    CLICK = "click"
    CHANGE_VIEW_RESOLUTION = "change_view_resolution"
    VIDEO_TIMING = "video_timing"
    SCROLL = "scroll"
    HOVER = "hover"


class EventModel(BaseModel):
    user_id: UUID = Field(..., description="UUID пользователя")
    event_type: EventType = Field(..., description="Тип события")
    timestamp: datetime = Field(..., description="Время события")
    content: Dict[str, Any] = Field(
        default_factory=dict, description="Дополнительные метаданные"
    )
