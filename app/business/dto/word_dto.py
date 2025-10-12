from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.data.models.word import Word
from app.extensions import ma


@dataclass
class WordDTO:
    id: Optional[int] = None
    word: Optional[str] = None
    input_times: Optional[int] = None
    meaning: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_model(cls, word_model: Word) -> "WordDTO":
        """Build a DTO from a Word database model."""
        return cls(
            id=word_model.id,
            word=word_model.word,
            input_times=word_model.input_times,
            meaning=word_model.meaning,
            created_at=word_model.created_at,
            updated_at=word_model.updated_at,
        )

    @classmethod
    def from_dict(cls, data: dict) -> "WordDTO":
        """Validate incoming payload and construct a DTO."""
        schema = WordDTOSchema()
        validated_data = schema.load(data)
        return cls(**validated_data)

    def to_dict(self) -> dict:
        """Serialize the DTO into a dictionary using Marshmallow."""
        schema = WordDTOSchema()
        return schema.dump(self)


class WordDTOSchema(ma.SQLAlchemyAutoSchema):
    """Auto schema definition for WordDTO serialisation/deserialisation."""

    class Meta:
        model = Word
        load_instance = False
        include_relationships = False
        dateformat = '%Y-%m-%dT%H:%M:%S.%fZ'
