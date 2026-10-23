import pytest
import os
from app.manager import Table4AllManager


@pytest.fixture
def manager():
    """Create a fresh manager for each test."""
    test_file = "test_data.json"
        # ARRANGE: Ensure no old test file exists.
    if os.path.exists(test_file):
        os.remove(test_file)
    return Table4AllManager(data_path=test_file)


# ==========================================
# FR-01: Register donation offers
# ==========================================

def test_register_donation_valid_client(manager):
    client = manager.register_new_client("Test Donor", "TestPassword123")
    donation = manager.register_donation(client.id)
    assert donation is not None
    assert donation in manager.pending_donations


def test_register_donation_invalid_client(manager):
    result = manager.register_donation("c9999999")
    assert result is None
    assert len(manager.pending_donations) == 0

def test_register_donation_with_no_details(manager):
    result = manager.register_donation("")
    assert result is None

def test_multiple_donations_have_unique_ids(manager):
    client = manager.register_new_client(
        "Test Donor", "TestPassword123"
    )
    donation1 = manager.register_donation(client.id)
    donation2 = manager.register_donation(client.id)
    assert donation1.id != donation2.id


# ==========================================
# FR-02: Review and record donations
# ==========================================

def test_approve_pending_donation(manager):
    client = manager.register_new_client("Test Donor", "TestPassword123")
    donation = manager.register_donation(client.id)
    manager.approve_donation(donation.id)
    assert donation.status == "approved"
    assert donation in manager.approved_donations
    assert donation not in manager.pending_donations

# ==========================================
# FR-03: Search recorded food
# ==========================================

def test_get_food_by_name(manager):
    food = manager.register_new_food("Rice", 100)
    result = manager.get_food("Rice")
    assert result == food


def test_get_nonexistent_food(manager):
    result = manager.get_food("Unknown Food")
    assert result is None


def test_search_food_case_insensitive(manager):
    manager.register_new_food("Salmon", 100)
    results = manager.search_food("Salmon")
    assert len(results) == 1
    assert results[0].name == "Salmon"


def test_search_food_empty_term(manager):
    manager.register_new_food("Rice", 100)
    results = manager.search_food("")
    assert results == []


def test_search_food_no_match(manager):
    manager.register_new_food("Rice", 100)
    results = manager.search_food("Bread")
    assert results == []

# ==========================================
# FR-04: View current stock
# ==========================================

def test_register_new_food(manager):
    food = manager.register_new_food("Rice", 100)
    assert food in manager.storage
    assert food.name == "Rice"
    assert food.quantity == 100
