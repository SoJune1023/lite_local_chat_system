import uvicorn

from fastapi import FastAPI
from dotenv import load_dotenv

from src.routers.interaction import router as interaction_router

app = FastAPI(title="ollama-chat")
app.include_router(interaction_router)

def main() -> None:
    load_dotenv()

    uvicorn.run(
        "src.__main__:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )

if __name__ == "__main__":
    main()