from typing import List
from app.data.repositories import WordRepositoryInterface
from app.business.dto import WordDTO
from app.exceptions import NotFoundError

class WordService:
    def __init__(self, word_repository: WordRepositoryInterface):
        self._word_repository = word_repository
    
    def get_all_words(self) -> List[WordDTO]:
        """获取所有单词"""
        words = self._word_repository.get_all()
        return [WordDTO.from_model(word) for word in words]
    
    def get_word_by_id(self, word_id: int) -> WordDTO:
        """根据ID获取单词"""
        word = self._word_repository.get_by_id(word_id)
        if not word:
            raise NotFoundError(f"Word with id {word_id} not found")
        return WordDTO.from_model(word)
    
    def create_word(self, word: str, meaning: str) -> WordDTO:
        """创建新单词"""
        new_word = self._word_repository.create(word, meaning)
        return WordDTO.from_model(new_word)
    
    def update_word(self, word_id: int, **kwargs) -> WordDTO:
        """更新单词"""
        updated_word = self._word_repository.update(word_id, **kwargs)
        if not updated_word:
            raise NotFoundError(f"Word with id {word_id} not found")
        return WordDTO.from_model(updated_word)
    
    def delete_word(self, word_id: int) -> bool:
        """删除单词"""
        success = self._word_repository.delete(word_id)
        if not success:
            raise NotFoundError(f"Word with id {word_id} not found")
        return success