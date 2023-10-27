from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def scan_calendar():
    pass