import hashlib
from src.repository.User.User import User as UserRepository
from src.domain.User.User import User as UserDomain


def test_UserRepository():
    name = "takeshi"
    email = "takeshi@mail.com"
    password = "password"
    userRepository = UserRepository()
    user = UserDomain(name, email, password)
    registered_user = userRepository.insert(user)

    assert registered_user.name == user.name
    assert registered_user.email == user.email
    assert (
        registered_user.password == hashlib.sha512(user.password.encode()).hexdigest()
    )
