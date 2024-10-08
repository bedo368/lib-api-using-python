from jsonschema.validators import validates
from marshmallow import Schema, fields ,validate


class ReturnBookValidateSchema(Schema):

    return_date = fields.DateTime(data_key='return_date' , required=True)

    fine = fields.Float(data_key='fine' , required=True , validate= validate.Range(min=0 , max=5 , error="book fine state should be between 0 and 5"))
