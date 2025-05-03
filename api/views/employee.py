from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.employee import EmployeeSerializer
from api.services.employee import EmployeeService


class EmployeeViewSet(APIView):
    @staticmethod
    def post(request):
        serializer = EmployeeSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = EmployeeService.create(serializer.validated_data)
        serializer = EmployeeSerializer(user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def get(request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = EmployeeSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ExternalEmployeeViewSet(APIView):
    @staticmethod
    def get(request, email: str):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if not EmployeeService.email_exists(email):
            return Response(status=status.HTTP_404_NOT_FOUND)

        employee = EmployeeService.get_by_email(email)
        serializer = EmployeeSerializer(employee)

        return Response(serializer.data, status=status.HTTP_200_OK)
