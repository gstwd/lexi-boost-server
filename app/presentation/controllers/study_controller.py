from flask import request

from app.business.services import StudyService
from app.presentation.schemas import validate_json, StudyRecordSchema, SchemaConverter
from .base_controller import BaseController


class StudyController(BaseController):
    def __init__(self, study_service: StudyService):
        super().__init__(study_service, 'study')
        self._study_service = study_service
    
    def _register_routes(self):
        self.blueprint.add_url_rule('/study', 'save_study_result', self.save_study_result, methods=['POST'])
        self.blueprint.add_url_rule('/study/<int:word_id>', 'get_study_record', self.get_study_record, methods=['GET'])
    
    @validate_json(StudyRecordSchema)
    def save_study_result(self):
        """保存学习结果"""
        data = request.validated_data
        word_id = data['word_id']
        status = data['status']

        study_record = self._study_service.save_study_result(word_id, status)

        if study_record:
            study_data = SchemaConverter.study_record_to_response(study_record)
            message = "Study record updated" if study_record.id else "Study record created"
            return self.success_response(study_data, message)
    
    def get_study_record(self, word_id):
        """获取学习记录"""
        record = self._study_service.get_study_record_by_word_id(word_id)
        record_data = SchemaConverter.study_record_to_response(record)
        return self.success_response(record_data)