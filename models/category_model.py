class Category:
    def __init__(self, id, name, description=None):
        self.id = id
        self.name = name
        self.description = description

    @classmethod
    def from_db_record(cls, record):
        return cls(
            id=record.get('id'),
            name=record.get('name'),
            description=record.get('description')
        )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }