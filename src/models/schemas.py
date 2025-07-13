from datetime import datetime
from typing import Optional

from pydantic import BaseModel

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


class ComplaintResponse(BaseModel):
    id: int
    status: ComplaintStatus
    sentiment: ComplaintSentiment
    category: ComplaintCategory

    class Config:
        from_attributes = True


class ComplaintListResponse(BaseModel):
    id: int
    text: str
    status: ComplaintStatus
    sentiment: ComplaintSentiment
    category: ComplaintCategory

    class Config:
        from_attributes = True


class ComplaintUpdate(BaseModel):
    text: Optional[str] = None
    status: Optional[ComplaintStatus] = None
    sentiment: Optional[ComplaintSentiment] = None
    category: Optional[ComplaintCategory] = None
