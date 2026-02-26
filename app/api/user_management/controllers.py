from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.base_components import BaseController, Endpoint
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

    async def register(self, user: UserCreate):
        db_user = self.service.get_user_by_email(email=user.email)
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        # In a real app, you would hash the password
        created_user = self.service.create_user(user.dict())
        return created_user

    async def login(self, form_data: OAuth2PasswordRequestForm = Depends()):
        user = self.service.get_user_by_email(email=form_data.username)
        if not user or user["password"] != form_data.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(data={"sub": user["email"]})
        return {"access_token": access_token, "token_type": "bearer"}
