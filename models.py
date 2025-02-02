from database import Base
from sqlalchemy import (Column, Integer, String, 
                        Boolean, TIMESTAMP, text,
                        ForeignKey)
from sqlalchemy.orm import relationship


class Posts(Base):

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default='True')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    owner = relationship("Users")




class Users(Base) : 

    __tablename__ = "users"  

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Vote(Base):

    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), 
                     primary_key=True, nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), 
                     primary_key=True, nullable=False)