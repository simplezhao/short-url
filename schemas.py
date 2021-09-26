from pydantic import BaseModel, validator
from urllib.parse import urlparse


class UrlCreate(BaseModel):
    url: str

    @validator('url')
    def valid_url(cls, v):
        if urlparse(v).scheme not in ('http', 'https'):
            raise ValueError('url is invalid')

        return v

