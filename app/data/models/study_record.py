from app.extensions import db
from datetime import datetime

class StudyRecord(db.Model):
    __tablename__ = 'study_records'

    id = db.Column(db.Integer, primary_key=True)
    word_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # 'learning', 'mastered', 'review', etc.
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'word_id': self.word_id,
            'status': self.status,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'update_time': self.update_time.isoformat() if self.update_time else None
        }