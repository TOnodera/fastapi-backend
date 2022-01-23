from operator import imod
from fastapi import UploadFile, File
import re

from src.config import settings


class UserFile:
    def regist(self, id: int, seq: int, file: UploadFile = File(...)) -> None:
        """ """
        match = re.search(r"(?<=\.)(?P<extension>[a-zA-Z]+)$", file.filename)
        extension = match["extension"].lower()
        file_name = f"USER_{id}_{seq}.{extension}"
        with open(settings.USER_FILES_DIR + file_name, "wb") as f:
            f.write(file.file.read())
