from datetime import timezone, datetime


def get_datetime_now() -> datetime:
    return datetime.now(timezone.utc)