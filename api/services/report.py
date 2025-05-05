from django.db.models import Count, Sum, F

from api.models.customer import Customer
from api.models.order import OrderProduct, Order
from api.serializers.customer import CustomerSerializer
from api.serializers.order import OrderSerializer


class ReportService:
    @classmethod
    def get_reports(cls):
        selling_resume = ReportService.get_selling_resume()

        pending_orders = ReportService.get_pending_orders()
        orders_serializer = OrderSerializer(pending_orders, many=True)

        most_active_customers = ReportService.get_most_active_customers()
        customers_serializer = CustomerSerializer(most_active_customers, many=True)

        return {
            'selling_resume': selling_resume,
            'pending_orders': orders_serializer.data,
            'most_active_customers': customers_serializer.data,
        }

    @classmethod
    def get_selling_resume(cls):
        query = (
            OrderProduct.objects.filter(order__status='Finalizado')
            .aggregate(
                total_amount_invoiced=Sum(F('quantity') * F('product__price')),
                total_sold_products_quantity=Sum('quantity')
            )
        )

        query['orders_quantity'] = Order.objects.count()

        return query

    @classmethod
    def get_pending_orders(cls):
        return Order.objects.filter(status=Order.Status.IN_PROGRESS).all()

    @classmethod
    def get_most_active_customers(cls):
        return (
            Customer.objects.
            annotate(orders_count=Count('orders'))
            .order_by('-orders_count')
        )
