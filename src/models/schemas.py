from typing import Optional

from pydantic import BaseModel

from .enums import (
    ComplaintStatus, ComplaintCategory, ComplaintSentiment
)


class ComplaintCreate(BaseModel):
    text: str


class ComplaintSentimentCreate(BaseModel):
    sentiment: ComplaintSentiment


class ComplaintCategoryCreate(BaseModel):
    category: ComplaintCategory


class ComplaintResponse(BaseModel):
    id: int
    status: ComplaintStatus
    sentiment: ComplaintSentiment
    category: ComplaintCategory

    class Config:
        from_attributes = True


class ComplaintUpdate(BaseModel):
    text: Optional[str]
    status: Optional[ComplaintStatus]
    sentiment: Optional[ComplaintSentiment]
    category: Optional[ComplaintCategory]
