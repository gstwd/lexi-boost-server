from flask import Blueprint, request, jsonify
from app.business.services import WordService
from app.presentation.schemas import validate_json, WordSchema, SchemaConverter
from app.exceptions import ValidationError, NotFoundError, DatabaseError

class WordController:
    def __init__(self, word_service: WordService):
        self._word_service = word_service
        self.blueprint = Blueprint('words', __name__)
        self._register_routes()
    
    def _register_routes(self):
        self.blueprint.add_url_rule('/words', 'get_words', self.get_words, methods=['GET'])
        self.blueprint.add_url_rule('/words', 'create_word', self.create_word, methods=['POST'])
        self.blueprint.add_url_rule('/words/<int:word_id>', 'get_word', self.get_word, methods=['GET'])
        self.blueprint.add_url_rule('/words/<int:word_id>', 'update_word', self.update_word, methods=['PUT'])
        self.blueprint.add_url_rule('/words/<int:word_id>', 'delete_word', self.delete_word, methods=['DELETE'])
    
    def success_response(self, data=None, message="success"):
        return jsonify({
            'code': 0,
            'message': message,
            'data': data
        })
    
    def get_words(self):
        """获取所有单词"""
        try:
            words = self._word_service.get_all_words()
            words_data = SchemaConverter.words_to_response(words)
            return self.success_response(words_data)
        except Exception as e:
            raise DatabaseError(f"Failed to fetch words: {str(e)}")
    
    def get_word(self, word_id):
        """根据ID获取单词"""
        try:
            word = self._word_service.get_word_by_id(word_id)
            word_data = SchemaConverter.word_to_response(word)
            return self.success_response(word_data)
        except NotFoundError as e:
            raise e
        except Exception as e:
            raise DatabaseError(f"Failed to fetch word: {str(e)}")
    
    @validate_json(WordSchema)
    def create_word(self):
        """创建新单词"""
        try:
            data = request.validated_data
            word = self._word_service.create_word(data['word'], data['meaning'])
            word_data = SchemaConverter.word_to_response(word)
            return self.success_response(word_data, "Word created successfully")
        except Exception as e:
            raise DatabaseError(f"Failed to create word: {str(e)}")
    
    @validate_json(WordSchema)
    def update_word(self, word_id):
        """更新单词"""
        try:
            data = request.validated_data
            word = self._word_service.update_word(word_id, **data)
            word_data = SchemaConverter.word_to_response(word)
            return self.success_response(word_data, "Word updated successfully")
        except NotFoundError as e:
            raise e
        except Exception as e:
            raise DatabaseError(f"Failed to update word: {str(e)}")
    
    def delete_word(self, word_id):
        """删除单词"""
        try:
            self._word_service.delete_word(word_id)
            return self.success_response(None, "Word deleted successfully")
        except NotFoundError as e:
            raise e
        except Exception as e:
            raise DatabaseError(f"Failed to delete word: {str(e)}")