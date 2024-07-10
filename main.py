import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from domain.answer import answer_router
from domain.question import question_router
from domain.user import user_router

app = FastAPI()

origins = [
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8080",  # React
    "http://localhost:8080",  # React
    "http://192.168.0.139",
]

internal = [f"http://192.168.0.{i}" for i in range(1, 256)]
origins += internal

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(question_router.router)
app.include_router(answer_router.router)
app.include_router(user_router.router)
app.mount("/assets", StaticFiles(directory="frontend/dist/assets"))

@app.get("/")
def index():
    return FileResponse("frontend/dist/index.html")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)