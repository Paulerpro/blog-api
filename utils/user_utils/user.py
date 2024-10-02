from apps.user.models import User

class UserUtils:

    @staticmethod
    def get_user_login_data(user: User, token: dict):

        data = {
            "user": {
                "id": user.id,
                "uuid": user.unique_id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "folowers_count": user.followers.count(),
                "following_count": user.following.count()
            }
        }

        data.update(token)

        return data