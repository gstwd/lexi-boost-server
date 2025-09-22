from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Word, StudyRecord
from app.exceptions import ValidationError, NotFoundError, DatabaseError
from app.validators import validate_json, StudyRecordSchema

words_bp = Blueprint('words', __name__)

def success_response(data=None, message="success"):
    return jsonify({
        'code': 0,
        'message': message,
        'data': data
    })

@words_bp.route('/words', methods=['GET'])
def get_words():
    try:
        words = Word.query.all()
        words_data = [word.to_dict() for word in words]
        return success_response(words_data)
    except Exception as e:
        raise DatabaseError(f"Failed to fetch words: {str(e)}")

@words_bp.route('/study', methods=['POST'])
@validate_json(StudyRecordSchema)
def save_study_result():
    try:
        data = request.validated_data
        word_id = data['word_id']
        status = data['status']

        # Check if word exists
        word = Word.query.get(word_id)
        if not word:
            raise NotFoundError("Word not found")

        # Check if study record already exists for this word
        existing_record = StudyRecord.query.filter_by(word_id=word_id).first()

        if existing_record:
            # Update existing record
            existing_record.status = status
            db.session.commit()
            return success_response(existing_record.to_dict(), "Study record updated")
        else:
            # Create new study record
            study_record = StudyRecord(word_id=word_id, status=status)
            db.session.add(study_record)
            db.session.commit()
            return success_response(study_record.to_dict(), "Study record created")

    except Exception as e:
        db.session.rollback()
        if isinstance(e, (ValidationError, NotFoundError)):
            raise e
        raise DatabaseError(f"Failed to save study result: {str(e)}")