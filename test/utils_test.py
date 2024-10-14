from datetime import datetime, timezone

from truthbrush.utils import as_datetime


def test_as_datetime():
    """Test that a valid date string is correctly converted to a datetime object in UTC."""
    recent = "2024-07-14 14:50:31.628257+00:00"
    result = as_datetime(recent)

    expected = datetime(2024, 7, 14, 14, 50, 31, 628257, tzinfo=timezone.utc)
    assert result == expected
