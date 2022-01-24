from typing import List
from black import os
from fastapi import UploadFile, File
import re
from glob import glob
from src.config import settings


class UserFile:
    def __init__(self, id: int) -> None:
        self.prefix = "USER"
        self.id = id

    def regist(self, seq: int, file: UploadFile = File(...)) -> None:
        """
        ユーザーファイルを保存する。

        Params
        -----
        seq: int
            シーケンス番号
        file: UploadFile

        Returns
        -----
        None
        """
        match = re.search(r"(?<=\.)(?P<extension>[a-zA-Z]+)$", file.filename)
        extension = match["extension"].lower()
        file_name = f"{self.prefix}_{self.id}_{seq}.{extension}"
        with open(settings.USER_FILES_DIR + file_name, "wb") as f:
            f.write(file.file.read())

    def read(self, seq: int) -> str:
        """
        特定のファイルを取得する。

        Params
        -----
        seq: int

        Returns
        -----
        path: str
        """
        pass

    def reads(self) -> List[str]:
        """
        ユーザーに紐づくファイルをすべて取得する

        Returns
        -----
        paths: List[str]
        """
        pass

    def deletes(self) -> None:
        """
        ユーザーファイルの削除
        """
        # USER_数字_数字.拡張子に一致するリストを作成する
        file_paths = [
            path
            for path in glob(f"{settings.USER_FILES_DIR}/**")
            if re.search(f"/{self.prefix}_{self.id}_\d+\.(png|jpg|gif)", path)
        ]
        # ファイル削除
        for file_path in file_paths:
            os.remove(file_path)

    def delete(self, seq: int) -> None:
        """
        特定のデータを削除

        Params
        -----
        seq: int
        """
        # USER_数字_数字.拡張子に一致するリストを作成する
        file_paths = [
            path
            for path in glob(f"{settings.USER_FILES_DIR}/**")
            if re.search(f"/{self.prefix}_{self.id}_{seq}\.(png|jpg|gif)", path)
        ]

        # ファイル削除
        for file_path in file_paths:
            os.remove(file_path)
