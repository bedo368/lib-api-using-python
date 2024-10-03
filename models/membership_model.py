class MembershipType:
    def __init__(self, membership_type_id, type_name, benefits=None):
        self.id = str(membership_type_id)
        self.type_name = type_name
        self.benefits = benefits

    @classmethod
    def from_db_record(cls, record):
        return cls(
            membership_type_id=str(record.get('id')),
            type_name=record.get('type_name'),
            benefits=record.get('benefits')
        )

    def to_dict(self):
        return {
            'id': self.id,
            'type_name': self.type_name,
            'benefits': self.benefits
        }
