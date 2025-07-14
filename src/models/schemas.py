from datetime import datetime
from typing import Optional

from pydantic import BaseModel, model_validator, ConfigDict

from .enums import (
    ComplaintStatus, ComplaintCategory, ComplaintSentiment
)


class ComplaintCreate(BaseModel):
    text: str
    sentiment: Optional[ComplaintSentiment] = ComplaintSentiment.UNKNOWN
    category: Optional[ComplaintCategory] = ComplaintCategory.OTHER


class ComplaintFilters(BaseModel):
    status: Optional[ComplaintStatus] = None
    category: Optional[ComplaintCategory] = None
    sentiment: Optional[ComplaintSentiment] = None
    timestamp: Optional[dict[str, datetime]] = None

    @model_validator(mode="before")
    def validate_timestamp(cls, values):
        if "timestamp" not in values or values["timestamp"] is None:
            return values

        timestamp = values["timestamp"]
        allowed_keys = {"start_date", "end_date"}

        if not set(timestamp.keys()).issubset(allowed_keys):
            raise ValueError(
                f"Timestamp must contain only of: {allowed_keys}"
            )

        if not all(key in timestamp for key in allowed_keys):
            raise ValueError(
                f"Timestamp must have both of: {allowed_keys}"
            )
        else:
            if timestamp["end_date"] < timestamp["start_date"]:
                raise ValueError(
                    "end_date must be >= start_date"
                )
        return values


class ComplaintResponse(BaseModel):
    id: int
    status: ComplaintStatus
    sentiment: ComplaintSentiment
    category: ComplaintCategory

    model_config = ConfigDict(from_attributes=True)


class ComplaintListResponse(BaseModel):
    id: int
    text: str
    status: ComplaintStatus
    sentiment: ComplaintSentiment
    category: ComplaintCategory

    model_config = ConfigDict(from_attributes=True)


class ComplaintUpdate(BaseModel):
    id: int
    text: Optional[str] = None
    status: Optional[ComplaintStatus] = None
    sentiment: Optional[ComplaintSentiment] = None
    category: Optional[ComplaintCategory] = None
