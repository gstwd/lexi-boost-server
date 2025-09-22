from flask_restx import Api, Resource, fields
from flask import Blueprint

api_bp = Blueprint('api', __name__)
api = Api(
    api_bp,
    version='1.0',
    title='Lexi Boost API',
    description='Vocabulary learning backend API',
    doc='/docs/'
)

# Define namespaces
ns_words = api.namespace('words', description='Word operations')
ns_study = api.namespace('study', description='Study record operations')

# Define models for documentation
word_model = api.model('Word', {
    'id': fields.Integer(readonly=True, description='Word ID'),
    'word': fields.String(required=True, description='The word'),
    'meaning': fields.String(required=True, description='Word meaning'),
    'created_at': fields.DateTime(readonly=True, description='Creation timestamp')
})

study_record_model = api.model('StudyRecord', {
    'id': fields.Integer(readonly=True, description='Record ID'),
    'word_id': fields.Integer(required=True, description='Word ID'),
    'status': fields.String(required=True, description='Study status',
                          enum=['learning', 'mastered', 'review', 'difficult']),
    'created_at': fields.DateTime(readonly=True, description='Creation timestamp'),
    'updated_at': fields.DateTime(readonly=True, description='Update timestamp')
})

study_input_model = api.model('StudyInput', {
    'word_id': fields.Integer(required=True, description='Word ID'),
    'status': fields.String(required=True, description='Study status',
                          enum=['learning', 'mastered', 'review', 'difficult'])
})

response_model = api.model('Response', {
    'code': fields.Integer(description='Response code (0 for success)'),
    'message': fields.String(description='Response message'),
    'data': fields.Raw(description='Response data')
})

# API Resources
@ns_words.route('/')
class WordList(Resource):
    @ns_words.doc('get_words')
    @ns_words.marshal_with(response_model)
    def get(self):
        """Get all words"""
        from app.routes.words import get_words
        return get_words()

@ns_study.route('/')
class StudyRecord(Resource):
    @ns_study.doc('save_study_result')
    @ns_study.expect(study_input_model)
    @ns_study.marshal_with(response_model)
    def post(self):
        """Save study result"""
        from app.routes.words import save_study_result
        return save_study_result()