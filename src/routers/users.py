from fastapi import APIRouter
from fastapi import status
from fastapi.responses import JSONResponse

from src.schemas.User.UserCreated import UserCreated
from src.schemas.User.UserOut import UserOut
from src.schemas.User.UserIn import UserIn
from src.domain.User.User import User as UserDomain

router = APIRouter()


@router.get("/users/{id}", response_model=UserOut)
def read(id: int):
    user = UserDomain.read(id)
    return {"name": user.name, "email": user.email, "id": user.id}


@router.post("/users/create", response_model=UserCreated)
def create(request: UserIn):
    user = UserDomain(name=request.name, email=request.email, password=request.password)
    id = user.create()
    return JSONResponse({"id": id}, status.HTTP_201_CREATED)
