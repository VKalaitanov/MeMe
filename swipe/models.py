from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from oauth.models import Base


class Swipes(Base):
    __tablename__ = 'swipes'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    target_user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("Users", foreign_keys=[user_id])
    target_user = relationship("Users", foreign_keys=[target_user_id])
