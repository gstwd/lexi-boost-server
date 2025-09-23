from abc import ABC, abstractmethod
from typing import List, Optional
from app.data.models import Word

class WordRepositoryInterface(ABC):
    @abstractmethod
    def get_all(self) -> List[Word]:
        pass
    
    @abstractmethod
    def get_by_id(self, word_id: int) -> Optional[Word]:
        pass
    
    @abstractmethod
    def create(self, word: str, meaning: str) -> Word:
        pass
    
    @abstractmethod
    def update(self, word_id: int, **kwargs) -> Optional[Word]:
        pass
    
    @abstractmethod
    def delete(self, word_id: int) -> bool:
        pass