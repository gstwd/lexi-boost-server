from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class WordDTO:
    id: Optional[int] = None
    word: Optional[str] = None
    meaning: Optional[str] = None
    created_at: Optional[datetime] = None
    
    @classmethod
    def from_model(cls, word_model):
        return cls(
            id=word_model.id,
            word=word_model.word,
            meaning=word_model.meaning,
            created_at=word_model.created_at
        )
    
    def to_dict(self):
        return {
            'id': self.id,
            'word': self.word,
            'meaning': self.meaning,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }