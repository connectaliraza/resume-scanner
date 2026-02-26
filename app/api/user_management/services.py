from app.api.base_components import Response

_users_db = {}


class UserManagementService:
    def create_user(self, user: dict) -> Response:
        if user["email"] in _users_db:
            return Response(
                status_code=400,
                message="Email already registered",
                error_code=1001,
            )

        _users_db[user["email"]] = user
        return Response(
            message="User registered successfully",
            body=user,
        )

    def get_user_by_email(self, email: str) -> dict | None:
        return _users_db.get(email)
