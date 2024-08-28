from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas


async def handle_swipe(swipe: schemas.SwipeCreate, db: AsyncSession):
    user = await db.execute(select(models.User).where(models.User.id == swipe.user_id))
    target_user = await db.execute(select(models.User).where(models.User.id == swipe.target_user_id))

    if user and target_user:
        new_swipe = models.Swipe(user_id=swipe.user_id, target_user_id=swipe.target_user_id)
        db.add(new_swipe)
        await db.commit()
        return {"status": "swiped successfully"}
    return {"status": "user or target user not found"}
