from app.extensions import db
from datetime import datetime

class Word(db.Model):
    __tablename__ = 'personal_words'

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False, unique=True)
    input_times = db.Column(db.Integer, default=0, nullable=False, unique=True)
    meaning = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now())

    def to_dict(self):
        return {
            'id': self.id,
            'word': self.word,
            'input_times': self.input_times,
            'meaning': self.meaning,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'update_time': self.update_time.isoformat() if self.update_time else None
        }