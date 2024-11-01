from apps.user.models import User

from utils.general_utils.api_response_util import APIResponseUtil

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
    
    @staticmethod
    def follower_following_logic(follower, following, action):
        if action:
            follower.following.add(following)
            following.followers.add(follower)

            follower.save()
            following.save()
            return APIResponseUtil.success_response(204, "User followed successfully", {})
        else:
            follower.following.remove(following)
            following.followers.remove(follower)

        follower.save()
        following.save()

        return APIResponseUtil.success_response(204, "User unfollowed successfully", {})