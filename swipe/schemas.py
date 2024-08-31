from pydantic import BaseModel


class SwipeCreate(BaseModel):
    user_id: int
    target_user_id: int
