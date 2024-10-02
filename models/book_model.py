class Book:
    def __init__(self, id, title , author_id  , author_name,  count=1, is_rentable=True, language=None ,  ):
        self.id = str(id)
        self.title = title
        self.count = count
        self.is_rentable = is_rentable
        self.language = language
        self.author_id = author_id
        self.author_name = author_name

    @classmethod
    def from_db_record(cls, record):
        return cls(
            id=str(record.get('id')),
            title=record.get('title'),
            count=record.get('count', 1),
            is_rentable=record.get('is_rentable', True),
            language=record.get('language'),
            author_id=record.get('author_id'),
            author_name=record.get('author_name'),
        )

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'count': self.count,
            'is_rentable': self.is_rentable,
            'language': self.language,
            'author_id': self.author_id,
            'author_name': self.author_name,
        }

