class Category:
    def __init__(self, category_id, name, description=None):
        self.id = str(category_id)
        self.name = name
        self.description = description

    @classmethod
    def from_db_record(cls, record):
        return cls(
            category_id=str(record.get("id")),
            name=record.get("name"),
            description=record.get("description"),
        )

    def to_dict(self):
        return {"id": self.id, "name": self.name, "description": self.description}
