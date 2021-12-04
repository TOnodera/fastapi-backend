from src.repository.DBConnection import DBConnection
from src.repository.User.User import User as UserRepository
from src.domain.User.User import User as UserDomain
import pytest


def test_UserRepository():
    userRepository = UserRepository()
    user = UserDomain("takeshi", "takeshi@mail.com", "password")
    userRepository.insert(user)
