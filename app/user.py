class User:
    """A base class for all users in the system."""
    def __init__(self, name, user_id, hash, type_name):
        self.id = user_id
        self.name = name
        self.hash = hash
        self.type_name = type_name