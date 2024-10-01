class Book:
    def __init__(self, id, title, isbn, count=1, is_rentable=True, publication_year=None, publisher=None, language=None):
        self.id = id
        self.title = title
        self.isbn = isbn
        self.count = count
        self.is_rentable = is_rentable
        self.publication_year = publication_year
        self.publisher = publisher
        self.language = language

    @classmethod
    def from_db_record(cls, record):
        return cls(
            id=record.get('id'),
            title=record.get('title'),
            isbn=record.get('isbn'),
            count=record.get('count', 1),
            is_rentable=record.get('is_rentable', True),
            publication_year=record.get('publication_year'),
            publisher=record.get('publisher'),
            language=record.get('language')
        )

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'isbn': self.isbn,
            'count': self.count,
            'is_rentable': self.is_rentable,
            'publication_year': self.publication_year,
            'publisher': self.publisher,
            'language': self.language
        }

