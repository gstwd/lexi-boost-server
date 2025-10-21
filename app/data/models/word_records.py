from datetime import datetime, UTC

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.dialects.postgresql import JSONB

from app.extensions import db


class WordRecord(db.Model):
    __tablename__ = 'word_records'

    id = Column(Integer, primary_key=True)
    word = Column(String(100), nullable=False)
    word_entry_id = Column(Integer, nullable=True)
    meaning = Column(Text, nullable=False)
    tags = Column(JSONB, nullable=True)
    location = Column(JSONB, nullable=True)
    context = Column(String(255), nullable=True)
    input_times = Column(Integer, default=0, nullable=False)
    notes = Column(String(255), nullable=True)
    source_type = Column(String(255), nullable=True)
    source_detail = Column(String(255), nullable=True)
    create_time = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)
    update_time = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC),
                         onupdate=lambda: datetime.now(UTC), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'word': self.word,
            'word_entry_id': self.word_entry_id,
            'meaning': self.meaning,
            'tags': self.tags if self.tags else [],
            'location': self.location if self.location else {},
            'context': self.context,
            'input_times': self.input_times,
            'notes': self.notes,
            'source_type': self.source_type,
            'source_detail': self.source_detail,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'update_time': self.update_time.isoformat() if self.update_time else None
        }
