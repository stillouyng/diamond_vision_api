import pytest

from src.models.enums import (
    ComplaintStatus, ComplaintSentiment, ComplaintCategory
)

@pytest.fixture
def valid_complaint_data():
    return {
        "text": "What's wrong with the pay button?",
        "sentiment": ComplaintSentiment.POSITIVE,
        "category": ComplaintCategory.TECHNICAL
    }
