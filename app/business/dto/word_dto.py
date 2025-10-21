from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

from app.data.models.word_records import WordRecord
from app.extensions import ma


@dataclass
class WordDTO:
    id: Optional[int] = None
    word: Optional[str] = None
    word_entry_id: Optional[int] = None
    input_times: Optional[int] = None
    meaning: Optional[str] = None
    context: Optional[str] = None
    tags: Optional[List[str]] = None
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None

    @classmethod
    def from_model(cls, word_model: WordRecord) -> "WordDTO":
        """Build a DTO from a WordRecord database model."""
        return cls(
            id=word_model.id,
            word=word_model.word,
            input_times=word_model.input_times,
            meaning=word_model.meaning,
            create_time=word_model.create_time,
            update_time=word_model.update_time,
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
        model = WordRecord
        load_instance = False
        include_relationships = False
        dateformat = '%Y-%m-%dT%H:%M:%S.%fZ'
