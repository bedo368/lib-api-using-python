from marshmallow import Schema, fields, validates, ValidationError

class ValidatePageSchema(Schema):
    page = fields.Integer(required=True)

    @validates('page')
    def validate_page(self, value):
        if value <= 0:
            raise ValidationError('Page must be greater than 0.')