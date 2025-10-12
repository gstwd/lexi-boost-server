import os
import sys
import tempfile

import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import create_app
from app.data.models import StudyRecord, Word
from app.extensions import db

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    test_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SECRET_KEY': 'test-secret-key'
    }

    app = create_app('testing')
    app.config.update(test_config)

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def sample_word(app):
    with app.app_context():
        word = Word(word="hello", meaning="a greeting")
        db.session.add(word)
        db.session.commit()
        word_id = word.id
        return word_id

@pytest.fixture
def sample_study_record(app, sample_word):
    with app.app_context():
        record = StudyRecord(word_id=sample_word, status="learning")
        db.session.add(record)
        db.session.commit()
        record_id = record.id
        return record_id
