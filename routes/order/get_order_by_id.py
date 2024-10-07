from core.database.database import Database
from models.order_model import OrderModel


def get_order_by_id(order_id):
    get_order_query = """
       SELECT 
    orders.id AS order_id, 
    orders.purchase_date, 
    orders.total_price,
    users.id AS user_id, 
    users.name AS user_name, 
    users.email AS user_email, 
    order_items.book_id, 
    books.title AS book_name, 
    order_items.quantity,
    order_items.price
FROM orders 
JOIN users ON orders.user_id = users.id
JOIN order_items ON orders.id = order_items.order_id
JOIN books ON order_items.book_id = books.id
where orders.id = %s
;
    """

    try:

        with Database() as db:
            db.cursor.execute(get_order_query, [str(order_id)])
            result = db.cursor.fetchall()
            if result.__len__() == 0:
                return {"message": "Order does not exist", "status": "error"}, 404

            print(result)

            order = OrderModel(
                order_id=str(result[0]["order_id"]),
                user_id=result[0]["user_id"],
                purchase_data=result[0]["purchase_date"],
                total_price=result[0]["total_price"],
                user_name=result[0]["user_name"],
                items=[
                    {
                        "book_id": o["book_id"],
                        "quantity": o["quantity"],
                        "price": o["price"],
                    }
                    for o in result
                ],
            )
            return {
                "data": order.to_dict(),
            }
    except Exception as e:
        return {"message": str(e), "status": "error"}, 500
