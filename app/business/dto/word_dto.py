from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from app.extensions import ma
from app.data.models.word import Word

@dataclass
class WordDTO:
    id: Optional[int] = None
    word: Optional[str] = None
    meaning: Optional[str] = None
    created_at: Optional[datetime] = None

    @classmethod
    def from_model(cls, word_model):
        """从数据库模型创建DTO"""
        return cls(
            id=word_model.id,
            word=word_model.word,
            meaning=word_model.meaning,
            created_at=word_model.created_at
        )

    @classmethod
    def from_dict(cls, data):
        """从字典创建DTO（使用marshmallow验证）"""
        schema = WordDTOSchema()
        validated_data = schema.load(data)
        return cls(**validated_data)

    def to_dict(self):
        """转换为字典（使用marshmallow序列化）"""
        schema = WordDTOSchema()
        return schema.dump(self)

class WordDTOSchema(ma.SQLAlchemyAutoSchema):
    """WordDTO的Flask-Marshmallow auto schema - 基于SQLAlchemy模型自动生成"""
    class Meta:
        model = Word
        load_instance = False
        include_relationships = False
        dateformat = '%Y-%m-%dT%H:%M:%S.%fZ'