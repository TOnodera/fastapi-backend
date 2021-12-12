from fastapi import APIRouter
from fastapi import status
from fastapi.responses import JSONResponse
from starlette.responses import Response

from src.exceptions.NoSuchObjectException import NoSuchObjectException
from src.exceptions.ValidationException import ValidationException
from src.schemas.User.UserOut import UserOut
from src.schemas.User.UserIn import UserIn
from src.schemas.User.UserUpdate import UserUpdate
from src.domain.User.User import User as UserDomain


router = APIRouter()


@router.post("/users/create")
def create(request: UserIn):
    try:
        user = UserDomain(
            name=request.name, email=request.email, password=request.password
        )
        id = user.create()
        return JSONResponse({"id": id}, status.HTTP_201_CREATED)
    except ValidationException as e:
        return JSONResponse(
            {"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST
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
