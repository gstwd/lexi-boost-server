from typing import List

from sqlalchemy.exc import IntegrityError

from app.business.dto import WordDTO, WordEntryDTO
from app.data.repositories import WordRecordRepository, WordEntryRepository
from app.exceptions import APIException


class WordService:
    def __init__(self, word_record_repository: WordRecordRepository, word_entry_repository: WordEntryRepository):
        self.word_record_repository = word_record_repository
        self.word_entry_repository = word_entry_repository

    def get_all_words(self) -> List[WordDTO]:
        words = self.word_record_repository.get_all()
        return [WordDTO.from_model(word) for word in words]

    def get_word_by_id(self, word_id: int) -> WordDTO:
        word = self.word_record_repository.get_by_id(word_id)
        if not word:
            raise APIException(
                f"WordRecord with id {word_id} not found",
                error_code=1002,
            )
        return WordDTO.from_model(word)

    def create_word(self, **kwargs) -> WordDTO:
        try:
            new_word = self.word_record_repository.create(**kwargs)
        except IntegrityError as exc:
            raise APIException(
                "WordRecord already exists",
                error_code=1005,
            ) from exc
        return WordDTO.from_model(new_word)

    def update_word(self, word_id: int, **kwargs) -> WordDTO:
        updated_word = self.word_record_repository.update(word_id, **kwargs)
        if not updated_word:
            raise APIException(
                f"WordRecord with id {word_id} not found",
                error_code=1002,
            )
        return WordDTO.from_model(updated_word)

    def delete_word(self, word_id: int) -> bool:
        success = self.word_record_repository.delete(word_id)
        if not success:
            raise APIException(
                f"WordRecord with id {word_id} not found",
                error_code=1002,
            )
        return success

    def check_duplication(self, word):
        pass

    def search_word_entries(self, query, page, limit) -> List[WordEntryDTO]:
        words = self.word_entry_repository.search_word_entries(query, page, limit)
        return [WordEntryDTO.from_model(word) for word in words]
