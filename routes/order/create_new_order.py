import uuid

import psycopg2
from flask import request, jsonify
from marshmallow import ValidationError

from core.database.database import Database
from routes.order.validate_reqests.validate_cerate_request import CreateNewOrderSchema


# there a trigger in the database that reduce the number of items by the number on the order and if thier is no enugh itemes in the store it stop and throw error
# you can handele this by your self in the code but id add trigger
def create_new_order():

    try:
        data = request.get_json()

        CreateNewOrderSchema().load(data)

        with Database() as db:
            total_price = sum(
                item["quantity"] * item["price"] for item in data["items"]
            )

            order_id = uuid.uuid4()

            db.cursor.execute(
                "insert into orders (id , user_id , purchase_date , total_price ) VALUES (%s , %s , %s , %s)",
                (str(order_id), data["user_id"], data["date"], total_price),
            )
            item_tuples = []
            for item in data["items"]:
                item_tuple = (
                    str(order_id),
                    item["book_id"],
                    item["quantity"],
                    item["price"],
                )
                item_tuples.append(item_tuple)

            db.execute_many(
                "insert into order_items ( order_id, book_id, quantity, price)  values ( %s , %s , %s , %s )",
                item_tuples,
            )

            return {"message": "Order created successfully", "data": order_id}, 201

    except ValidationError as err:
        return (
            jsonify(
                {
                    "errors": err.messages,
                    "status": "fail",
                    "message": "error on validate data check errors for more detail",
                }
            ),
            400,
        )
    except psycopg2.OperationalError as op_err:
        return (
            jsonify(
                {
                    "errors": op_err.args[0],
                }
            ),
            500,
        )
    except psycopg2.ProgrammingError as prog_err:
        return (
            jsonify(
                {
                    "errors": prog_err.args[0],
                }
            ),
            500,
        )
    except psycopg2.IntegrityError as integrity_err:
        return (
            jsonify(
                {
                    "errors": integrity_err.args[0],
                }
            ),
            500,
        )

    except Exception as e:
        # print(e.with_traceback())
        return jsonify({"error": str(e)}), 500
