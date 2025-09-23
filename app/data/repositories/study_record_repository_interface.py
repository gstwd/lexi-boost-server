from abc import ABC, abstractmethod
from typing import List, Optional
from app.data.models import StudyRecord

class StudyRecordRepositoryInterface(ABC):
    @abstractmethod
    def get_by_word_id(self, word_id: int) -> Optional[StudyRecord]:
        pass
    
    @abstractmethod
    def create(self, word_id: int, status: str) -> StudyRecord:
        pass
    
    @abstractmethod
    def update(self, record_id: int, **kwargs) -> Optional[StudyRecord]:
        pass
    
    @abstractmethod
    def update_by_word_id(self, word_id: int, status: str) -> Optional[StudyRecord]:
        pass