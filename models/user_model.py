# models.py

from datetime import datetime


class User:
    def __init__(
        self,
        user_id,
        name,
        phone_number,
        email=None,
        address=None,
        membership_type_id=None,
        date_joined=None,
        is_active=True,
        is_admin=False,
    ):
        self.id = str(user_id)
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.address = address
        self.membership_type_id = membership_type_id
        self.date_joined = date_joined or datetime.now().date()
        self.is_active = is_active
        self.is_admin = is_admin

    @classmethod
    def from_db_record(cls, record):
        """
        Create a User instance from a database record.

        :param record: A dictionary representing a user record from the database.
        :return: An instance of User.
        """
        return cls(
            user_id=str(record.get("id")),
            name=record.get("name"),
            phone_number=record.get("phone_number"),
            email=record.get("email"),
            address=record.get("address"),
            membership_type_id=record.get("membership_type_id"),
            date_joined=record.get("date_joined"),
            is_active=record.get("is_active", True),
            is_admin=record.get("is_admin", True),
        )

    def to_dict(self):
        """
        Convert the User instance to a dictionary.

        :return: A dictionary representation of the user.
        """
        return {
            "id": self.id,
            "name": self.name,
            "phone_number": self.phone_number,
            "email": self.email,
            "address": self.address,
            "membership_type_id": self.membership_type_id,
            "date_joined": self.date_joined.isoformat() if self.date_joined else None,
            "is_active": self.is_active,
            "is_admin": self.is_admin,
        }
