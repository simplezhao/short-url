import os

from sqlalchemy.orm import Session
import random
import string
import models
from datetime import datetime, timedelta


def get_url(db: Session, link_code: str):

    return db.query(models.URLData).filter(models.URLData.code == link_code).first()


def create_url(db: Session, url: str):
    alphabet = string.ascii_lowercase + string.digits + string.ascii_uppercase
    code = "".join(random.choices(alphabet, k=7))
    utc_now = datetime.utcnow()
    item = models.URLData(url=url, created_at=utc_now)
    item.code = code
    item.expired_at = utc_now + timedelta(days=7)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def default_404_page():
    return os.getenv("DEFAULT_404_URL", None)
