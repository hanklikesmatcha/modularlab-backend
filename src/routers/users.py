from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from schemas import item_schema, user_schema
from queries import item_queries, user_queries
from database import db_connection, Session

router = APIRouter(prefix='/users', tags=['users'])


@router.post('', response_model=user_schema.User)
def create_user(user: user_schema.UserCreate, db: Session = Depends(db_connection)):
    db_user = user_queries.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_queries.create_user(db=db, user=user)


@router.get('', response_model=list[user_schema.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(db_connection)):
    users = user_queries.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=user_schema.User)
def read_user(user_id: UUID, db: Session = Depends(db_connection)):
    db_user = user_queries.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/{user_id}/items/", response_model=item_schema.Item)
def create_item_for_user(
    user_id: UUID, item: item_schema.ItemCreate, db: Session = Depends(db_connection)
):
    return item_queries.create_user_item(db=db, item=item, user_id=user_id)