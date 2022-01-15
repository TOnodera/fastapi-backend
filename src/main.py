from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers.routers import router


def get_application() -> FastAPI:
    application = FastAPI()
    application.include_router(router)
    return application


app = get_application()

# CORS対応
origins = ["http://localhost:3000", "http://127.0.0.1:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
