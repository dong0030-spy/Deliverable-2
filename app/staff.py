from app.user import User

class StaffUser(User):
    """Represents a staff, inheriting from the base User class."""
    def __init__(self, name, id, hash, type_name="staff"):
        super().__init__(name, id, hash, type_name)
        self.type_name = "staff"
        self.id = id
        self.name = name
        self.hash = hash

    