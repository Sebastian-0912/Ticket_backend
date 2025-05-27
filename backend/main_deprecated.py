import os
from typing import List, Optional

from flask import Flask, request, jsonify, abort
import sqlalchemy_cockroachdb.base
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
# from dotenv import load_dotenv # 如果使用 python-dotenv

# load_dotenv() # 如果使用 python-dotenv

# --- SQLAlchemy 設定 ---
# 從環境變數讀取 DATABASE_URL
# 範例: "postgresql://root@crdb1:26257/defaultdb?sslmode=disable"
# 在 docker-compose.yml 中設定
DATABASE_URL = os.getenv("DATABASE_URL", "cockroachdb+psycopg2://root@localhost:26257/defaultdb?sslmode=disable")

from sqlalchemy.dialects.postgresql.psycopg2 import PGDialect_psycopg2
original_get_server_version_info = PGDialect_psycopg2._get_server_version_info

def _patched_get_server_version_info(self, connection):
    try:
        return original_get_server_version_info(self, connection)
    except AssertionError:
        # 如果無法解析版本，則使用默認版本
        return (24, 3)

PGDialect_psycopg2._get_server_version_info = _patched_get_server_version_info

# 明確設定 CockroachDB 版本資訊

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- SQLAlchemy 模型 (Models) ---
class ItemDB(Base):
    __tablename__ = "items" # 資料表名稱

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True, nullable=True)

# 啟動時創建資料表 (如果不存在)
Base.metadata.create_all(bind=engine)

# --- Flask 應用程式實例 ---
app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

# --- 資料庫會話處理 ---
def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

# 輔助函數將 ItemDB 轉換為字典
def item_to_dict(item):
    return {
        "id": item.id,
        "name": item.name,
        "description": item.description
    }

# --- API 端點 (Endpoints) ---
@app.route("/items/", methods=["POST"])
def create_item():
    """
    創建一個新的 item。
    """
    data = request.json
    db = get_db()
    try:
        db_item = ItemDB(name=data["name"], description=data.get("description"))
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return jsonify(item_to_dict(db_item)), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()

@app.route("/items/<int:item_id>", methods=["GET"])
def read_item(item_id):
    """
    根據 ID 獲取一個 item。
    """
    db = get_db()
    try:
        db_item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
        if db_item is None:
            abort(404, description="Item not found")
        return jsonify(item_to_dict(db_item))
    finally:
        db.close()

@app.route("/items/", methods=["GET"])
def read_items():
    """
    獲取 item 列表，支持分頁。
    """
    skip = request.args.get("skip", 0, type=int)
    limit = request.args.get("limit", 10, type=int)
    
    db = get_db()
    try:
        items = db.query(ItemDB).offset(skip).limit(limit).all()
        return jsonify([item_to_dict(item) for item in items])
    finally:
        db.close()

@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    """
    根據 ID 更新一個 item。
    """
    data = request.json
    db = get_db()
    try:
        db_item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
        if db_item is None:
            abort(404, description="Item not found")

        # 更新欄位
        db_item.name = data["name"]
        db_item.description = data.get("description")

        db.commit()
        db.refresh(db_item)
        return jsonify(item_to_dict(db_item))
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()

@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    """
    根據 ID 刪除一個 item。
    """
    db = get_db()
    try:
        db_item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
        if db_item is None:
            abort(404, description="Item not found")

        deleted_item = item_to_dict(db_item)
        db.delete(db_item)
        db.commit()
        return jsonify(deleted_item)
    finally:
        db.close()

@app.route("/")
def root():
    return jsonify({"message": "Flask ORM App is running!"})

# --- 資料庫連線測試端點 ---
@app.route("/db-test/")
def test_db_connection():
    db = get_db()
    try:
        # 執行一個簡單的查詢
        db.execute(text("SELECT 1"))
        return jsonify({"status": "success", "message": "Database connection successful."})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Database connection failed: {str(e)}"}), 500
    finally:
        db.close()

# 處理 404 錯誤
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

# 如果直接運行這個檔案
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)


# # ##################### 請修改你需要的input ######################
# # 功能設定
# # func = "create table"
# func = "none"
# # sub_func = "create activity"    # create user / create arena / create activity
# sub_func = "none"    # create user / create arena / create activity

# # user 輸入
# email = "alex@example.com"
# username = "alex"
# password = "alexalex"
# role = UserRole.CLIENT
# phone_number = "0999654738"

# # arena 輸入
# arena_title = "Taipei Dome"
# arena_address = "No. 515, Section 4, Zhongxiao East Road, Xinyi District, Taipei City"
# arena_capacity = 15000

# # activity 輸入
# arena_id = uuid.UUID("217f5a69-ebd7-4d7c-a244-3c6467e9c129") # taipei_arena
# user_id = uuid.UUID("14b5f079-320b-4e87-9588-f5f260f46bd1") # host
# arena = session.query(Arena).filter_by(id=arena_id).first()
# user = session.query(User).filter_by(id=user_id).first()
# activity_title = "NCT 台北演唱會"
# activity_content = "NCT dream concert"
# activity_price = 5800
# on_sale_date = datetime(2025, 7, 5, 20, 0)
# start_time = datetime(2025, 8, 10, 19, 0)
# end_time = datetime(2025, 8, 10, 21, 30)
# cover_image = "https://example.com/cover.jpg"

# ########################### 功能區 ###########################
# # 建立 table
# if func == "create table":
#     Base.metadata.create_all(engine)
#     print("資料表建立完成")

# def create_user(email, username, password, role, phone_number):
#     return User(
#         id=uuid.uuid4(),
#         email=email,
#         username=username,
#         password=password,
#         role=role,
#         phone_number=phone_number,
#         create_at=datetime.utcnow()
#     )

# def create_arena(title, address, capacity):
#     return Arena(
#         id=uuid.uuid4(),
#         title=title,
#         address=address,
#         capacity=capacity
#     )

# def create_activity(title, content, price, on_sale_date, start_time, end_time, cover_image, arena, user):
#     return Activity(
#         id=uuid.uuid4(),
#         title=title,
#         content=content,
#         price=price,
#         on_sale_date=on_sale_date,
#         start_time=start_time,
#         end_time=end_time,
#         num_ticket=arena.capacity,
#         cover_image=cover_image,
#         arena_id=arena.id,
#         creator_id=user.id,
#         is_achieved=False
#     )

# def create_arena_taken(activity, arena):
#     return ArenaTaken(
#         id=uuid.uuid4(),
#         activity_id=activity.id,
#         arena_id=arena.id,
#         date=activity.start_time.date()
#     )

# def create_ticket(activity):
#     tickets = []
#     for i in range(1, activity.num_ticket + 1):
#         seat_number = f"{str(activity.id)[:8]}-{i:05d}"
#         ticket = Ticket(
#             id=uuid.uuid4(),
#             user_id=None,
#             create_at=datetime.utcnow(),
#             activity_id=activity.id,
#             seat_number=seat_number,
#             status=TicketStatus.UNSOLD,
#             is_finish=False
#         )
#         tickets.append(ticket)
#     return tickets

# if sub_func == "create user":
#     new_user = create_user(email, username, password, role, phone_number)
#     session.add(new_user)
#     session.commit()
#     print(f"User 建立成功：{new_user.username}")

# elif sub_func == "create arena":
#     new_arena = create_arena(arena_title, arena_address, arena_capacity)
#     session.add(new_arena)
#     session.commit()
#     print(f"Arena 建立成功：{new_arena.title}")

# elif sub_func == "create activity":
#     activity = create_activity(activity_title, activity_content, activity_price,
#                                on_sale_date, start_time, end_time,
#                                cover_image, arena, user)
#     session.add(activity)
#     session.commit()
#     print(f"Activity 建立成功：{activity.title}")

#     arena_taken = create_arena_taken(activity, arena)
#     session.add(arena_taken)
#     session.commit()
#     print(f"ArenaTaken 建立完成：{arena_taken.id}")

#     tickets = create_ticket(activity)
#     session.add_all(tickets)
#     session.commit()
#     print(f"共建立 {len(tickets)} 張票券")