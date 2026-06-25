import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import api.spoonacular_api as spoonacular

#Test 1: get_nutrition returns correct nutrient info
def test_get_nutrition(monkeypatch):
    # Fake search response
    def fake_search(*args, **kwargs):
        class FakeResponse:
            def json(self):
                return {"results": [{"id": 123}]}
        return FakeResponse()

    # Fake nutrition response
    def fake_nutrition(*args, **kwargs):
        class FakeResponse:
            def json(self):
                return {
                    "name": "rice",
                    "nutrition": {
                        "nutrients": [
                            {"name": "Calories", "amount": 200, "unit": "kcal"},
                            {"name": "Protein", "amount": 4, "unit": "g"},
                        ]
                    }
                }
        return FakeResponse()

    #First call returns search, second call returns nutrition
    responses = [fake_search, fake_nutrition]
    monkeypatch.setattr("requests.get", lambda *a, **kw: responses.pop(0)(*a, **kw))

    result = spoonacular.get_nutrition("rice")
    assert result["name"] == "rice"
    assert "Calories" in result["nutrients"]

#Test 2: get_nutrition returns None when ingredient not found
def test_get_nutrition_not_found(monkeypatch):
    def fake_empty(*args, **kwargs):
        class FakeResponse:
            def json(self):
                return {"results": []}
        return FakeResponse()

    monkeypatch.setattr("requests.get", fake_empty)

    result = spoonacular.get_nutrition("xyzabc")
    assert result is None

#Test 3: find_recipes_by_ingredients returns first recipe
def test_find_recipes_by_ingredients(monkeypatch):
    def fake_response(*args, **kwargs):
        class FakeResponse:
            status_code = 200
            def json(self):
                return [{"id": 456, "title": "Egg Fried Rice"}]
        return FakeResponse()

    monkeypatch.setattr("requests.get", fake_response)

    result = spoonacular.find_recipes_by_ingredients(["eggs", "rice"])
    assert result["id"] == 456
    assert result["title"] == "Egg Fried Rice"