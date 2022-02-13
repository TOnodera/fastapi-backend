from datetime import datetime
from typing import List, Optional
from src.schemas.User.User import User


class UserOut(User):
    id: int
    username: Optional[str]
    email: Optional[str]
    paths: Optional[List[dict]]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
