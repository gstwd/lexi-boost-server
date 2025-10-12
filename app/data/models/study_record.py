from datetime import datetime

from app.extensions import db


class StudyRecord(db.Model):
    __tablename__ = 'study_records'

    id = db.Column(db.Integer, primary_key=True)
    word_id = db.Column(
        db.Integer,
        db.ForeignKey('words.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    status = db.Column(db.String(20), nullable=False)  # 'learning', 'mastered', 'review', etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    word = db.relationship('Word', back_populates='study_records')

    def to_dict(self):
        return {
            'id': self.id,
            'word_id': self.word_id,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
