from pydantic import BaseModel, Field

class ScrumRequestDto(BaseModel):
    notion_api_key: str = Field(..., example="your_notion_api_key")
    notion_database_id: str = Field(..., example="your_database_id")
    name: str = Field(..., example="정기 스크럼")
    day: str = Field(..., example="금요일")
    time: str = Field(..., example="18:00")
    type: str = Field(..., example="비대면")