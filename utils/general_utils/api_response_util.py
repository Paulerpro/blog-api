from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import APIException

class APIResponseUtil:

    @staticmethod
    def success_response(code: int, message: str, data: dict):
        response = {"detail": message, "data": data}

        if code == 200:
            return Response(response, status=status.HTTP_200_OK)
        elif code == 201:
            return Response(response, status=status.HTTP_201_CREATED)
        elif code == 204:
            return Response(response, status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def error_response(code: int, message: str, data: dict):
        response = {"detail": message, "data": data}

        if code == 400:
            raise APIException(response, status.HTTP_400_BAD_REQUEST)
        elif code == 401:
            raise APIException(response, status.HTTP_401_UNAUTHORIZED)
        elif code == 404:
            raise APIException(response, status.HTTP_404_NOT_FOUND)
        elif code == 500:
            raise APIException(response, status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            raise APIException(response, code)
        