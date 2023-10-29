from entity.notion import NotionPage
from .farthing_patifipants import make_participants


def add_participants(meeting: NotionPage, result) -> NotionPage:
    participants = make_participants(result, meeting.notion_database_id)

    meeting.participants = participants if participants else None
    return meeting