from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Users(Base):
    """Таблица пользователя"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)  # уникальное и НЕ МОЖЕТ быть пустым
    phone = Column(String, nullable=False, unique=True)  # уникальное и НЕ МОЖЕТ быть пустым
    email = Column(String, nullable=True, unique=True)  # уникальное и МОЖЕТ быть пустым
    gender = Column(String)
    hashed_password = Column(String, nullable=True)
    register_date = Column(TIMESTAMP, default=datetime.utcnow)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    # Связь с моделью  Swipe
    swipes = relationship(
        'Swipes',
        foreign_keys='Swipes.user_id',
        back_populates='user'
    )


