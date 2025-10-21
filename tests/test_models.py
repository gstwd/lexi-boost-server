from app.data.models import WordRecord, StudyRecord
from app.extensions import db

class TestWordModel:
    def test_word_creation(self, app):
        with app.app_context():
            word = WordRecord(word="test", meaning="a test word")
            db.session.add(word)
            db.session.commit()

            assert word.id is not None
            assert word.word == "test"
            assert word.meaning == "a test word"
            assert word.create_time is not None

    def test_word_to_dict(self, app, sample_word):
        with app.app_context():
            # Get the word from database using the word_id
            word = db.session.get(WordRecord, sample_word)
            word_dict = word.to_dict()
            assert 'id' in word_dict
            assert 'word' in word_dict
            assert 'meaning' in word_dict
            assert 'create_time' in word_dict

class TestStudyRecordModel:
    def test_study_record_creation(self, app, sample_word):
        with app.app_context():
            record = StudyRecord(word_id=sample_word, status="learning")
            db.session.add(record)
            db.session.commit()

            assert record.id is not None
            assert record.word_id == sample_word
            assert record.status == "learning"
            assert record.create_time is not None
            assert record.update_time is not None

    def test_study_record_to_dict(self, app, sample_study_record):
        with app.app_context():
            # Get the record from database using the record_id
            record = db.session.get(StudyRecord, sample_study_record)
            record_dict = record.to_dict()
            assert 'id' in record_dict
            assert 'word_id' in record_dict
            assert 'status' in record_dict
            assert 'create_time' in record_dict
            assert 'update_time' in record_dict

    def test_word_study_record_relationship(self, app, sample_word):
        with app.app_context():
            record = StudyRecord(word_id=sample_word, status="learning")
            db.session.add(record)
            db.session.commit()

            # Get the word from database to check relationships
            word = db.session.get(WordRecord, sample_word)
            assert len(word.study_records) == 1
            assert word.study_records[0].status == "learning"
