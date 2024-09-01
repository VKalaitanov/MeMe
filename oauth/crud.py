from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from fastapi import HTTPException, status

from .models import Users
from .validators import transformation_phone


async def add_user_in_database(username: str, phone: str, hashed_password: str, session: AsyncSession):
    """Добавление пользователя"""
    await exists_user_by_username(username, session)
    user = Users(username=username, phone=phone, hashed_password=hashed_password)
    session.add(user)
    await session.commit()


async def exists_user_by_username(username: str, session: AsyncSession):
    """Проверка наличия пользователя по имени"""
    user = await session.scalar(select(Users).where(Users.username == username))
    if user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="A user with the same username already exists")


async def get_user(username: str, session: AsyncSession):
    """Получение пользователя по имени"""
    user = await session.scalar(select(Users).where(Users.username == username))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid username or password")
    return user


async def delete_user_db(username: str, session: AsyncSession):
    """Удаление пользователя"""
    await session.execute(delete(Users).where(Users.username == username))
    await session.commit()


async def exists_user_by_phone(number_phone: str, session: AsyncSession):
    """Проверка наличия пользователя по номеру телефона"""
    phone = transformation_phone(number_phone)
    user = await session.scalar(select(Users).where(Users.phone == phone))
    if user is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="A user with the same phone number already exists")
    return True


async def change_password_db(username: str, new_hash_password: str, session: AsyncSession):
    """Смена пароля пользователю"""
    await session.execute(update(Users).where(Users.username == username)
                          .values(hashed_password=new_hash_password))
    await session.commit()
