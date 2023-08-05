from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SkribblBase(BaseModel):
    word: str
    submitter: str


class SkribblIn(SkribblBase):
    pass


class SkribblOut(SkribblBase):
    submitted: datetime

    class Config:
        orm_mode = True
