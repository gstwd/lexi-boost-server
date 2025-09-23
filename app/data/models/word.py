from app.extensions import db
from datetime import datetime

class Word(db.Model):
    __tablename__ = 'words'

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False, unique=True)
    meaning = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    study_records = db.relationship('StudyRecord', backref='word_ref', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'word': self.word,
            'meaning': self.meaning,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }