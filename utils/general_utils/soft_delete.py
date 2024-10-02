from rest_framework.response import Response

def delete_instance(instance):
    if instance.status != "DELETED":
        instance.status = "DELETED"
        instance.save()
        return Response({"Deleted Successfully"}, 200)
    return Response({"Post Already deleted"}, 404)