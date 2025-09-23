from marshmallow import fields, validate, ValidationError as MarshmallowValidationError, pre_load, post_dump
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.extensions import ma
from app.data.models.word import Word
from app.data.models.study_record import StudyRecord

# ============ 输入验证 Schemas ============
class StudyRecordSchema(ma.Schema):
    word_id = fields.Integer(required=True, validate=validate.Range(min=1))
    status = fields.String(required=True, validate=validate.OneOf([
        'learning', 'mastered', 'review', 'difficult'
    ]))

class WordSchema(ma.Schema):
    word = fields.String(required=True, validate=validate.Length(min=1, max=100))
    meaning = fields.String(required=True, validate=validate.Length(min=1, max=1000))

    @pre_load
    def clean_data(self, data, **kwargs):
        """数据清洗和格式化"""
        if 'word' in data and data['word']:
            data['word'] = data['word'].strip().lower()
        if 'meaning' in data and data['meaning']:
            data['meaning'] = data['meaning'].strip()
        return data

class WordQuerySchema(ma.Schema):
    page = fields.Integer(load_default=1, validate=validate.Range(min=1))
    per_page = fields.Integer(load_default=10, validate=validate.Range(min=1, max=100))
    search = fields.String(load_default=None, validate=validate.Length(max=100))

    @pre_load
    def clean_search(self, data, **kwargs):
        """清洗搜索参数"""
        if 'search' in data and data['search']:
            data['search'] = data['search'].strip()
        return data

# ============ 响应序列化 Schemas（使用SQLAlchemyAutoSchema） ============
class WordResponseSchema(SQLAlchemyAutoSchema):
    """Word响应序列化Schema - 基于SQLAlchemy模型自动生成"""
    class Meta:
        model = Word
        load_instance = True
        include_relationships = False
        dateformat = '%Y-%m-%dT%H:%M:%S.%fZ'

    @post_dump
    def format_response(self, data, **kwargs):
        """响应格式化"""
        if data.get('created_at'):
            data['created_at'] = data['created_at'].replace('+00:00', 'Z')
        return data

class StudyRecordResponseSchema(SQLAlchemyAutoSchema):
    """StudyRecord响应序列化Schema - 基于SQLAlchemy模型自动生成"""
    class Meta:
        model = StudyRecord
        load_instance = True
        include_relationships = False
        dateformat = '%Y-%m-%dT%H:%M:%S.%fZ'

    @post_dump
    def format_response(self, data, **kwargs):
        """响应格式化"""
        for field in ['created_at', 'updated_at']:
            if data.get(field):
                data[field] = data[field].replace('+00:00', 'Z')
        return data

class WordWithStudyRecordSchema(SQLAlchemyAutoSchema):
    """Word与StudyRecord嵌套响应Schema"""
    study_record = fields.Nested(StudyRecordResponseSchema, allow_none=True)

    class Meta:
        model = Word
        load_instance = True
        include_relationships = False
        dateformat = '%Y-%m-%dT%H:%M:%S.%fZ'

    @post_dump
    def format_response(self, data, **kwargs):
        """响应格式化"""
        if data.get('created_at'):
            data['created_at'] = data['created_at'].replace('+00:00', 'Z')
        return data

# ============ DTO转换助手类 ============
class SchemaConverter:
    """Schema转换助手类，用于DTO与Model之间的转换"""

    @staticmethod
    def word_to_response(word_dto):
        """将WordDTO转换为响应数据"""
        schema = WordResponseSchema()
        return schema.dump(word_dto.__dict__)

    @staticmethod
    def study_record_to_response(study_record_dto):
        """将StudyRecordDTO转换为响应数据"""
        schema = StudyRecordResponseSchema()
        return schema.dump(study_record_dto.__dict__)

    @staticmethod
    def word_with_study_record_to_response(word_dto, study_record_dto=None):
        """将Word和StudyRecord组合转换为响应数据"""
        data = word_dto.__dict__.copy()
        if study_record_dto:
            data['study_record'] = study_record_dto.__dict__
        else:
            data['study_record'] = None

        schema = WordWithStudyRecordSchema()
        return schema.dump(data)

    @staticmethod
    def words_to_response(word_dtos):
        """将WordDTO列表转换为响应数据"""
        schema = WordResponseSchema(many=True)
        return schema.dump([dto.__dict__ for dto in word_dtos])

# ============ 验证装饰器 ============

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