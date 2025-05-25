from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 資料庫連線字串（本機 + insecure）
db_url = "cockroachdb+psycopg2://root@localhost:26257/mydb?sslmode=disable"

# 建立 engine 與 session
engine = create_engine(db_url, echo=True)
Session = sessionmaker(bind=engine)
session = Session()