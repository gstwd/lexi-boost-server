from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class StudyRecordDTO:
    id: Optional[int] = None
    word_id: Optional[int] = None
    status: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @classmethod
    def from_model(cls, record_model):
        return cls(
            id=record_model.id,
            word_id=record_model.word_id,
            status=record_model.status,
            created_at=record_model.created_at,
            updated_at=record_model.updated_at
        )
    
    def to_dict(self):
        return {
            'id': self.id,
            'word_id': self.word_id,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }