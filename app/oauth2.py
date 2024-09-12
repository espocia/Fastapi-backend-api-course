from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session
from app.config import Settings

from app import models, schemas
from app.database import get_db

settings = Settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = [settings.algorithm]
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minute


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
