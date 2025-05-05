from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.customer import CustomerSerializer
from api.services.customer import CustomerService


class CustomerViewSet(APIView):
    @staticmethod
    def post(request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = CustomerSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        customer = CustomerService.create(serializer.validated_data)
        serializer = CustomerSerializer(customer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def get(request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        customers = CustomerService.get_all()
        serializer = CustomerSerializer(customers, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class SingleCustomerViewSet(APIView):
    @staticmethod
    def get(request, pk: int):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if not CustomerService.exists(pk):
            return Response(status=status.HTTP_404_NOT_FOUND)

        customer = CustomerService.get(pk)
        serializer = CustomerSerializer(customer)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def put(request, pk: int):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if not CustomerService.exists(pk):
            return Response(status=status.HTTP_404_NOT_FOUND)

        customer = CustomerService.get(pk)
        serializer = CustomerSerializer(customer, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # print(f'{serializer.validated_data=}   |   {serializer.data=}')
        CustomerService.update(serializer.validated_data, serializer.instance)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def delete(request, pk: int):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if not CustomerService.exists(pk):
            return Response(status=status.HTTP_404_NOT_FOUND)

        CustomerService.delete(pk)

        return Response(status=status.HTTP_204_NO_CONTENT)
