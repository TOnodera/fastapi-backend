from datetime import datetime
from typing import Optional
from src.schemas.User.User import User


class UserOut(User):
    id: int
    name: Optional[str]
    email: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
