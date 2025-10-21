from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.data.models.study_record import StudyRecord
from app.extensions import ma


@dataclass
class StudyRecordDTO:
    id: Optional[int] = None
    word_id: Optional[int] = None
    status: Optional[str] = None
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None

    @classmethod
    def from_model(cls, record_model: StudyRecord) -> "StudyRecordDTO":
        """Build a DTO from a StudyRecord database model."""
        return cls(
            id=record_model.id,
            word_id=record_model.word_id,
            status=record_model.status,
            create_time=record_model.create_time,
            update_time=record_model.update_time,
        )

    @classmethod
    def from_dict(cls, data: dict) -> "StudyRecordDTO":
        """Validate incoming payload and construct a DTO."""
        schema = StudyRecordDTOSchema()
        validated_data = schema.load(data)
        return cls(**validated_data)

    def to_dict(self) -> dict:
        """Serialize the DTO into a dictionary using Marshmallow."""
        schema = StudyRecordDTOSchema()
        return schema.dump(self)


class StudyRecordDTOSchema(ma.SQLAlchemyAutoSchema):
    """Auto schema definition for StudyRecordDTO serialisation/deserialisation."""

    class Meta:
        model = StudyRecord
        load_instance = False
        include_relationships = False
        dateformat = '%Y-%m-%dT%H:%M:%S.%fZ'
