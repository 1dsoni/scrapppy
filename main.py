from typing import List

from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

import log_config  # noqa
from apis import ht
from apis import scrapper


def make_middleware() -> List[Middleware]:
    return [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"]
        )
    ]


def init_routers(app_: FastAPI) -> None:
    app_.include_router(scrapper.router)
    app_.include_router(ht.router)


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="Scrappppy",
        description="Scrappppy API",
        version="0.0.1",
        docs_url="/_docs",
        middleware=make_middleware()
    )

    init_routers(app_)
    return app_


app = create_app()
