from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Users
from engine_db import get_async_session
from .hashing import Hasher
from .crud import (get_user, add_user_in_database, exists_user_by_phone,
                   change_password_db, delete_user_db)
from .schemas import GetMeUser, RegisterUser, ChangePassword
from .validators import transformation_phone

router = APIRouter()
security = HTTPBasic()


async def basic_auth(user: Annotated[HTTPBasicCredentials, Depends(security)],
                     session: AsyncSession = Depends(get_async_session)):
    """Метод возвращает пользователя из базы данных"""
    user_from_db = await get_user(username=user.username, session=session)
    if not Hasher.verify_password(plain_password=user.password, hashed_password=user_from_db.hashed_password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid username or password")
    return user_from_db


@router.get("/me/profile/", response_model=GetMeUser)
async def get_user_me(user: Users = Depends(basic_auth)):
    """Возвращает свой профиль пользователя"""
    return user


@router.delete('/me/profile/')
async def delete_user(password_user: str,  # пароль от пользователя для подтверждения удаления профиля
                      user: Users = Depends(basic_auth),
                      session: AsyncSession = Depends(get_async_session)):
    """Удаление авторизованного пользователя"""
    username = user.username
    if not Hasher.verify_password(plain_password=password_user,  # проверка паролей
                                  hashed_password=user.hashed_password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid old password")
    await delete_user_db(username, session)  # удаление профиля
    return {"success": "User deleted successfully!"}


@router.post("/register/", status_code=status.HTTP_201_CREATED)
async def register_user(user: RegisterUser,
                        session: AsyncSession = Depends(get_async_session)):
    """Регистрация пользователя на сайте"""
    # Проверяем наличие юзера с таким номером телефона
    if await exists_user_by_phone(user.phone, session):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="A user with the same phone number already exists")

    phone = transformation_phone(user.phone)
    hashed_password = Hasher.get_password_hash(user.password_1)
    await add_user_in_database(user.username, phone, hashed_password, session)
    return {"success": "User successfully registered!"}


@router.post("/change-password/")
async def change_password(password_schema: ChangePassword,
                          user: Users = Depends(basic_auth),  # текущий пользователь
                          session: AsyncSession = Depends(get_async_session)):
    """Функция смены пароля"""
    if not Hasher.verify_password(  # Проверка паролей
            plain_password=password_schema.old_password,
            hashed_password=user.hashed_password):  # сравниваем полученный пароль со старым
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid old password")
    new_hashed_password = Hasher.get_password_hash(password_schema.password_1)  # получаем hash нового пароля
    await change_password_db(username=user.username,
                             new_hash_password=new_hashed_password,
                             session=session)
    return {"success": "Password changed successfully!"}
