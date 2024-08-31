from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, TIMESTAMP
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Users(Base):
    """Таблица пользователя"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username: str = Column(String, nullable=False, unique=True)  # уникальное  и НЕ МОЖЕТ быть пустым
    phone: str = Column(String, nullable=False, unique=True)  # уникальное  и НЕ МОЖЕТ быть пустым
    email: str = Column(String, nullable=True, unique=True)  # уникальное  и МОЖЕТ быть пустым
    gender = Column(String)
    swipes = relationship('Swipe', back_populates="user")
    hashed_password: str = Column(String, nullable=True)
    register_data: datetime.utcnow = Column(TIMESTAMP, default=datetime.utcnow())  # дата регистрации пользователя
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)
