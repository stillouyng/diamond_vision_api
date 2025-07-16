from datetime import datetime

from sqlalchemy import (
    Integer, String, DateTime,
    func, Enum as SaEnum
)
from sqlalchemy.orm import (
    Mapped, mapped_column
)

from src.core.database import Base

from .enums import (
    ComplaintStatus, ComplaintSentiment, ComplaintCategory
)


class Complaint(Base):
    __tablename__ = "complaint"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    text: Mapped[str] = mapped_column(
        String(500), nullable=False
    )
    status: Mapped[ComplaintStatus] = mapped_column(
        SaEnum(ComplaintStatus), default=ComplaintStatus.OPEN
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, default=func.now()
    )
    sentiment: Mapped[ComplaintSentiment] = mapped_column(
        SaEnum(ComplaintSentiment), nullable=True
    )
    category: Mapped[ComplaintCategory] = mapped_column(
        SaEnum(ComplaintCategory), default=ComplaintCategory.OTHER
    )
