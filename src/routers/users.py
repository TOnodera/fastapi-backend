from fastapi import APIRouter
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi import File, UploadFile
from starlette.responses import Response
from typing import List
from src.exceptions.FileRegistException import FileRegistException

from src.exceptions.NoSuchObjectException import NoSuchObjectException
from src.exceptions.ValidationException import ValidationException
from src.schemas.User.UserOut import UserOut
from src.schemas.User.UserIn import UserIn
from src.schemas.User.UserUpdate import UserUpdate
from src.domain.User.User import User as UserDomain
from src.config import settings

router = APIRouter()


@router.post("/users/create")
def create(request: UserIn) -> JSONResponse:
    """
    ユーザー新規作成API

    Params
    -----
    request: UserIn
    files: List[UploadFile]

    Returns
    -----
    JSONResponse
    """
    try:
        user = UserDomain(
            name=request.name, email=request.email, password=request.password
        )
        # ユーザー新規作成
        id = user.create()

        return JSONResponse({"id": id}, status.HTTP_201_CREATED)
    except ValidationException as e:
        return JSONResponse(
            {"message": str(e)}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
    except FileRegistException as e:
        return JSONResponse(
            {"message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        return JSONResponse(
            {"message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.get("/users")
def all(offset: int = 0, limit: int = 10):
    try:
        users = UserDomain.all(offset, limit)
        response = []
        for user in users:
            response.append(
                {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "created_at": str(user.created_at),
                    "updated_at": str(user.updated_at),
                }
            )
        return JSONResponse(response, status_code=status.HTTP_200_OK)
    except Exception as e:
        return JSONResponse(
            {"message": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.get("/users/{id}", response_model=UserOut)
def read(id: int):
    try:
        user = UserDomain.read(id)
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }

    except NoSuchObjectException as e:
        return JSONResponse(
            {"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST
        )


@router.put("/users/{id}")
def update(id: int, request: UserUpdate):
    try:
        user = UserDomain.read(id)
        user.update(name=request.name, email=request.email, password=request.password)
        return JSONResponse({"id": user.id, "name": user.name, "email": user.email})
    except NoSuchObjectException as e:
        return JSONResponse(
            {"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST
        )


@router.delete("/users/{id}")
def delete(id: int):
    try:
        user = UserDomain.read(id)
        user.delete()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except NoSuchObjectException as e:
        return JSONResponse(
            {"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST
        )


@router.post("/users/{id}/{seq}/upload-file")
def upload_file(id: int, seq: int, file: UploadFile = File(...)):
    try:
        user = UserDomain.read(id)
        user.regist_file(id, seq, file)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return JSONResponse(
            {"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST
        )
