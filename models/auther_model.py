class Author:
    def __init__(self, id, name, bio=None):
        self.id = id
        self.name = name
        self.bio = bio

    @classmethod
    def from_db_record(cls, record):
        return cls(
            id=record.get('id'),
            name=record.get('name'),
            bio=record.get('bio')
        )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'bio': self.bio
        }
