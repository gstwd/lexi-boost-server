from typing import List

from app.data.models import WordEntry


class WordEntryRepository:
    def search_word_entries(self, query, page, page_size)-> List[WordEntry]:
        return WordEntry.query.filter(
            WordEntry.word.ilike(f"%{query}%")  # type: ignore
        ).paginate(
            page=page,
            per_page=page_size,
            error_out=False
        ).items

