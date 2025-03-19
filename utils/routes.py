from collections.abc import Iterable
from dataclasses import dataclass
from typing import Tuple

from fastapi import APIRouter
from fastapi import FastAPI, Depends

from config import APP_SETTINGS


@dataclass
class Routes:
    routers: Tuple[APIRouter]

    def register_routes(self, app: FastAPI, prefix=APP_SETTINGS.API_V1_PREFIX):
        for router in self.routers:
            app.include_router(router, prefix=prefix)
