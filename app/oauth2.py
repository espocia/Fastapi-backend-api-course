from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = ["HS256"]
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def verify_access_token(token: str, credentails_exeptions):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id: str = payload.get("user_id")

        if id is None:
            raise credentails_exeptions

        token_data = schemas.TokenData(id=str(id))
    except InvalidTokenError:
        raise credentails_exeptions

    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentails_exeptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not verify credentails"
    )

    token = verify_access_token(token, credentails_exeptions)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
