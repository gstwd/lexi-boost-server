from typing import Optional

from app.data.models import StudyRecord
from app.extensions import db


class StudyRecordRepository:
    def get_by_word_id(self, word_id: int) -> Optional[StudyRecord]:
        return StudyRecord.query.filter_by(word_id=word_id).first()

    def create(self, word_id: int, status: str) -> StudyRecord:
        study_record = StudyRecord(word_id=word_id, status=status)
        db.session.add(study_record)
        db.session.commit()
        return study_record

    def update(self, record_id: int, **kwargs) -> Optional[StudyRecord]:
        record = db.session.get(StudyRecord, record_id)
        if not record:
            return None

        for key, value in kwargs.items():
            if hasattr(record, key):
                setattr(record, key, value)

        db.session.commit()
        return record

    def update_by_word_id(self, word_id: int, status: str) -> Optional[StudyRecord]:
        record = StudyRecord.query.filter_by(word_id=word_id).first()
        if not record:
            return None

        record.status = status
        db.session.commit()
        return record
