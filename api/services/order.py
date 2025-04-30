from api.models.order import Order, OrderProduct


class OrderService:
    @staticmethod
    def create(order_data):
        # print(f'{order_data=}')

        order = Order(
            customer=order_data['customer'],
            employee=order_data['employee'],
        )

        order.save()

        for product in order_data['products']:
            OrderProduct.objects.create(
                order=order,
                product=product.instance,
                quantity=product.initial_data['quantity']
            )

        return order

    @classmethod
    def get(cls, pk):
        return Order.objects.get(pk=pk)

    @staticmethod
    def get_all():
        return Order.objects.all()

    @classmethod
    def exists(cls, pk):
        return Order.objects.filter(pk=pk).exists()

    @staticmethod
    def update(new_order_data: dict, order: Order):
        customer = new_order_data.get('customer')
        if customer:
            order.customer = customer

        employee = new_order_data.get('employee')
        if employee:
            order.employee = employee

        order.save()

    @classmethod
    def delete(cls, pk):
        Order.objects.filter(pk=pk).delete()
