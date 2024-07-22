import uuid

from apps.users.models import User


class UserService:
    def get_user_by_id(self, user_id: uuid.UUID):
        return User.objects.get(pk=user_id)
