from api.models.order import OrderProduct


class OrderProductService:

    @classmethod
    def get_quantity(cls, product_id: int, order_id: int) -> int | None:
        return OrderProduct.objects.get(product_id=product_id, order_id=order_id).quantity