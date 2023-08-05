from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import random

from .. import models, schemas


def skribbl_get_word(db: Session, word: str):
    return db.query(models.Skribbl).filter_by(word=word).first()


def skribbl_get_words(db: Session, limit: Optional[int] = None):
    return db.query(models.Skribbl).order_by(random()).limit(limit).all()


def skribbl_add_word(db: Session, word: schemas.SkribblIn) -> models.Skribbl:
    w = models.Skribbl(word=word.word, submitter=word.submitter)
    db.add(w)
    db.commit()
    db.refresh(w)
    return w


def skribbl_delete_word(db: Session, word: str) -> int:
    r = db.query(models.Skribbl).filter_by(word=word).delete()
    db.commit()
    return r
