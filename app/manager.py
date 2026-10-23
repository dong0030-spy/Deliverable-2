import json
import datetime
import uuid
import csv
import logging
import re
import bcrypt
from app.staff import StaffUser
from app.volunteer import VolunteerUser
from app.client import ClientUser
from app.food_donation import Food, Donation

class Table4AllManager:
    """The main controller for all business logic and data handling."""
    def __init__(self, data_path="data/data.json"):
        self.data_path = data_path
        self.staffs = [
            StaffUser("teststaff123", "s0000001", self.encrypt_password("teststaff123").decode("utf-8"))
        ]
        self.volunteers = [
            VolunteerUser("testvol123", "v0000001", self.encrypt_password("teststaff123").decode("utf-8"))
        ]
        self.clients = []
        self.storage = []
        self.pending_donations = []
        self.approved_donations = []
        self.completed_donations = []
        self.food_id_count = 1
        self.donation_id_count = 1
        self._load_data()

    def _load_data(self):
        """Loads data from the JSON file and populates the object lists."""
        try:
            with open(self.data_path, 'r') as f:
                data = json.load(f)
                self.staffs = [StaffUser(**s) for s in data["staffs"]]
                self.volunteers = [VolunteerUser(**v) for v in data["volunteers"]]
                self.clients = [ClientUser(**c) for c in data["clients"]]
                self.storage = [Food(**f) for f in data["storage"]]
                self.pending_donations = [Donation(**d) for d in data["pending_donations"]]
                self.approved_donations = [Donation(**d) for d in data["approved_donations"]]
                self.completed_donations = [Donation(**d) for d in data["completed_donations"]]
                self.food_id_count = data["food_id_count"]
                self.donation_id_count = data["donation_id_count"]
                print("Data successfully loaded.")
        except FileNotFoundError:
            print("Data file not found. Starting with a clean state.")

    
    def _save_data(self):
        """Converts object lists back to dictionaries and saves to JSON."""
        data_to_save = {
            "staffs": [s.__dict__ for s in self.staffs],
            "volunteers": [v.__dict__ for v in self.volunteers],
            "clients": [c.__dict__ for c in self.clients],
            "storage": [f.__dict__ for f in self.storage],
            "pending_donations": [d.__dict__ for d in self.pending_donations],
            "approved_donations": [d.__dict__ for d in self.approved_donations],
            "completed_donations": [d.__dict__ for d in self.completed_donations],
            "food_id_count": self.food_id_count,
            "donation_id_count": self.donation_id_count
        }
        with open(self.data_path, 'w') as f:
            json.dump(data_to_save, f, indent=4)

    def get_client(self, term):
        for c in self.clients:
            if c.id == term or c.name == term:
                return c
        return None

    def get_staff(self, term):
        for s in self.staffs:
            if s.id == term or s.name == term:
                return s
        return None

    def get_volunteer(self, term):
        for v in self.volunteers:
            if v.id == term or v.name == term:
                return v
        return None

    def get_food(self, term):
        for f in self.storage:
            if f.id == term or f.name == term:
                return f
        return None

    def get_pending_donation(self, term):
        for d in self.pending_donations:
            if d.id == term or d.donor_id == term:
                return d
    def get_approved_donation(self, term):
        for d in self.approved_donations:
            if d.id == term or d.donor_id == term:
                return d
                
        return None
    def get_pending_food(self, term):
        for f in self.storage:
            if f.pending.get(term):
                return f
        return None

    def search_food(self, term):
        results = []
        if term == "":
            return results
        for f in self.storage:
            if re.search(term.lower(), f.name.lower()):
                results.append(f)
        return results
    
    def generate_id(self, type):
        full_uuid = uuid.uuid4()
        id = full_uuid.hex[:7]
        if type == "client":
            return f"c{id}"
        elif type == "staff":
            return f"s{id}"
        elif type == "volunteer":
            return f"v{id}"
        elif type == "food":
            new_id = f"f{str(self.food_id_count).zfill(7)}"
            self.food_id_count += 1
            return new_id
        elif type == "donation":
            new_id = f"d{str(self.donation_id_count).zfill(7)}"
            self.donation_id_count += 1
            return new_id
        

    def encrypt_password(self, pwd):
        pwd = pwd.encode("utf-8")
        hashed = bcrypt.hashpw(pwd, bcrypt.gensalt())
        return hashed

    def check_password(self, user, pwd):
        return bcrypt.checkpw(pwd.encode("utf-8"), user.hash.encode("utf-8"))

    def register_new_client(self, name, pwd):
        new_client = ClientUser(name, self.generate_id("client"), self.encrypt_password(pwd).decode("utf-8"))
        self.clients.append(new_client)
        self._save_data()
        return new_client

    def register_new_staff(self, name, pwd):
        new_staff = StaffUser(name, self.generate_id("staff"), self.encrypt_password(pwd))
        self.staffs.append(new_staff)
        self._save_data()
        return new_staff

    def register_new_volunteer(self, name, pwd):
        new_volunteer = VolunteerUser(name, self.generate_id("volunteer".type), self.encrypt_password(pwd))
        self.staffs.append(new_volunteer)
        self._save_data()
        return new_volunteer

    def register_new_food(self, name, quantity):
        new_food = Food(name, self.generate_id("food"), quantity)
        self.storage.append(new_food)
        self._save_data()
        return new_food

    def register_donation(self, user_id):
        user = self.get_client(user_id)
        if user:
            new_donation = Donation(self.generate_id("donation"), user_id)
            self.pending_donations.append(new_donation)
            return new_donation
        else:
            print("User ID not found, new donation is not created")

    def approve_donation(self, donation_id):
        donation = self.get_pending_donation(donation_id)
        donation.status = "approved"
        self.approved_donations.append(donation)
        self.pending_donations.remove(donation)
        self._save_data()

    def update_donation(self, donor_id, food_list):
        for food_id, amount in food_list.items():
            food = self.get_food(food_id)
            food.pending[donor_id]["received"] += amount
        self._save_data()

    def complete_donation(self, donation_id):
        donation = self.get_approved_donation(donation_id)
        donation.status = "completed"
        self.completed_donations.append(donation)
        self.approved_donations.remove(donation)
        self._save_data()

    
    





