from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.order import OrderSerializer
from api.services.order import OrderService


class OrderViewSet(APIView):
    @staticmethod
    def post(request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = OrderSerializer(
            data={
                **request.data,
                'employee': request.user
            }
        )

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        order = OrderService.create(serializer.validated_data)
        serializer = OrderSerializer(order)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def get(request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        orders = OrderService.get_all()
        serializer = OrderSerializer(orders, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class SingleOrderViewSet(APIView):
    @staticmethod
    def get(request, pk: int):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if not OrderService.exists(pk):
            return Response(status=status.HTTP_404_NOT_FOUND)

        order = OrderService.get(pk)
        serializer = OrderSerializer(order)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def put(request, pk: int):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if not OrderService.exists(pk):
            return Response(status=status.HTTP_404_NOT_FOUND)

        order = OrderService.get(pk)
        serializer = OrderSerializer(
            order,
            data={
                **request.data,
                'employee': request.user
            }
        )

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        OrderService.update(serializer.validated_data, serializer.instance)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def delete(request, pk: int):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if not OrderService.exists(pk):
            return Response(status=status.HTTP_404_NOT_FOUND)

        OrderService.delete(pk)

        return Response(status=status.HTTP_204_NO_CONTENT)
