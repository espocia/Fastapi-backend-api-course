from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, text

from .database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default="True")
    create_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    create_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
