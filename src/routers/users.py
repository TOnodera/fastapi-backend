from fastapi import APIRouter
from src.schemas.User.User import User
from src.schemas.User.UserIn import UserIn
from fastapi import status

router = APIRouter()


@router.get("/users/{item_id}", response_model=User)
def read(item_id: int):
    return {"name": "test", "email": "test@email.com", "item_id": item_id}


@router.post("/users/create", response_model=User, status_code=status.HTTP_201_CREATED)
def post(user: UserIn):
    return user
