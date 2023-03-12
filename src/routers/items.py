from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from schemas import item_schema
from queries import item_queries, user_queries
from database import db_connection, Session
from uuid import UUID
from fastapi import UploadFile, Depends, HTTPException, File
from schemas import item_schema
from queries import item_queries, user_queries
from utils import computer_vision_tasks 
from azure.cognitiveservices.vision.computervision import models

from database import db_connection, Session

router = APIRouter(prefix='/items', tags=['items'])


@router.get("/search-items/{user_id}/{category}/{description}", response_model=list[item_schema.Item])
def search_items(user_id: UUID, description: str, category: str, db: Session = Depends(db_connection)):
    db_user = user_queries.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    items = item_queries.search_items(db, item={'user_id': db_user.id, 'category': category, 'description': description})
    return items.all()


@router.get("/", response_model=list[item_schema.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(db_connection)):
    items = item_queries.get_items(db, skip=skip, limit=limit)
    return items

@router.post("/image-classification")
async def classify_image(file: UploadFile, user_id: UUID, db: Session = Depends(db_connection)):
    db_user = user_queries.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    potential_objects = []
    try:
        encoded_file = await file.read()
        potential_objects = computer_vision_tasks.image_recognition(encoded_file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"There was an error when scanning the file - {e}")

    items = item_queries.create_user_items(db=db, items=potential_objects, user_id=user_id)
    
    return {"status": "successful", "user": db_user.email, "data": items}

@router.post("/text-extraction/easy-ocr")
async def text_extraction(file: UploadFile, user_id: UUID, db: Session = Depends(db_connection)):
    db_user = user_queries.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, error="User not found")
    try:    
        encoded_file = await file.read()
        text_lines = computer_vision_tasks.text_extraction(file=encoded_file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"There was an error when scanning the file - {e}")
    items = item_queries.create_user_items(db=db, items=text_lines, user_id=user_id)

    return {"status": "successful", "user": db_user.email, "data": items}


@router.post("/text-extraction/microsoft")
async def mcft_text_extraction(user_id: UUID, db: Session = Depends(db_connection), file: UploadFile = File(...)):
    db_user = user_queries.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, error="User not found")
    try:    
        encoded_file = file.file.read()
        text_lines = computer_vision_tasks.mcft_ocr(file=encoded_file)

    except models._models_py3.ComputerVisionOcrErrorException as e:
        raise HTTPException(status_code=500, detail=f"There was an error when scanning the file - {e}")

    items = item_queries.create_user_items(db=db, items=text_lines, user_id=user_id)

    return {"status": "successful", "user": db_user.email, "data": items}


@router.post("/image-categorisation")
async def image_categorisation(user_id: UUID, db: Session = Depends(db_connection), file: UploadFile = File(...)):
    db_user = user_queries.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, error="User not found")
    try:    
        encoded_file = file.file.read()
        text_lines = computer_vision_tasks.mcft_image_categorisation(file=encoded_file)
    except models._models_py3.ComputerVisionOcrErrorException as e:
        raise HTTPException(status_code=500, detail=f"There was an error when scanning the file - {e}")

    items = item_queries.create_user_items(db=db, items=text_lines, user_id=user_id)

    return {"status": "successful", "user": db_user.email, "data": items}