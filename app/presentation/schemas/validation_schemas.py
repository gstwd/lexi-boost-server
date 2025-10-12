from functools import wraps

from marshmallow import (
    ValidationError as MarshmallowValidationError,
    fields,
    post_dump,
    pre_load,
    validate,
)
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.data.models.study_record import StudyRecord
from app.data.models.word import Word
from app.exceptions import APIException, ValidationError
from app.extensions import ma


# ============ Request Schemas ============
class StudyRecordSchema(ma.Schema):
    word_id = fields.Integer(required=True, validate=validate.Range(min=1))
    status = fields.String(
        required=True,
        validate=validate.OneOf(['learning', 'mastered', 'review', 'difficult']),
    )


class WordSchema(ma.Schema):
    word = fields.String(required=True, validate=validate.Length(min=1, max=100))
    meaning = fields.String(required=True, validate=validate.Length(min=1, max=1000))

    @pre_load
    def clean_data(self, data, **kwargs):
        """Normalise free-text fields before validation."""
        if data.get('word'):
            data['word'] = data['word'].strip().lower()
        if data.get('meaning'):
            data['meaning'] = data['meaning'].strip()
        return data


class WordQuerySchema(ma.Schema):
    page = fields.Integer(load_default=1, validate=validate.Range(min=1))
    per_page = fields.Integer(load_default=10, validate=validate.Range(min=1, max=100))
    search = fields.String(load_default=None, validate=validate.Length(max=100))

    @pre_load
    def clean_search(self, data, **kwargs):
        """Trim search parameters."""
        if data.get('search'):
            data['search'] = data['search'].strip()
        return data


# ============ Response Schemas ============
class WordResponseSchema(SQLAlchemyAutoSchema):
    """Serialise Word resources."""

    class Meta:
        model = Word
        load_instance = True
        include_relationships = False
        dateformat = '%Y-%m-%dT%H:%M:%S.%fZ'

    @post_dump
    def format_response(self, data, **kwargs):
        for field in ['created_at', 'updated_at']:
            if data.get(field):
                data[field] = data[field].replace('+00:00', 'Z')
        return data


class StudyRecordResponseSchema(SQLAlchemyAutoSchema):
    """Serialise StudyRecord resources."""

    class Meta:
        model = StudyRecord
        load_instance = True
        include_relationships = False
        dateformat = '%Y-%m-%dT%H:%M:%S.%fZ'

    @post_dump
    def format_response(self, data, **kwargs):
        for field in ['created_at', 'updated_at']:
            if data.get(field):
                data[field] = data[field].replace('+00:00', 'Z')
        return data


class WordWithStudyRecordSchema(SQLAlchemyAutoSchema):
    """Serialise Word resources together with an optional study record."""

    study_record = fields.Nested(StudyRecordResponseSchema, allow_none=True)

    class Meta:
        model = Word
        load_instance = True
        include_relationships = False
        dateformat = '%Y-%m-%dT%H:%M:%S.%fZ'

    @post_dump
    def format_response(self, data, **kwargs):
        for field in ['created_at', 'updated_at']:
            if data.get(field):
                data[field] = data[field].replace('+00:00', 'Z')
        return data


# ============ DTO Conversion Helpers ============
class SchemaConverter:
    """Helper methods for converting DTOs into API responses."""

    @staticmethod
    def word_to_response(word_dto):
        schema = WordResponseSchema()
        return schema.dump(word_dto.__dict__)

    @staticmethod
    def study_record_to_response(study_record_dto):
        schema = StudyRecordResponseSchema()
        return schema.dump(study_record_dto.__dict__)

    @staticmethod
    def word_with_study_record_to_response(word_dto, study_record_dto=None):
        data = word_dto.__dict__.copy()
        data['study_record'] = study_record_dto.__dict__ if study_record_dto else None

        schema = WordWithStudyRecordSchema()
        return schema.dump(data)

    @staticmethod
    def words_to_response(word_dtos):
        schema = WordResponseSchema(many=True)
        return schema.dump([dto.__dict__ for dto in word_dtos])


# ============ Validation Decorators ============
def validate_json(schema_class):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            from flask import request

            schema = schema_class()
            data = request.get_json(silent=True)

            if data is None:
                raise APIException("No JSON data provided", error_code=1004, status_code=415)

            try:
                validated_data = schema.load(data)
            except MarshmallowValidationError as exc:
                raise ValidationError(f"Validation failed: {exc.messages}")

            request.validated_data = validated_data
            return f(*args, **kwargs)

        return wrapper

    return decorator


def validate_args(schema_class):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            from flask import request

            try:
                schema = schema_class()
                validated_data = schema.load(request.args)
            except MarshmallowValidationError as exc:
                raise ValidationError(f"Query parameter validation failed: {exc.messages}")

            request.validated_args = validated_data
            return f(*args, **kwargs)

        return wrapper

    return decorator
