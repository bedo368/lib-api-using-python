class Rent:
    def __init__(self, rent_id, user_id, book_id, rent_date, due_date, return_date=None, status='Rented', fine=0.00):
        self.id = str(rent_id)
        self.user_id = user_id
        self.book_id = book_id
        self.rent_date = rent_date
        self.due_date = due_date
        self.return_date = return_date
        self.status = status
        self.fine = fine

    @classmethod
    def from_db_record(cls, record):
        return cls(
            rent_id=str(record.get('id')),
            user_id=record.get('user_id'),
            book_id=record.get('book_id'),
            rent_date=record.get('rent_date'),
            due_date=record.get('due_date'),
            return_date=record.get('return_date'),
            status=record.get('status'),
            fine=record.get('fine', 0.00)
        )

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'book_id': self.book_id,
            'rent_date': self.rent_date.isoformat() if self.rent_date else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'return_date': self.return_date.isoformat() if self.return_date else None,
            'status': self.status,
            'fine': float(self.fine)
        }