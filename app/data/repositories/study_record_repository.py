from typing import Optional
from app.extensions import db
from app.data.models import StudyRecord
from app.data.repositories.study_record_repository_interface import StudyRecordRepositoryInterface
from app.exceptions import DatabaseError

class StudyRecordRepository(StudyRecordRepositoryInterface):
    def get_by_word_id(self, word_id: int) -> Optional[StudyRecord]:
        try:
            return StudyRecord.query.filter_by(word_id=word_id).first()
        except Exception as e:
            raise DatabaseError(f"Failed to fetch study record for word {word_id}: {str(e)}")
    
    def create(self, word_id: int, status: str) -> StudyRecord:
        try:
            study_record = StudyRecord(word_id=word_id, status=status)
            db.session.add(study_record)
            db.session.commit()
            return study_record
        except Exception as e:
            db.session.rollback()
            raise DatabaseError(f"Failed to create study record: {str(e)}")
    
    def update(self, record_id: int, **kwargs) -> Optional[StudyRecord]:
        try:
            record = StudyRecord.query.get(record_id)
            if not record:
                return None
            
            for key, value in kwargs.items():
                if hasattr(record, key):
                    setattr(record, key, value)
            
            db.session.commit()
            return record
        except Exception as e:
            db.session.rollback()
            raise DatabaseError(f"Failed to update study record {record_id}: {str(e)}")
    
    def update_by_word_id(self, word_id: int, status: str) -> Optional[StudyRecord]:
        try:
            record = StudyRecord.query.filter_by(word_id=word_id).first()
            if not record:
                return None
            
            record.status = status
            db.session.commit()
            return record
        except Exception as e:
            db.session.rollback()
            raise DatabaseError(f"Failed to update study record for word {word_id}: {str(e)}")