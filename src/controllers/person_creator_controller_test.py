import pytest
from src.models.sqlite.entities.people import PeopleTable
from src.models.sqlite.interfaces.people_repository import PeopleRepositoryInterface
from .person_creator_controller import PersonCreatorController

class MockPeopleRepository(PeopleRepositoryInterface):
    def insert_person(self, first_name: str, last_name: str, age: int, pet_id: int) -> None:
        pass

    def get_person(self, person_id: int) -> PeopleTable:
        return PeopleTable(first_name='John', last_name='Doe', age=31, pet_id=1)


def test_create():
    person_info = {
        "first_name": "John",
        "last_name": "Doe",
        "age": 31,
        "pet_id": 1
    }

    controller = PersonCreatorController(MockPeopleRepository())
    response = controller.create(person_info)

    assert response["data"]["type"] == "Person"
    assert response["data"]["count"] == 1
    assert response["data"]["attributes"] == person_info

def test_create_error():
    person_info = {
        "first_name": "John",
        "last_name": "Doe Natanael",
        "age": 31,
        "pet_id": 1
    }

    controller = PersonCreatorController(MockPeopleRepository())

    with pytest.raises(Exception):
        controller.create(person_info)
