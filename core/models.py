from sqlalchemy import Column, Integer, String, DateTime, Table, ForeignKey, ARRAY,BigInteger 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class General(Base):
    __tablename__ = 'general'
    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime)

class Server(Base):
    __tablename__ = 'server'
    guild = Column(BigInteger , primary_key=True)
    category =  Column(String(50), default='feedback')
    channel =  Column(String(50), default='feedback')
    allowed_links = Column(ARRAY(String), default=['youtube.com', 'soundcloud.com', 'audius.com'])
    min_length = Column(Integer, default=30)
    max_feedback = Column(Integer, default=3)

class Users(Base):
    __tablename__ = 'users'
    userid = Column(BigInteger , primary_key=True)
    guild = Column(BigInteger, ForeignKey('server.guild'))
    rating = Column(Integer, default=1)
    votes = Column(Integer, default=1)

class Posts(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    userid = Column(BigInteger, ForeignKey('users.userid'))
    link = Column(String(32), nullable=False)
    body = Column(String(200), nullable=False)
    guild = Column(BigInteger, ForeignKey('server.guild'))

class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True)
    related_post = Column(Integer, ForeignKey('posts.id'))
    recipient_id = Column(BigInteger, ForeignKey('users.userid'))
    addressee_id = Column(BigInteger, ForeignKey('users.userid'))
    body = Column(String(200), nullable=False)
    guild = Column(BigInteger, ForeignKey('server.guild'))
    rating = Column(Integer, default=1)

