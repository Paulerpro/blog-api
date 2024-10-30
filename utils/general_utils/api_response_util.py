from rest_framework import status
from rest_framework.response import Response

class APIResponseUtil:

    @staticmethod
    def success_response(code: int, message: str, data: dict):
        response = {"detail": message, "data": data}

        if code == "200":
            return Response(response, status=status.HTTP_200_OK)
        elif code == "201":
            return Response(response, status=status.HTTP_201_CREATED)
        if code == "204":
            return Response(response, status=status.HTTP_204_NO_CONTENT)
