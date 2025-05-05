from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Employee
from api.serializers.product import ProductSerializer
from api.services.product import ProductService


class ProductViewSet(APIView):
    @staticmethod
    def post(request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = ProductSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        product = ProductService.create(serializer.validated_data)
        serializer = ProductSerializer(product)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def get(request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        products = ProductService.get_all()
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class SingleProductViewSet(APIView):
    @staticmethod
    def get(request, pk: int):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if not ProductService.exists(pk):
            return Response(status=status.HTTP_404_NOT_FOUND)

        product = ProductService.get(pk)
        serializer = ProductSerializer(product)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def put(request, pk: int):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if not ProductService.exists(pk):
            return Response(status=status.HTTP_404_NOT_FOUND)

        product = ProductService.get(pk)
        serializer = ProductSerializer(product, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        ProductService.update(serializer.validated_data, serializer.instance)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def delete(request, pk: int):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if not ProductService.exists(pk):
            return Response(status=status.HTTP_404_NOT_FOUND)

        ProductService.delete(pk)

        return Response(status=status.HTTP_204_NO_CONTENT)
