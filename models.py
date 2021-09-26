from database import Base
from sqlalchemy import Column, Integer, TIMESTAMP, String
from datetime import datetime


class URLData(Base):
    __tablename__ = "url_data"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    code = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow())
    expired_at = Column(TIMESTAMP, nullable=False)
