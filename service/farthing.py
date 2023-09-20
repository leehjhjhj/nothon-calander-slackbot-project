from datetime import datetime
from entity import Notion, StatusChoice

def farthing_calender_data(result):

    properties = result.get('properties', {})

    status_str = properties.get("확정여부", {}).get("multi_select", [{}])[0].get("name")
    status_enum = StatusChoice(status_str) if status_str else None

    meeting = Notion(
        page_id=result.get('id'),
        status=status_enum,
        time=datetime.fromisoformat(properties.get("날짜", {}).get("date", {}).get("start")),
        meeting_type=properties.get("종류", {}).get("multi_select", [{}])[0].get("name"),
        meeting_url=result.get('url'),
        name=properties.get("이름", {}).get("title", [{}])[0].get('text').get('content')
    )
        
    return meeting
