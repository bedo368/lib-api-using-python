

from flask import request
from marshmallow import ValidationError

from core.database.database import Database
from models.order_model import OrderModel
from routes.order.validate_reqests.vlidate_get_orders_by_page import ValidatePageSchema


def get_orders_by_page():
    query = """
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
OFFSET %s ROWS FETCH NEXT 5 ROWS ONLY
;
    """

    try:

        data = request.get_json()
        ValidatePageSchema().load(data)

        with Database() as db:
            db.cursor.execute(query  , (data['page'],))
            result = db.cursor.fetchall()

            if result.__len__() == 0:
                return  {
                    "status": "failure",
                    "message": "No more orders found"

                },404

            # Organize the results by order_id
            orders:dict[str:OrderModel] = {}
            for row in result:
                order_id = row['order_id']
                if order_id not in orders:
                    orders[order_id] = OrderModel(
                        order_id= str(order_id) ,
                        total_price=row["total_price"],
                        user_id=row["user_id"] ,
                        purchase_data= str(row["purchase_date"]) ,
                        user_name=row["user_name"] ,
                        items=[{
                        "book_id":row["book_id"] ,
                        "title":row["book_name"] ,
                        "quantity":row["quantity"] ,
                            "price":row["price"]
                        }])
                    # {
                    #     'id': order_id,
                    #     'user_id': row['user_id'],
                    #     'purchase_data': row['order_date'],
                    #     'user_name': row['user_name'],
                    #     'items': []
                    # }
                # Append each item to the order_items list for the order
                else:
                    orders[order_id].items.append({
                        'book_id': row['book_id'],
                        'book_name': row['book_name'],
                        'quantity': row['quantity'],
                        "price": row["price"]

                    })

            print(orders)

            return  {
                "message":"success",
                "data":[order.to_dict() for order in orders.values()],
                "page":data["page"]

            },200


    except ValidationError as err:
        return  {"errors":err.messages , "message":"error on validation check errors key for more detail"}, 400
    except Exception as err:
        return  {
            "message": str(err)

        }, 500
