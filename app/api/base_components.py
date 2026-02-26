from dataclasses import dataclass
from typing import Callable, List, Union

import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, create_model


@dataclass
class Endpoint:
    rule: str
    func: callable
    methods: List[str]
    response_type: Union[BaseModel, None] = None
    possible_error_codes: Union[List[int], None] = None


class BaseResponse(BaseModel):
    message: str
    body: Union[dict, list, None] = None
    error_code: int = 0


class Response(JSONResponse):
    def __init__(
        self,
        status_code: int = 200,
        message: str = "",
        body: Union[dict, list, None] = None,
        error_code: int = 0,
    ):
        content = {
            "message": message,
            "body": jsonable_encoder(body),
            "error_code": error_code,
        }
        super().__init__(
            status_code=status_code,
            content=content,
        )


class BaseController:
    def __init__(self, title: str, prefix: str, endpoints: List[Endpoint]) -> None:
        self.router: APIRouter = APIRouter(
            prefix="/api" + prefix,
            tags=[title.title()],
        )
        self._register_endpoints(endpoints)

    def _register_endpoints(self, endpoints: List[Endpoint]) -> None:
        for endpoint in endpoints:
            response_model = create_model(
                f"{endpoint.func.__name__.capitalize()}Response",
                __base__=BaseResponse,
                body=(endpoint.response_type, Field(None)),
            )

            self.router.add_api_route(
                endpoint.rule,
                endpoint.func,
                methods=endpoint.methods,
                response_model=response_model,
            )


class BaseAPI:
    def __init__(
        self,
        ip: str,
        port: int,
        debug: bool,
        title: str,
        description: str,
        version: str,
        summary: str,
    ) -> None:
        self.ip = ip
        self.port = port
        self.debug = debug
        self.app = FastAPI(
            title=title, description=description, version=version, summary=summary
        )

    def register_controllers(self, controllers: List[BaseController]) -> None:
        for controller in controllers:
            self.app.include_router(controller.router)

    def register_exception_handlers(
        self, handlers: List[tuple[type, Callable]]
    ) -> None:
        for exception_type, handler in handlers:
            self.app.add_exception_handler(exception_type, handler)

    async def start(self) -> None:
        if self.debug:
            origins = ["*"]
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=origins,
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

        config = uvicorn.Config(
            app=self.app,
            host=self.ip,
            port=self.port,
            loop="auto",
        )
        server = uvicorn.Server(config)
        await server.serve()
