import typing
from uuid import UUID
from sqlalchemy.orm import Session
import models
from schemas import item_schema

def search_items(db: Session, item: item_schema.Item):
    print(item)
    x = db.query(models.Item).filter(models.Item.category == item['category'], models.Item.description==item['description'], models.Item.user_id==item['user_id'])
    print(x.all())
    return x

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: item_schema.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), user_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def create_user_items(db: Session, items: typing.List[item_schema.ItemCreate], user_id: int) -> typing.List:
    create_user_items = []
    for item in items:
        db_item = models.Item(category='others', description=item['label'], user_id=user_id)
        db.add(db_item)
        create_user_items.append({"label": db_item.description, "score": item['score']})
    db.commit()
    return create_user_items