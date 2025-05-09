from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models.order import Order
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

        customer_id_to_filter = request.query_params.get('customer_id')
        if customer_id_to_filter:
            orders = OrderService.get_related_to_customer(customer_id_to_filter)
            serializer = OrderSerializer(orders, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        product_id_to_filter = request.query_params.get('product_id')
        if product_id_to_filter:
            orders = OrderService.get_related_to_product(product_id_to_filter)
            serializer = OrderSerializer(orders, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        employee_email_to_filter = request.query_params.get('employee_email')
        if employee_email_to_filter:
            orders = OrderService.get_related_to_employee(employee_email_to_filter)
            serializer = OrderSerializer(orders, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

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

    @staticmethod
    def patch(request, pk: int):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if not OrderService.exists(pk):
            return Response(status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get('status')

        print(Order.Status.choices)

        if not new_status:
            return Response('O campo \'status\' é obrigatório', status=status.HTTP_400_BAD_REQUEST)
        if new_status not in Order.Status.values:
            return Response(f'O status deve ser um dos indicados: {", ".join(Order.Status.values)}.', status=status.HTTP_400_BAD_REQUEST)

        order = OrderService.get(pk)
        OrderService.update_status(new_status, order)

        return Response(status=status.HTTP_204_NO_CONTENT)
