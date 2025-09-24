from typing import List, Optional
from app.extensions import db
from app.data.models import Word

class WordRepository:
    def get_all(self) -> List[Word]:
        return Word.query.all()

    def get_by_id(self, word_id: int) -> Optional[Word]:
        return Word.query.get(word_id)

    def create(self, word: str, meaning: str) -> Word:
        new_word = Word(word=word, meaning=meaning)
        db.session.add(new_word)
        db.session.commit()
        return new_word

    def update(self, word_id: int, **kwargs) -> Optional[Word]:
        word = Word.query.get(word_id)
        if not word:
            return None

        for key, value in kwargs.items():
            if hasattr(word, key):
                setattr(word, key, value)

        db.session.commit()
        return word

    def delete(self, word_id: int) -> bool:
        word = Word.query.get(word_id)
        if not word:
            return False

        db.session.delete(word)
        db.session.commit()
        return True