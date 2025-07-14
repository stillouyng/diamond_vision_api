import pytest
from datetime import datetime
from pydantic import ValidationError

from src.models.schemas import (
    ComplaintCreate, ComplaintUpdate, ComplaintFilters,
    ComplaintResponse, ComplaintListResponse,
)

from src.models.enums import (
    ComplaintStatus, ComplaintCategory, ComplaintSentiment,
)



def test_complaint_create_valid(valid_complaint_data):
    """All fields are correct."""
    complaint = ComplaintCreate(**valid_complaint_data)
    assert complaint.text == "What's wrong with the pay button?"
    assert complaint.sentiment == ComplaintSentiment.POSITIVE
    assert complaint.category == ComplaintCategory.TECHNICAL


def test_complaint_create_defaults():
    """All fields are default-valued."""
    complaint = ComplaintCreate(text="Жалоба")
    assert complaint.sentiment == ComplaintSentiment.UNKNOWN
    assert complaint.category == ComplaintCategory.OTHER


def test_complaint_create_invalid():
    """Incorrect inputs."""
    with pytest.raises(ValidationError):
        ComplaintCreate(text=None)

    with pytest.raises(ValidationError):
        ComplaintCreate(text="A", sentiment="INVALID_SENTIMENT")


def test_complaint_filters_valid():
    """All fields are correct."""
    filters = ComplaintFilters(
        status=ComplaintStatus.OPEN,
        category=ComplaintCategory.TECHNICAL,
        sentiment=ComplaintSentiment.POSITIVE,
        timestamp={
            "start_date": datetime(2023, 1, 1),
            "end_date": datetime(2023, 12, 31)
        },
    )
    assert filters.status == ComplaintStatus.OPEN


def test_complaint_filters_defaults():
    """All fields are optional."""
    filters = ComplaintFilters()
    assert filters.status is None
    assert filters.timestamp is None


def test_complaint_filters_invalid_timestamp():
    """Incorrect timestamp format"""
    with pytest.raises(ValidationError):
        ComplaintFilters(timestamp={"invalid_key": datetime.now()})


def test_valid_timestamp():
    """Correct timestamp keys."""
    filters = ComplaintFilters(
        timestamp={
            "start_date": datetime(2023, 1, 1),
            "end_date": datetime(2023, 12, 31),
        }
    )
    assert filters.timestamp is not None

def test_invalid_timestamp_keys():
    """Incorrect keys."""
    with pytest.raises(ValueError):
        ComplaintFilters(
            timestamp={"from": datetime.now(), "to": datetime.now()}
        )


def test_partial_timestamp():
    """Only start_date"""
    with pytest.raises(ValidationError):
        ComplaintFilters(timestamp={"start_date": datetime.now()})


def test_complaint_response_valid():
    """Response is valid."""
    response = ComplaintResponse(
        id=1,
        status=ComplaintStatus.CLOSED,
        sentiment=ComplaintSentiment.POSITIVE,
        category=ComplaintCategory.TECHNICAL,
    )
    assert response.id == 1

def test_complaint_list_response_valid():
    """List Response is valid."""
    response = ComplaintListResponse(
        id=1,
        text="Everything is good, thanks!",
        status=ComplaintStatus.CLOSED,
        sentiment=ComplaintSentiment.NEGATIVE,
        category=ComplaintCategory.PAYMENT,
    )
    assert ComplaintCategory.PAYMENT == response.category


def test_complaint_update_valid():
    """Update valid test"""
    update = ComplaintUpdate(id=1)
    assert update.text is None

    update = ComplaintUpdate(
        id=1,
        text="Text was updated!",
        status=ComplaintStatus.OPEN,
    )
    assert update.status == ComplaintStatus.OPEN


def test_complaint_update_invalid():
    """No ID provided."""
    with pytest.raises(ValidationError):
        ComplaintUpdate(text="There is no ID!")
