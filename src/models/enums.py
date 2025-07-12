from enum import Enum


class ComplaintStatus(str, Enum):
    OPEN = "open"
    CLOSED = "closed"


class ComplaintSentiment(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    UNKNOWN = "unknown"


class ComplaintCategory(str, Enum):
    TECHNICAL = "technical"
    PAYMENT = "payment"
    OTHER = "other"
