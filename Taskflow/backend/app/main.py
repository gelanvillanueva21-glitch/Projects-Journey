

from fastapi import FastAPI


app = FastAPI(title="Taskflow API")



@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "message": "TaskFlow backend is running"
    }


