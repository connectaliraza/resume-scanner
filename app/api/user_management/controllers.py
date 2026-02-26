from fastapi import Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.base_components import BaseController, Endpoint, Response
from app.api.user_management.models import Token, User, UserCreate
from app.api.user_management.services import UserManagementService


# Dummy security functions for now
def create_access_token(data: dict):
    return "fake-token"


class UserManagementController(BaseController):
    def __init__(self, service: UserManagementService, api_version: str):
        self.service = service
        self.api_version = api_version

        endpoints = [
            Endpoint(
                rule="/register",
                func=self.register,
                methods=["POST"],
                response_type=User,
            ),
            Endpoint(
                rule="/login",
                func=self.login,
                methods=["POST"],
                response_type=Token,
            ),
        ]

        super().__init__(
            title="User Management",
            prefix=f"/{self.api_version}/users",
            endpoints=endpoints,
        )

    async def register(self, user: UserCreate) -> Response:
        return self.service.create_user(user.dict())

    async def login(self, form_data: OAuth2PasswordRequestForm = Depends()) -> Response:
        user = self.service.get_user_by_email(email=form_data.username)
        if not user or user["password"] != form_data.password:
            return Response(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="Incorrect username or password",
                error_code=1002,
            )

        access_token = create_access_token(data={"sub": user["email"]})
        return Response(
            message="Login successful",
            body={"access_token": access_token, "token_type": "bearer"},
        )
