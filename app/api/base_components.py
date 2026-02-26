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
    """
    This class is used to define an endpoint for a controller.

    It contains the rule, the function, the methods, the response type and
    the possible error codes. The response type is used to define the response
    body of the endpoint. The possible error codes are used to define the
    possible error codes that the endpoint can return. These all are mainly
    used in order to automatically generate the documentation for the
    controller but also as a check for your output.

    Providing a different response from this given response type will result
    in an error.
    """

    rule: str
    func: callable
    methods: List[str]
    response_type: Union[BaseModel, None] = None
    possible_error_codes: Union[List[int], None] = None


class BaseResponse(BaseModel):
    """
    This is the base response model for the entire API.

    It describes the structure of the response so that everyone knows what
    answer to expect.
    """

    message: str
    body: Union[dict, list]
    error_code: int


class Response(JSONResponse):
    def __init__(
        self,
        status_code: int = 200,
        message: str = "",
        body: dict = {},
        error_code: int = 0,
    ):
        # Use jsonable_encoder to convert Pydantic models/dataclasses
        content = jsonable_encoder(
            {"message": message, "body": body, "error_code": error_code}
        )

        super().__init__(
            status_code=status_code,
            content=content,
        )


class BaseController:
    """
    This is used as a base class for all of our controllers.

    You can simply use a list of Endpoint objects to create a controller.
    This class will automatically create a router and the corresponding
    documentation for the controller.

    Since this uses FastAPI in combination with Pydantic, you can use
    Pydantic models in order to define the request bodies of your endpoints.
    Doing this will also automatically perform data validation on the bodies
    of the requests.
    """

    def __init__(self, title: str, prefix: str, endpoints: List[Endpoint]) -> None:
        self.router: APIRouter = APIRouter(
            prefix="/api" + prefix,
            tags=[title.title()],
        )

        self._register_endpoints(endpoints)

    def _register_endpoints(self, endpoints: List[Endpoint]) -> None:
        for endpoint in endpoints:
            new_response_model = BaseResponse

            if endpoint.response_type:
                new_response_model = create_model(
                    f"{endpoint.response_type.__qualname__.capitalize()}Response",
                    message=(str, Field("")),
                    body=(endpoint.response_type, Field(None)),
                    error_code=(int, Field(0)),
                )

            responses = {
                200: {"model": new_response_model},
                400: {"model": BaseResponse},
                422: {"model": BaseResponse},
            }

            for error_code in endpoint.possible_error_codes or []:
                responses[error_code] = {"model": BaseResponse}

            self.router.add_api_route(
                endpoint.rule,
                endpoint.func,
                methods=endpoint.methods,
                response_model=new_response_model,
                responses=responses,
            )


class BaseAPI:
    """
    This class is mostly a wrapper around FastAPI.

    It is used to start the API and to register controllers to the API.
    It also allows you to define the IP and port of the API and whether
    you want to run the API in debug mode.

    If you run the API in debug mode, it will also allow CORS requests from
    all origins.
    """

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
        """
        Registers blueprints of app controllers to our api.
        """
        for controller in controllers:
            self.app.include_router(controller.router)

    def register_exception_handlers(
        self, handlers: List[tuple[type, Callable]]
    ) -> None:
        """
        Register custom exception handlers to the FastAPI app.

        Args:
            handlers: List of tuples (exception_type, handler_function)
        """
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

        # Use Config to ensure proper event loop handling
        config = uvicorn.Config(
            app=self.app,
            host=self.ip,
            port=self.port,
            loop="auto",  # Let uvicorn choose the best loop
        )
        server = uvicorn.Server(config)
        await server.serve()
