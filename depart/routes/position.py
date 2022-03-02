from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from depart import dto
from depart.db.session import db_session, Session
from depart.db import tables

router = APIRouter(tags=["positions"])


@router.get("/positions", response_model=list[dto.Position])
def fetch_positions(
    db: Session = Depends(db_session)
) -> list[dto.Position]:
    result = db.query(tables.Position).all()
    return result


@router.post("/positions", status_code=201)
def create_position(
    new_position: dto.Position.New,
    db: Session = Depends(db_session)
) -> dto.Position:
    position = tables.Position(**new_position.dict())
    db.add(position)
    db.commit()
    db.refresh(position)
    return position


@router.get("/positions/{position_id}")
def fetch_position(
    position_id: UUID,
    db: Session = Depends(db_session),
) -> dto.Position:
    result = (
        db.query(tables.Position)
        .filter_by(id=position_id)
        .first()
    )
    if not result:
        raise HTTPException(status_code=404, detail="Position not found")

    return result


@router.put("/positions/{position_id}")
def update_position(
    position_id: UUID,
    new_data: dto.Position.Update,
    db: Session = Depends(db_session),
) -> dto.Position:
    position = (
        db.query(tables.Position)
        .filter_by(id=position_id)
        .one()
    )
    position.name = new_data.name
    db.commit()
    db.refresh(position)
    return position


@router.delete("/positions/{position_id}")
def update_position(
    position_id: UUID,
    db: Session = Depends(db_session),
) -> dto.Position:
    position = (
        db.query(tables.Position)
        .filter_by(id=position_id)
        .one()
    )
    position_data = dto.Position.from_orm(position)
    db.delete(position)
    db.commit()
    return position_data


@router.get("/positions/{position_id}/workers", response_model=list[dto.Worker])
def fetch_position_workers(
    position_id: UUID,
    db: Session = Depends(db_session),
) -> list[dto.Worker]:
    result = (
        db.query(tables.Worker)
        .join(tables.Position)
        .filter_by(id=position_id)
        .all()
    )
    return result
