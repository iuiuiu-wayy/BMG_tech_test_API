from . import db
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Sequence, ForeignKey, UnicodeText
from sqlalchemy.orm import sessionmaker



Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    username = Column(String, primary_key=True, unique=True)
    password = Column(String)
    name = Column(String)
    email = Column(String, unique=True)
    referral_code = Column(String)


Base.metadata.create_all(db.engine)
Session = sessionmaker(bind=db.engine)

