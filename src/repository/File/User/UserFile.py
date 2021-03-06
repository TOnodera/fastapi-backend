from typing import List
from black import os
from fastapi import UploadFile, File
import re
from glob import glob
from src.config import settings


class UserFile:
    def __init__(self, id: int) -> None:
        self.prefix = "USER"
        self.storage_name = "users"
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

    def path(self, seq: int) -> str:
        """
        特定のファイルを取得する。

        Params
        -----
        seq: int

        Returns
        -----
        path: str
        """
        # USER_数字_数字.拡張子に一致するリストを作成する
        file_paths = [
            path
            for path in glob(f"{settings.USER_FILES_DIR}/**")
            if re.search(f"/{self.prefix}_{self.id}_{seq}\.(png|jpg|gif)", path)
        ]
        file_name = file_paths[0].split("/")[-1]
        return {"storage_name": self.storage_name, "file_name": file_name}

    def paths(self) -> List[dict]:
        """
        ユーザーに紐づくファイルをすべて取得する

        Returns
        -----
        paths: List[dict]
        """
        # USER_数字_数字.拡張子に一致するリストを作成する
        file_paths = [
            path
            for path in glob(f"{settings.USER_FILES_DIR}/**")
            if re.search(f"/{self.prefix}_{self.id}_\d+\.(png|jpg|gif)", path)
        ]
        results = []
        for path in file_paths:
            file_name = path.split("/")[-1]
            results.append({"storage_name": self.storage_name, "file_name": file_name})
        return results

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
