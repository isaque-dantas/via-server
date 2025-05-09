from django.db.models import Count, Sum, F, Value

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

        if not query.get('total_amount_invoiced'):
            query['total_amount_invoiced'] = 0

        if not query.get('total_sold_products_quantity'):
            query['total_sold_products_quantity'] = 0

        return query

    @classmethod
    def get_pending_orders(cls):
        return Order.objects.filter(status=Order.Status.IN_PROGRESS).all()

    @classmethod
    def get_most_active_customers(cls):
        customers_with_orders = (
            Customer.objects
            .annotate(orders_count=Count('orders'))
            .order_by('-orders_count')
        )

        return customers_with_orders
        # return customers_with_orders.union(
        #     Customer.objects
        #     .annotate(orders_count=Value(239))
        #     .exclude(pk__in=customers_with_orders)
        # )
