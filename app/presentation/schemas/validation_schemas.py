from marshmallow import Schema, fields, validate, ValidationError as MarshmallowValidationError

class StudyRecordSchema(Schema):
    word_id = fields.Integer(required=True, validate=validate.Range(min=1))
    status = fields.String(required=True, validate=validate.OneOf([
        'learning', 'mastered', 'review', 'difficult'
    ]))

class WordSchema(Schema):
    word = fields.String(required=True, validate=validate.Length(min=1, max=100))
    meaning = fields.String(required=True, validate=validate.Length(min=1, max=1000))

class WordQuerySchema(Schema):
    page = fields.Integer(missing=1, validate=validate.Range(min=1))
    per_page = fields.Integer(missing=10, validate=validate.Range(min=1, max=100))
    search = fields.String(missing=None, validate=validate.Length(max=100))

def validate_json(schema_class):
    def decorator(f):
        def wrapper(*args, **kwargs):
            from flask import request, jsonify
            from app.exceptions import ValidationError

            try:
                schema = schema_class()
                data = request.get_json()

                if not data:
                    raise ValidationError("No JSON data provided")

                validated_data = schema.load(data)
                request.validated_data = validated_data
                return f(*args, **kwargs)

            except MarshmallowValidationError as e:
                raise ValidationError(f"Validation failed: {e.messages}")

        wrapper.__name__ = f.__name__
        return wrapper
    return decorator

def validate_args(schema_class):
    def decorator(f):
        def wrapper(*args, **kwargs):
            from flask import request
            from app.exceptions import ValidationError

            try:
                schema = schema_class()
                validated_data = schema.load(request.args)
                request.validated_args = validated_data
                return f(*args, **kwargs)

            except MarshmallowValidationError as e:
                raise ValidationError(f"Query parameter validation failed: {e.messages}")

        wrapper.__name__ = f.__name__
        return wrapper
    return decorator