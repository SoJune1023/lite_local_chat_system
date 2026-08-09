import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from src.routers.interaction import router as interaction_router

app = FastAPI(title="ollama-chat")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(interaction_router)

app.mount("/static", StaticFiles(directory="static"), name="static")

def main() -> None:
    load_dotenv()

    uvicorn.run(
        "src.__main__:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=["src"]
    )

if __name__ == "__main__":
    main()