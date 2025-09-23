from flask import Blueprint, request, jsonify
from app.business.services import StudyService
from app.presentation.schemas import validate_json, StudyRecordSchema, SchemaConverter
from app.exceptions import ValidationError, NotFoundError, DatabaseError

class StudyController:
    def __init__(self, study_service: StudyService):
        self._study_service = study_service
        self.blueprint = Blueprint('study', __name__)
        self._register_routes()
    
    def _register_routes(self):
        self.blueprint.add_url_rule('/study', 'save_study_result', self.save_study_result, methods=['POST'])
        self.blueprint.add_url_rule('/study/<int:word_id>', 'get_study_record', self.get_study_record, methods=['GET'])
    
    def success_response(self, data=None, message="success"):
        return jsonify({
            'code': 0,
            'message': message,
            'data': data
        })
    
    @validate_json(StudyRecordSchema)
    def save_study_result(self):
        """保存学习结果"""
        try:
            data = request.validated_data
            word_id = data['word_id']
            status = data['status']

            study_record = self._study_service.save_study_result(word_id, status)

            if study_record:
                study_data = SchemaConverter.study_record_to_response(study_record)
                message = "Study record updated" if study_record.id else "Study record created"
                return self.success_response(study_data, message)

        except NotFoundError as e:
            raise e
        except Exception as e:
            raise DatabaseError(f"Failed to save study result: {str(e)}")
    
    def get_study_record(self, word_id):
        """获取学习记录"""
        try:
            record = self._study_service.get_study_record_by_word_id(word_id)
            record_data = SchemaConverter.study_record_to_response(record)
            return self.success_response(record_data)
        except NotFoundError as e:
            raise e
        except Exception as e:
            raise DatabaseError(f"Failed to fetch study record: {str(e)}")