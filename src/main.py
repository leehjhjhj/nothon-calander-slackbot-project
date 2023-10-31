from fastapi import FastAPI
from src.api.service.redis_user_lists import save_user_lists_to_redis
app = FastAPI()


@app.get("/")
async def save_user_lists_to_redis():
    pass