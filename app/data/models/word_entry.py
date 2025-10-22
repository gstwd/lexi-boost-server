from sqlalchemy import Column, Integer, String, Text

from app.extensions import db


class WordEntry(db.Model):
    __tablename__ = 'stardict'

    id = Column(Integer, primary_key=True)
    word = Column(String(255), nullable=True)
    phonetic = Column(String(255), nullable=True)
    definition = Column(Text, nullable=True)
    translation = Column(Text, nullable=True)
    pos = Column(String(255), nullable=True)
    collins = Column(String(255), nullable=True)
    oxford = Column(String(255), nullable=True)
    tag = Column(String(255), nullable=True)
    bnc = Column(String(255), nullable=True)
    frq = Column(String(255), nullable=True)
    exchange = Column(String(255), nullable=True)
    detail = Column(Text, nullable=True)
    audio = Column(String(255), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'word': self.word,
            'phonetic': self.phonetic,
            'definition': self.definition,
            'translation': self.translation,
            'pos': self.pos,
            'collins': self.collins,
            'oxford': self.oxford,
            'tag': self.tag,
            'bnc': self.bnc,
            'frq': self.frq,
            'exchange': self.exchange,
            'detail': self.detail,
            'audio': self.audio
        }
