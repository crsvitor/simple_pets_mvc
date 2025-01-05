from unittest import mock
import pytest
from sqlalchemy.orm.exc import StaleDataError
from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from src.models.sqlite.entities.people import PeopleTable
from src.models.sqlite.entities.pets import PetsTable
from .people_repository import PeopleRepository

class MockConnection:
    def __init__(self) -> None:
        self.session = UnifiedAlchemyMagicMock(
            data=[
                (
                    [mock.call.query(PeopleTable)], # query
                    [
                        PeopleTable(first_name='John', last_name='Doe', age='33', pet_id=1),
                    ], # result
                ),
                (
                    [
                        mock.call.query(PeopleTable)
                            .outerjoin(PetsTable, PetsTable.id == PeopleTable.pet_id)
                            .filter(PeopleTable.id == 0)
                            .with_entities(
                                PeopleTable.first_name,
                                PeopleTable.last_name,
                                PetsTable.name.label("pet_name"),
                                PetsTable.type.label("pet_type")
                            )
                            .one()
                    ], # query
                    [
                        {
                            "first_name": "John",
                            "last_name": "Doe",
                            "pet_name": "Buddy",
                            "pet_type": "Dog",
                        }
                    ],
                )
            ]
        )

    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): pass

class MockConnectionException:
    def __init__(self) -> None:
        self.session = UnifiedAlchemyMagicMock()
        self.session.query.side_effect = self.__raise_exception
        self.session.add.side_effect = self.__raise_exception

    def __raise_exception(self, *args, **kwargs):
        raise StaleDataError('data error exception')

    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): pass


def test_insert_person():
    mock_connection = MockConnection()
    repo = PeopleRepository(mock_connection)
    repo.insert_person(
        first_name='Jane',
        last_name='Doe',
        age='32',
        pet_id=1
    )

    mock_connection.session.add.assert_called_once()
    mock_connection.session.commit.assert_called_once()

def test_insert_person_error():
    mock_connection = MockConnectionException()
    repo = PeopleRepository(mock_connection)

    with pytest.raises(Exception):
        repo.insert_person(
            first_name='Jane',
            last_name='Doe',
            age=32,
        pet_id=1
        )

    mock_connection.session.add.assert_called_once()
    mock_connection.session.commit.assert_not_called()
    mock_connection.session.rollback.assert_called_once()

def test_get_person():
    mock_connection = MockConnection()
    repo = PeopleRepository(mock_connection)
    repo.get_person(person_id=0)

    mock_connection.session.query.assert_called_once()
    mock_connection.session.outerjoin.assert_called_once()
    # mock_connection.session.filter.assert_called_once() # need to mock filter and so on
    # mock_connection.session.with_entities.assert_called_once()
    # mock_connection.session.one.assert_called_once()

def test_get_person_error():
    mock_connection = MockConnectionException()
    repo = PeopleRepository(mock_connection)

    with pytest.raises(Exception):
        repo.get_person(person_id=0)

    mock_connection.session.query.assert_called_once()
    mock_connection.session.outerjoin.not_called()
