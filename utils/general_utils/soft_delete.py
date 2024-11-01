from utils.general_utils.api_response_util import APIResponseUtil

def delete_instance(instance):
    if instance.status != "DELETED":
        instance.status = "DELETED"
        instance.save()
        return APIResponseUtil.success_response(200, "Deleted Successfully")
    return APIResponseUtil.error_response(208, "Post Already deleted")