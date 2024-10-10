from marshmallow import Schema, fields, validate


class RentBookRequestSchema(Schema):
    user_id = fields.UUID(required=True)

    time_by_days = fields.Float(
        required=True,
        validate=validate.Range(
            min=1, max=20, error="Time to rent book  must be between 1 and 20 day."
        ),
    )
