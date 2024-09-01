from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from fastapi import HTTPException, status

from .models import Users
from .validators import transformation_phone


async def add_user_in_database(username: str,
                               phone: str,
                               hashed_password: str,
                               session: AsyncSession):
    """Добавление пользователя"""
    await exists_user_by_username(username, session)
    user = Users(username=username, phone=phone, hashed_password=hashed_password)
    session.add(user)
    await session.commit()
    await session.refresh(user)


async def exists_user_by_username(username: str, session: AsyncSession):
    """Проверка наличия пользователя"""
    user = await session.execute(select(Users).where(Users.username == username))  # type: ignore
    if user.scalar():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="A user with the same Nickname already exists")


async def get_user(username: str, session: AsyncSession):
    """Выдача пользователя"""
    user = await session.execute(select(Users).where(Users.username == username))  # type: ignore
    user = user.scalar()
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Invalid username or password")


async def delete_user_db(username: str, session: AsyncSession):
    """Удаление пользователя"""
    await session.execute(delete(Users).where(Users.username == username))  # type: ignore
    await session.commit()


async def exists_user_by_phone(number_phone: str, session: AsyncSession):
    """Проверка наличия пользователя по номеру телефона"""
    phone = transformation_phone(number_phone)
    user = await session.execute(select(Users).where(Users.phone == phone))  # type: ignore
    if user.scalar():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="A user with the same phone number already exists")


async def change_password_db(username: str,
                             new_hash_password,
                             session: AsyncSession):
    """Смена пароля пользователю"""
    await session.execute(update(Users).where(Users.username == username)  # type: ignore
                          .values(hashed_password=new_hash_password))
    await session.commit()
