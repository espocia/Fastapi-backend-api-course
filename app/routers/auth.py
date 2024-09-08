from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import models, oauth2, schemas, utils
from app.database import get_db

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.Token)
def login(
    user_credentails: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentails.username)
        .first()
    )

    if not user:
        utils.raise_403("invalid credentails")

    if not utils.verify_password(user_credentails.password, str(user.password)):
        utils.raise_403("invalid credentails")

    access_token = oauth2.create_access_token(
        data={"user_id": user.id, "user": user.email}
    )

    return {"access_token": access_token}
