from typing import List, Optional
from app.extensions import db
from app.data.models import Word
from app.data.repositories.word_repository_interface import WordRepositoryInterface
from app.exceptions import DatabaseError

class WordRepository(WordRepositoryInterface):
    def get_all(self) -> List[Word]:
        try:
            return Word.query.all()
        except Exception as e:
            raise DatabaseError(f"Failed to fetch words: {str(e)}")
    
    def get_by_id(self, word_id: int) -> Optional[Word]:
        try:
            return Word.query.get(word_id)
        except Exception as e:
            raise DatabaseError(f"Failed to fetch word by id {word_id}: {str(e)}")
    
    def create(self, word: str, meaning: str) -> Word:
        try:
            new_word = Word(word=word, meaning=meaning)
            db.session.add(new_word)
            db.session.commit()
            return new_word
        except Exception as e:
            db.session.rollback()
            raise DatabaseError(f"Failed to create word: {str(e)}")
    
    def update(self, word_id: int, **kwargs) -> Optional[Word]:
        try:
            word = Word.query.get(word_id)
            if not word:
                return None
            
            for key, value in kwargs.items():
                if hasattr(word, key):
                    setattr(word, key, value)
            
            db.session.commit()
            return word
        except Exception as e:
            db.session.rollback()
            raise DatabaseError(f"Failed to update word {word_id}: {str(e)}")
    
    def delete(self, word_id: int) -> bool:
        try:
            word = Word.query.get(word_id)
            if not word:
                return False
            
            db.session.delete(word)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise DatabaseError(f"Failed to delete word {word_id}: {str(e)}")