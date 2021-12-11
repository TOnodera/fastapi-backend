from fastapi import APIRouter
from fastapi import status
from fastapi.responses import JSONResponse

from src.schemas.User.UserOut import UserOut
from src.schemas.User.UserIn import UserIn
from src.schemas.User.UserUpdate import UserUpdate
from src.domain.User.User import User as UserDomain

router = APIRouter()


@router.get("/users/{id}", response_model=UserOut)
def read(id: int):
    user = UserDomain.read(id)
    return {"id": user.id, "name": user.name, "email": user.email}


@router.post("/users/create")
def create(request: UserIn):
    user = UserDomain(name=request.name, email=request.email, password=request.password)
    id = user.create()
    return JSONResponse({"id": id}, status.HTTP_201_CREATED)


@router.put("/users/{id}")
def update(id: int, request: UserUpdate):
    user = UserDomain.read(id)
    user.update(name=request.name, email=request.email, password=request.password)
    return JSONResponse({"id": user.id, "name": user.name, "email": user.email})
