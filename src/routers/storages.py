from fastapi import APIRouter
from fastapi import status
from fastapi.responses import FileResponse, JSONResponse
from src.config import settings
import os


router = APIRouter()


@router.get("/storages/{storage_name}/{file_name}")
def resourses(storage_name: str, file_name: str):
    path_file = f"{settings.FILES_DIR}/{storage_name}/{file_name}"
    if os.path.exists(path_file):
        return FileResponse(path_file)
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND)
