from pydantic import BaseModel, Field

class ScrumRequestDto(BaseModel):
    db_name: str = Field(..., example="your_notion_api_key")
    name: str = Field(..., example="정기 스크럼")
    day: str = Field(..., example="금요일")
    time: str = Field(..., example="18:00")
    type: str = Field(..., example="비대면")
    blocks: list[dict]