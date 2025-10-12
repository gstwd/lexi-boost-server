from typing import List

from sqlalchemy.exc import IntegrityError

from app.business.dto import WordDTO
from app.data.repositories import WordRepository
from app.exceptions import APIException


class WordService:
    def __init__(self, word_repository: WordRepository):
        self._word_repository = word_repository

    def get_all_words(self) -> List[WordDTO]:
        words = self._word_repository.get_all()
        return [WordDTO.from_model(word) for word in words]

    def get_word_by_id(self, word_id: int) -> WordDTO:
        word = self._word_repository.get_by_id(word_id)
        if not word:
            raise APIException(
                f"Word with id {word_id} not found",
                error_code=1002,
                status_code=404,
            )
        return WordDTO.from_model(word)

    def create_word(self, word: str, meaning: str) -> WordDTO:
        try:
            new_word = self._word_repository.create(word, meaning)
        except IntegrityError as exc:
            raise APIException(
                "Word already exists",
                error_code=1005,
                status_code=409,
            ) from exc
        return WordDTO.from_model(new_word)

    def update_word(self, word_id: int, **kwargs) -> WordDTO:
        updated_word = self._word_repository.update(word_id, **kwargs)
        if not updated_word:
            raise APIException(
                f"Word with id {word_id} not found",
                error_code=1002,
                status_code=404,
            )
        return WordDTO.from_model(updated_word)

    def delete_word(self, word_id: int) -> bool:
        success = self._word_repository.delete(word_id)
        if not success:
            raise APIException(
                f"Word with id {word_id} not found",
                error_code=1002,
                status_code=404,
            )
        return success
