from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker,Session
from models.user import User
from db.base_class import Base
from schemas.ticket import TicketStatus
from models.arena import Arena
from models.activity import Activity
from models.arena_taken import ArenaTaken
from models.ticket import Ticket
import uuid
from datetime import datetime
from flask import Flask, request, jsonify, abort, g
import os
from schemas.user import UserRole
from db.session import SessionLocal
from typing import cast

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

app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

def get_db() -> Session:
    return cast(Session, g.db)

# This runs before each request
@app.before_request
def create_db_session():
    g.db = SessionLocal()

# This runs after each request (even if error)
@app.teardown_request
def close_db_session(exception=None):
    db = g.pop('db', None)
    if db is not None:
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
        result = db.execute(text("SELECT * from users;"))
        return jsonify({"status": "success", "message": f"Database connection successful.{result}"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Database connection failed: {str(e)}"}), 500


