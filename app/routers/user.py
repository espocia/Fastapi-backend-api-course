from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import models, schemas, utils
from app.database import get_db

router = APIRouter(prefix="/user", tags=["Posts"])


@router.get("/", response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    user_query = db.query(models.User).all()
    if not user_query:
        utils.raise_404("No users founds")
    return user_query


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id).first()
    if not user_query:
        utils.raise_404(f"user with id {id} not found")
    return user_query


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    # hash the password - user.password

    user.password = utils.hash(user.password)

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
