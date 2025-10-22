from dataclasses import dataclass
from typing import Optional

from app.data.models.word_entry import WordEntry
from app.extensions import ma


@dataclass
class WordEntryDTO:
    id: Optional[int] = None
    word: Optional[str] = None
    phonetic: Optional[str] = None
    definition: Optional[str] = None
    translation: Optional[str] = None
    pos: Optional[str] = None
    collins: Optional[str] = None
    oxford: Optional[str] = None
    tag: Optional[str] = None
    bnc: Optional[str] = None
    frq: Optional[str] = None
    exchange: Optional[str] = None
    detail: Optional[str] = None
    audio: Optional[str] = None

    @classmethod
    def from_model(cls, entry_model: WordEntry) -> "WordEntryDTO":
        """Build a DTO from a WordEntry database model."""
        return cls(
            id=entry_model.id,
            word=entry_model.word,
            phonetic=entry_model.phonetic,
            definition=entry_model.definition,
            translation=entry_model.translation,
            pos=entry_model.pos,
            collins=entry_model.collins,
            oxford=entry_model.oxford,
            tag=entry_model.tag,
            bnc=entry_model.bnc,
            frq=entry_model.frq,
            exchange=entry_model.exchange,
            detail=entry_model.detail,
            audio=entry_model.audio,
        )

    @classmethod
    def from_dict(cls, data: dict) -> "WordEntryDTO":
        """Validate incoming payload and construct a DTO."""
        schema = WordEntryDTOSchema()
        validated_data = schema.load(data)
        return cls(**validated_data)

    def to_dict(self) -> dict:
        """Serialize the DTO into a dictionary using Marshmallow."""
        schema = WordEntryDTOSchema()
        return schema.dump(self)


class WordEntryDTOSchema(ma.SQLAlchemyAutoSchema):
    """Auto schema definition for WordEntryDTO serialisation/deserialisation."""

    class Meta:
        model = WordEntry
        load_instance = False
        include_relationships = False
        dateformat = '%Y-%m-%dT%H:%M:%S.%fZ'
