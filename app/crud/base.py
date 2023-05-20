from typing import Generic, Optional, Type, TypeVar, List
from pydantic import BaseModel
from sqlmodel import SQLModel, select, or_
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model.from_orm(obj_in)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, user: str) -> Optional[ModelType]:
        return db.exec(select(self.model).where(self.model.id == user)).first().unique()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.exec(select(self.model).offset(skip).limit(limit)).unique().all()

    def update(
        self, db: Session, *, db_obj: ModelType, obj_in: UpdateSchemaType
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
