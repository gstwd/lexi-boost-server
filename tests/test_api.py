import pytest
import json
from app.models import Word, StudyRecord
from app.extensions import db

class TestWordsAPI:
    def test_get_words_empty(self, client):
        response = client.get('/api/words')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['code'] == 0
        assert data['message'] == 'success'
        assert data['data'] == []

    def test_get_words_with_data(self, client, sample_word):
        response = client.get('/api/words')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['code'] == 0
        assert len(data['data']) == 1
        assert data['data'][0]['word'] == 'hello'
        assert data['data'][0]['meaning'] == 'a greeting'

    def test_save_study_result_new_record(self, client, sample_word):
        payload = {
            'word_id': sample_word.id,
            'status': 'learning'
        }

        response = client.post('/api/study',
                             data=json.dumps(payload),
                             content_type='application/json')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['code'] == 0
        assert data['message'] == 'Study record created'
        assert data['data']['status'] == 'learning'

    def test_save_study_result_update_existing(self, client, sample_study_record):
        payload = {
            'word_id': sample_study_record.word_id,
            'status': 'mastered'
        }

        response = client.post('/api/study',
                             data=json.dumps(payload),
                             content_type='application/json')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['code'] == 0
        assert data['message'] == 'Study record updated'
        assert data['data']['status'] == 'mastered'

    def test_save_study_result_invalid_word(self, client):
        payload = {
            'word_id': 999,
            'status': 'learning'
        }

        response = client.post('/api/study',
                             data=json.dumps(payload),
                             content_type='application/json')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['code'] == 1
        assert 'Word not found' in data['message']

    def test_save_study_result_missing_data(self, client):
        payload = {
            'word_id': 1
            # missing status
        }

        response = client.post('/api/study',
                             data=json.dumps(payload),
                             content_type='application/json')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['code'] == 1
        assert 'required' in data['message']

    def test_save_study_result_no_json(self, client):
        response = client.post('/api/study')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['code'] == 1
        assert 'No data provided' in data['message']