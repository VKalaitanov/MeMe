from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .models import Swipe
from .schemas import SwipeCreate
from oauth.models import Users


async def handle_swipe(swipe: SwipeCreate, session: AsyncSession):
    user = await session.execute(select(Users).where(Users.id == swipe.user_id))
    target_user = await session.execute(select(Users).where(Users.id == swipe.target_user_id))

    if user and target_user:
        new_swipe = Swipe(user_id=swipe.user_id, target_user_id=swipe.target_user_id)
        session.add(new_swipe)
        await session.commit()
        return {"status": "swiped successfully"}
    return {"status": "user or target user not found"}
