from datetime import datetime, timedelta
from pytz import timezone
import logging

def check_meeting_id(target_id, meeting_ids):
    if target_id in meeting_ids:
        return True
    else:
        return False

def check_meeting_time(meeting_time):
    try:
        now = datetime.now(tz=timezone('Asia/Seoul'))
        day_after_tomorrow_start = (now + timedelta(days=2)).replace(hour=0, minute=0, second=0, microsecond=0)
        if now <= meeting_time < day_after_tomorrow_start:
            return True
        return False
    except TypeError as e:
        if str(e) == "can't compare offset-naive and offset-aware datetimes":
            logging.error(f'시간 에러, 노션 DB 시간 수정 요망: {e}')
            return False