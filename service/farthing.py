from datetime import datetime
from entitiy import Notion

def farthing_calender_data(result):

    properties = result.get('properties', {})
    
    meeting = Notion(
        page_id=result.get('id'),
        status=properties.get("확정여부", {}).get("multi_select", [{}])[0].get("name"),
        time=datetime.fromisoformat(properties.get("날짜", {}).get("date", {}).get("start")),
        meeting_type=properties.get("종류", {}).get("multi_select", [{}])[0].get("name"),
        meeting_url=result.get('url'),
        name=properties.get("이름", {}).get("title", [{}])[0].get('text').get('content')
    )
        
    return meeting
