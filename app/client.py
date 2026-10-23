from app.user import User

class ClientUser(User):
    """Represents a staff, inheriting from the base User class."""
    def __init__(self, name, id, hash, type_name="class", donation_history=[]):
        super().__init__(name, id, hash, type_name)
        self.type_name = "client"
        self.id = id
        self.name = name
        self.hash = hash
        self.donation_history = donation_history
