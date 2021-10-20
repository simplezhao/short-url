from datetime import datetime

import uvicorn
from fastapi import Depends, FastAPI
from fastapi.responses import RedirectResponse
from loguru import logger
from sqlalchemy.orm import Session

import models
import schemas
import views
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/s/{link_code}")
def redirect_url(link_code, db: Session = Depends(get_db)):

    url_info = views.get_url(db, link_code=link_code)
    origin_url = views.default_404_page()
    if url_info:
        if url_info.expired_at and url_info.expired_at > datetime.utcnow():
            origin_url = url_info.url
        else:
            logger.info(
                f"the url({url_info.url}) has expired after {url_info.expired_at}, dropped"
            )
    logger.info(f"the redirect url is {origin_url}")
    return RedirectResponse(origin_url, status_code=302)


@app.post("/api/v1/url")
def create_short_url(url: schemas.UrlCreate, db: Session = Depends(get_db)):
    item = views.create_url(db, url.url)
    logger.info(f"add new url: {item}")
    return item


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
