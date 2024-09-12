from fastapi import HTTPException, status
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt", "sha256_crypt"], deprecated="auto")


def raise_404(message: str):
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail=message)


def raise_403(message: str):
    raise HTTPException(status.HTTP_403_FORBIDDEN, detail=message)

def raise_409(message: str):
    raise HTTPException(status.HTTP_409_CONFLICT, detail=message)

def hash(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)
