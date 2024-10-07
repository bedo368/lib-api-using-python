from marshmallow import Schema, fields


class ItemSchema(Schema):
    book_id = fields.String(required=True)
    quantity = fields.Integer(required=True, validate=lambda n: n > 0)
    price = fields.Float(required=True, validate=lambda p: p >= 0)


class CreateNewOrderSchema(Schema):
    user_id = fields.String(required=True)
    date = fields.String(
        required=True
    )  # This could be further validated to check date format
    items = fields.List(fields.Nested(ItemSchema()), required=True)
