_users_db = {}


class UserManagementService:
    def create_user(self, user: dict) -> dict:
        _users_db[user["email"]] = user
        return user

    def get_user_by_email(self, email: str) -> dict | None:
        return _users_db.get(email)
