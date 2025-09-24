from flask import request

from app.business.services import WordService
from app.presentation.schemas import validate_json, WordSchema, SchemaConverter
from .base_controller import BaseController


class WordController(BaseController):
    def __init__(self, word_service: WordService):
        super().__init__(word_service, 'words')
        self._word_service = word_service
    
    def _register_routes(self):
        self.blueprint.add_url_rule('/words', 'get_words', self.get_words, methods=['GET'])
        self.blueprint.add_url_rule('/words', 'create_word', self.create_word, methods=['POST'])
        self.blueprint.add_url_rule('/words/<int:word_id>', 'get_word', self.get_word, methods=['GET'])
        self.blueprint.add_url_rule('/words/<int:word_id>', 'update_word', self.update_word, methods=['PUT'])
        self.blueprint.add_url_rule('/words/<int:word_id>', 'delete_word', self.delete_word, methods=['DELETE'])
    
    def get_words(self):
        """获取所有单词"""
        words = self._word_service.get_all_words()
        words_data = SchemaConverter.words_to_response(words)
        return self.success_response(words_data)
    
    def get_word(self, word_id):
        """根据ID获取单词"""
        word = self._word_service.get_word_by_id(word_id)
        word_data = SchemaConverter.word_to_response(word)
        return self.success_response(word_data)
    
    @validate_json(WordSchema)
    def create_word(self):
        """创建新单词"""
        data = request.validated_data
        word = self._word_service.create_word(data['word'], data['meaning'])
        word_data = SchemaConverter.word_to_response(word)
        return self.success_response(word_data, "Word created successfully")
    
    @validate_json(WordSchema)
    def update_word(self, word_id):
        """更新单词"""
        data = request.validated_data
        word = self._word_service.update_word(word_id, **data)
        word_data = SchemaConverter.word_to_response(word)
        return self.success_response(word_data, "Word updated successfully")
    
    def delete_word(self, word_id):
        """删除单词"""
        self._word_service.delete_word(word_id)
        return self.success_response(None, "Word deleted successfully")