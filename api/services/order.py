from api.models.order import Order, OrderProduct


class OrderService:
    @staticmethod
    def create(order_data):
        print(f'{order_data=}')

        order = Order(
            customer=order_data['customer'],
            employee=order_data['employee'],
            date=order_data['date'],
            description=order_data['description'],
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

        products = new_order_data.get('products')
        if products:
            order.products.clear()

            for product in products:
                OrderProduct.objects.create(
                    order=order,
                    product=product.instance,
                    quantity=product.initial_data['quantity']
                )

        order.date = new_order_data['date']

        description = new_order_data.get('description')
        if description:
            order.description = description

        order.save()

    @classmethod
    def delete(cls, pk):
        Order.objects.filter(pk=pk).delete()

    @classmethod
    def get_quantity(cls, product_id: int, order_id: int) -> int | None:
        return OrderProduct.objects.get(product_id=product_id, order_id=order_id).quantity

    @classmethod
    def update_status(cls, new_status: str, order: Order):
        order.status = new_status
        order.save()
