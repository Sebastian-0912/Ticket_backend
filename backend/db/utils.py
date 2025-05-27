# utils/db.py

from flask import g
from typing import cast
from sqlalchemy.orm import Session

def get_db() -> Session:
    return cast(Session, g.db)
