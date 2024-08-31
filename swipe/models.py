from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from oauth.models import Base


class Swipe(Base):
    __tablename__ = "swipes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    target_user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("Users", back_populates="swipes")
