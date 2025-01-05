from .person_finder_controller import PersonFinderController

class MockPerson():
    def __init__(self, first_name, last_name, pet_name, pet_type):
        self.first_name = first_name
        self.last_name = last_name
        self.pet_name = pet_name
        self.pet_type = pet_type

class MockPeopleRepository():
    def insert_person(self, first_name: str, last_name: str, age: int, pet_id: int) -> None:
        pass

    def get_person(self, person_id: int) -> MockPerson: # pylint: disable=unused-argument
        return MockPerson(
            first_name='John',
            last_name='Doe',
            pet_name='Buddy',
            pet_type='Dog'
        )



def test_find():
    controller = PersonFinderController(MockPeopleRepository())
    response = controller.find(1)

    expected_response = {
        'data': {
            'type': 'Person',
            'count': 1,
            'attributes': {
                'first_name': 'John',
                'last_name': 'Doe',
                'pet_name': 'Buddy',
                'pet_type': 'Dog'
            }
        }
    }

    assert response == expected_response
