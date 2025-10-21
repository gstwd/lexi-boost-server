from typing import List, Optional

from sqlalchemy.exc import IntegrityError

from app.data.models import WordRecord
from app.extensions import db

class WordRecordRepository:
    def get_all(self) -> List[WordRecord]:
        return WordRecord.query.all()

    def get_by_id(self, word_id: int) -> Optional[WordRecord]:
        return db.session.get(WordRecord, word_id)

    def create(self, **kwargs) -> WordRecord:
        new_word = WordRecord(**kwargs)
        db.session.add(new_word)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise
        return new_word

    def update(self, word_id: int, **kwargs) -> Optional[WordRecord]:
        word = db.session.get(WordRecord, word_id)
        if not word:
            return None

        for key, value in kwargs.items():
            if hasattr(word, key):
                setattr(word, key, value)

        db.session.commit()
        return word

    def delete(self, word_id: int) -> bool:
        word = db.session.get(WordRecord, word_id)
        if not word:
            return False

        db.session.delete(word)
        db.session.commit()
        return True
