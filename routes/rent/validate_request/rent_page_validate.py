from marshmallow import Schema, fields


class RentPageValidate(Schema):
    page = fields.Integer()
