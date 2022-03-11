from datetime import datetime
from uuid import UUID

from depart.dto import Position
from depart.dto import Worker


def test_worker_serialize_json(mocker):
    position = Position(
        id=UUID('875956ce-9b1a-11ec-ae60-d8c0a60f59cc'),
        name="HR",
        created_at=datetime(2020, 11, 10),
        updated_at=datetime(2020, 11, 10),
    )

    worker = Worker(
        id=UUID('875956ce-9b1a-11ec-ae60-d8c0a60f59cc'),
        surname="Ivanov",
        name="Vasya",
        position=position,
    )

    assert worker.dict() == {
        "id": UUID("875956ce-9b1a-11ec-ae60-d8c0a60f59cc"),
        "surname": "Ivanov",
        "name": "Vasya",
        "position": {
            "id": UUID("875956ce-9b1a-11ec-ae60-d8c0a60f59cc"),
            "name": "HR",
            "created_at": datetime(2020, 11, 10),
            "updated_at": datetime(2020, 11, 10),
        }
    }

    mocked = mocker.patch("pydantic.BaseModel.dict")

    worker.dict()

    assert mocked.called
