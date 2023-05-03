from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from src.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)  # make a name verification
    surname = Column(String)
    middle_name = Column(String, nullable=True)
    password = Column(String)
    email = Column(String)  # make an email verification
    phone = Column(String)  # make a phone number verification
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=True)
