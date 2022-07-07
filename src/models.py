
from sqlalchemy import Column, Integer, String, func, ForeignKey
from sqlalchemy.dialects.postgresql import TIMESTAMP

from . import db


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_name = Column(String, unique=True, nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_onupdate=func.now())


class CallBilling(db.Model):
    __tablename__ = 'call_billings'

    id = Column(Integer, primary_key=True)

    user_id = Column(ForeignKey('users.id'), nullable=False)
    call_duration = Column(Integer)
    block_count = Column(Integer)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_onupdate=func.now())
