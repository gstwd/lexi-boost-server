from app.extensions import db
from datetime import datetime

class StudyRecord(db.Model):
    __tablename__ = 'study_records'

    id = db.Column(db.Integer, primary_key=True)
    word_id = db.Column(db.Integer, db.ForeignKey('words.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # 'learning', 'mastered', 'review', etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'word_id': self.word_id,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }