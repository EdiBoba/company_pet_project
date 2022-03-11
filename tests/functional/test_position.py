import pytest

from depart.db import tables


@pytest.mark.parametrize(
    "position_name", (
        "HR",
        "ADMIN",
        "PM",
    )
)
def test_fetch_position(api, db_session, position_name):
    position = tables.Position(name=position_name)
    db_session.add(position)
    db_session.commit()
    db_session.refresh(position)

    response = api.get("/positions")
    assert response.ok
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == str(position.id)
    assert body[0]["name"] == position_name
