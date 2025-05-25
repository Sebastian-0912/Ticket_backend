# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# # 資料庫連線字串（本機 + insecure）
# db_url = "cockroachdb+psycopg2://root@localhost:26257/mydb?sslmode=disable"

# # 建立 engine 與 session
# engine = create_engine(db_url, echo=True)
# Session = sessionmaker(bind=engine)
# session = Session()

# db/connection.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql.psycopg2 import PGDialect_psycopg2

# Patch CockroachDB version issue
original_get_server_version_info = PGDialect_psycopg2._get_server_version_info
def _patched_get_server_version_info(self, connection):
    try:
        return original_get_server_version_info(self, connection)
    except AssertionError:
        return (24, 3)

PGDialect_psycopg2._get_server_version_info = _patched_get_server_version_info

# DB Config
db_url = os.getenv("DATABASE_URL", "cockroachdb+psycopg2://root@localhost:26257/defaultdb?sslmode=disable")
engine = create_engine(db_url, echo=True)
SessionLocal = sessionmaker(bind=engine)
