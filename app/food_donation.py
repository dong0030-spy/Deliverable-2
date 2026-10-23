import datetime

class Food:
    """Stores each food's information such as name, quantity"""
    def __init__(self, name, id, quantity=0, pending={}, history={}):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.pending = pending
        self.history = history

    def add_donation(self, manager, donor_id, info):
        self.pending[donor_id] = info
        manager._save_data()

class Donation:
    """Stores each donation's information such as food types"""
    def __init__(self, id, donor_id, donation_list=[], remarks="", pickup_details={}, timestamp=datetime.datetime.now().isoformat(), status="pending"):
        self.id = id
        self.donor_id = donor_id
        self.donation_list = donation_list
        self.remarks = remarks
        self.pickup_details = pickup_details
        self.timestamp = timestamp
        self.status = status

    def add_items(self, manager, donations, remarks):
        self.donation_list = donations
        self.remarks = remarks
        manager._save_data()

