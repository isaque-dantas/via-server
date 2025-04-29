from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.user import UserSerializer
from api.services.user import UserService


class UserViewSet(APIView):
    @staticmethod
    def post(request):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = UserService.create(serializer.validated_data)
        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def get(request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

