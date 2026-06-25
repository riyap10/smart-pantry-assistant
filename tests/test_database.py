import sqlite3
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import database.database as db

TEST_DB = "test_pantry.db"

@pytest.fixture(autouse=True)
def setup_test_db(monkeypatch):
    # Point connect_db to a test database file instead of pantry.db
    monkeypatch.setattr(db, "connect_db", lambda: sqlite3.connect(TEST_DB))

    # Create the tables
    db.create_table()
    db.create_recipe_table()

    yield

    # Delete the test database after each test
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def test_add_ingredient():
    db.add_ingredient("eggs", 6, "06-30-2026")
    pantry = db.view_pantry()
    assert len(pantry) == 1
    assert pantry[0][1] == "eggs"
    assert pantry[0][2] == 6

def test_view_pantry():
    db.add_ingredient("rice", 2, "10-18-2026")
    db.add_ingredient("chicken", 1, "03-15-2027")
    pantry = db.view_pantry()
    assert len(pantry) == 2

def test_save_recipe():
    db.save_recipe("Chicken and Rice Soup")
    recipes = db.view_recipes()
    assert len(recipes) == 1
    assert recipes[0][1] == "Chicken and Rice Soup"