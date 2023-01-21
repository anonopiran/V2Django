from contextlib import contextmanager
from typing import ContextManager
from uuid import UUID

import requests
from yarl import URL


class UserMan:
    PATH_ADD = "user"
    PATH_REMOVE = "user"

    def __init__(self, endpoint: URL):
        self.endpoint = URL(endpoint)

    @contextmanager
    def client(self) -> ContextManager[requests.Session]:
        with requests.Session() as sess_:
            yield sess_

    def user__add(self, uuid: UUID, email: str, level=0):
        data = {"uuid": str(uuid), "email": email, "level": level}
        with self.client() as cl_:
            res = cl_.post(self.endpoint / self.PATH_ADD, json=data)
        res.raise_for_status()

    def user__rm(self, email: str):
        data = {"email": email}
        with self.client() as cl_:
            res = cl_.delete(self.endpoint / self.PATH_REMOVE, json=data)
        res.raise_for_status()
