from marshmallow import Schema, fields, validate


class CallSchema(Schema):
    user_name = fields.String(required=True, validate=validate.Length(min=1, max=32), allow_none=False)
    call_duration = fields.Integer(required=True,
                                   strict=True,
                                   validate=validate.Range(min=1, error="Value must be greater than 0"),
                                   allow_none=False)


class BillingSchema(Schema):
    call_count = fields.Integer()
    block_count = fields.Integer()
