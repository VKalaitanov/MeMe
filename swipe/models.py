from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

from oauth.models import Users


Base = declarative_base()


class Swipe(Base):
    __tablename__ = "swipes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(Users.id))
    target_user_id = Column(Integer, ForeignKey(Users.id))

    user = relationship(Users, back_populates="swipes")
