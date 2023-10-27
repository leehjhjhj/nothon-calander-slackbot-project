from datetime import datetime, timedelta
from pytz import timezone

def check_meeting_id(target_id, meeting_ids):
    if target_id in meeting_ids:
        return True
    else:
        return False

def check_meeting_time(meeting_time):
    now = datetime.now(tz=timezone('Asia/Seoul'))
    day_after_tomorrow_start = (now + timedelta(days=2)).replace(hour=0, minute=0, second=0, microsecond=0)
    if now <= meeting_time < day_after_tomorrow_start:
        return True

    return False

