from fastapi import APIRouter
from api.service.containers import MeetingContainer

router = APIRouter(
    prefix="/meeting",
)

@router.post("/redis", status_code=201)
def self_save_user_lists_to_redis():
    participants_process = MeetingContainer.participants_process()
    participants_process.save_user_lists_to_redis() 
    