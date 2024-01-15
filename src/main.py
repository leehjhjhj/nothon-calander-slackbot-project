from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from api.scrum_api import question_controller
from api import meeting_controller
app = FastAPI()


origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(question_controller.router)
app.include_router(meeting_controller.router)
