from app.business.dto import StudyRecordDTO
from app.data.repositories import StudyRecordRepository, WordRepository
from app.exceptions import APIException


class StudyService:
    def __init__(self, word_repository: WordRepository, study_record_repository: StudyRecordRepository):
        self._word_repository = word_repository
        self._study_record_repository = study_record_repository

    def save_study_result(self, word_id: int, status: str) -> StudyRecordDTO:
        word = self._word_repository.get_by_id(word_id)
        if not word:
            raise APIException("Word not found", error_code=1002, status_code=404)

        existing_record = self._study_record_repository.get_by_word_id(word_id)

        if existing_record:
            updated_record = self._study_record_repository.update_by_word_id(word_id, status)
            return StudyRecordDTO.from_model(updated_record)

        new_record = self._study_record_repository.create(word_id, status)
        return StudyRecordDTO.from_model(new_record)

    def get_study_record_by_word_id(self, word_id: int) -> StudyRecordDTO:
        record = self._study_record_repository.get_by_word_id(word_id)
        if not record:
            raise APIException(
                f"Study record for word {word_id} not found",
                error_code=1002,
                status_code=404,
            )
        return StudyRecordDTO.from_model(record)
