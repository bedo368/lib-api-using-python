from gi.overrides import override


class OrderModel:
    def __init__(self, order_id: str, user_id: str, purchase_data: str, user_name: str, items: list, total_price: float):
        self.id = order_id
        self.user_id = user_id
        self.purchase_data = purchase_data
        self.user_name = user_name
        self.items = items
        self.total_price = total_price

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            order_id=data['id'],
            user_id=data['user_id'],
            purchase_data=data['purchase_data'],
            user_name=data['user_name'],
            items=data['items'],
            total_price=data['total_price']
        )


    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'purchase_data': self.purchase_data,
            'user_name': self.user_name,
            'items': self.items,
            "total_price":self.total_price
        }

    def __repr__(self):
        return str(self.to_dict())