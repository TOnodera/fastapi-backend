class User:
    def __init__(
        self, *, name: str, email: str, id: int = None, password: str = None
    ) -> None:
        self.name = name
        self.email = email
        self.id = id
        self.password = password
