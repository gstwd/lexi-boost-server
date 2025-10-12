from datetime import datetime

from app.extensions import db


class Word(db.Model):
    __tablename__ = 'words'

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False, unique=True)
    input_times = db.Column(db.Integer, default=0, nullable=False)
    meaning = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    study_records = db.relationship(
        'StudyRecord',
        back_populates='word',
        cascade='all, delete-orphan',
        passive_deletes=True,
        lazy='select'
    )

    def to_dict(self):
        return {
            'id': self.id,
            'word': self.word,
            'input_times': self.input_times,
            'meaning': self.meaning,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
