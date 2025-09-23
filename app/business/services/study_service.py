from app.data.repositories import WordRepositoryInterface, StudyRecordRepositoryInterface
from app.business.dto import StudyRecordDTO, WordDTO
from app.exceptions import NotFoundError

class StudyService:
    def __init__(self, word_repository: WordRepositoryInterface, study_record_repository: StudyRecordRepositoryInterface):
        self._word_repository = word_repository
        self._study_record_repository = study_record_repository
    
    def save_study_result(self, word_id: int, status: str) -> StudyRecordDTO:
        """保存学习结果"""
        # 检查单词是否存在
        word = self._word_repository.get_by_id(word_id)
        if not word:
            raise NotFoundError("Word not found")
        
        # 检查是否已有学习记录
        existing_record = self._study_record_repository.get_by_word_id(word_id)
        
        if existing_record:
            # 更新现有记录
            updated_record = self._study_record_repository.update_by_word_id(word_id, status)
            return StudyRecordDTO.from_model(updated_record)
        else:
            # 创建新记录
            new_record = self._study_record_repository.create(word_id, status)
            return StudyRecordDTO.from_model(new_record)
    
    def get_study_record_by_word_id(self, word_id: int) -> StudyRecordDTO:
        """根据单词ID获取学习记录"""
        record = self._study_record_repository.get_by_word_id(word_id)
        if not record:
            raise NotFoundError(f"Study record for word {word_id} not found")
        return StudyRecordDTO.from_model(record)