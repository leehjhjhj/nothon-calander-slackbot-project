from fastapi import APIRouter
from .scrum_process import ScrumProcess
from .scrum_dto import ScrumRequestDto
from .containers import ScrumContainer

router = APIRouter(
    prefix="/scrum",
)

@router.post("/create", status_code=201)
async def create_scrum(request_data: ScrumRequestDto):
    scrum_process = ScrumContainer.scrum_process()
    response = await scrum_process.create_scrum_in_notion(request_data)
    return response