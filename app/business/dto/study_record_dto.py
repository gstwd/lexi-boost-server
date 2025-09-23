from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.extensions import ma
from app.data.models.study_record import StudyRecord

@dataclass
class StudyRecordDTO:
    id: Optional[int] = None
    word_id: Optional[int] = None
    status: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_model(cls, record_model):
        """从数据库模型创建DTO"""
        return cls(
            id=record_model.id,
            word_id=record_model.word_id,
            status=record_model.status,
            created_at=record_model.created_at,
            updated_at=record_model.updated_at
        )

    @classmethod
    def from_dict(cls, data):
        """从字典创建DTO（使用marshmallow验证）"""
        schema = StudyRecordDTOSchema()
        validated_data = schema.load(data)
        return cls(**validated_data)

    def to_dict(self):
        """转换为字典（使用marshmallow序列化）"""
        schema = StudyRecordDTOSchema()
        return schema.dump(self)

class StudyRecordDTOSchema(SQLAlchemyAutoSchema):
    """StudyRecordDTO的Flask-Marshmallow auto schema - 基于SQLAlchemy模型自动生成"""
    class Meta:
        model = StudyRecord
        load_instance = False
        include_relationships = False
        dateformat = '%Y-%m-%dT%H:%M:%S.%fZ'