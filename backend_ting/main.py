from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from module.user import User
from db.base_class import Base
from schemas.ticket import TicketStatus
from module.arena import Arena
from module.activity import Activity
from module.arena_taken import ArenaTaken
from module.ticket import Ticket
import uuid
from datetime import datetime

# 資料庫連線
db_url = "cockroachdb+psycopg2://root@localhost:26257/mydb?sslmode=disable"
engine = create_engine(db_url, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

##################### 請修改你需要的input ######################
# 功能設定
func = "create table"
sub_func = "create activity"    # create user / create arena / create activity

# user 輸入
# email = "alex@example.com"
# username = "alex"
# password = "alexalex"
# role = UserRole.CLIENT
# phone_number = "0999654738"

# arena 輸入
# arena_title = "Taipei Dome"
# arena_address = "No. 515, Section 4, Zhongxiao East Road, Xinyi District, Taipei City"
# arena_capacity = 15000

# activity 輸入
arena_id = uuid.UUID("b6bc20c4-e2ff-4e74-8d33-d62e1dd58ec9") # taipei_arena
user_id = uuid.UUID("c26a97b8-4bad-4e06-b355-bff8a65950da") # host
arena = session.query(Arena).filter_by(id=arena_id).first()
user = session.query(User).filter_by(id=user_id).first()
activity_title = "NCT 台北演唱會"
activity_content = "NCT dream concert"
activity_price = 5800
on_sale_date = datetime(2025, 7, 5, 20, 0)
start_time = datetime(2025, 8, 10, 19, 0)
end_time = datetime(2025, 8, 10, 21, 30)
cover_image = "https://example.com/cover.jpg"

########################### 功能區 ###########################
# 建立 table
if func == "create table":
    Base.metadata.create_all(engine)
    print("資料表建立完成")

def create_user(email, username, password, role, phone_number):
    return User(
        id=uuid.uuid4(),
        email=email,
        username=username,
        password=password,
        role=role,
        phone_number=phone_number,
        create_at=datetime.utcnow()
    )

def create_arena(title, address, capacity):
    return Arena(
        id=uuid.uuid4(),
        title=title,
        address=address,
        capacity=capacity
    )

def create_activity(title, content, price, on_sale_date, start_time, end_time, cover_image, arena, user):
    return Activity(
        id=uuid.uuid4(),
        title=title,
        content=content,
        price=price,
        on_sale_date=on_sale_date,
        start_time=start_time,
        end_time=end_time,
        num_ticket=arena.capacity,
        cover_image=cover_image,
        arena_id=arena.id,
        creator_id=user.id,
        is_achieved=False
    )

def create_arena_taken(activity, arena):
    return ArenaTaken(
        id=uuid.uuid4(),
        activity_id=activity.id,
        arena_id=arena.id,
        date=activity.start_time.date()
    )

def create_ticket(activity):
    tickets = []
    for i in range(1, activity.num_ticket + 1):
        seat_number = f"{str(activity.id)[:8]}-{i:05d}"
        ticket = Ticket(
            id=uuid.uuid4(),
            user_id=None,
            create_at=datetime.utcnow(),
            activity_id=activity.id,
            seat_number=seat_number,
            status=TicketStatus.UNSOLD,
            is_finish=False
        )
        tickets.append(ticket)
    return tickets

if sub_func == "create user":
    new_user = create_user(email, username, password, role, phone_number)
    session.add(new_user)
    session.commit()
    print(f"User 建立成功：{new_user.username}")

elif sub_func == "create arena":
    new_arena = create_arena(arena_title, arena_address, arena_capacity)
    session.add(new_arena)
    session.commit()
    print(f"Arena 建立成功：{new_arena.title}")

elif sub_func == "create activity":
    activity = create_activity(activity_title, activity_content, activity_price,
                               on_sale_date, start_time, end_time,
                               cover_image, arena, user)
    session.add(activity)
    session.commit()
    print(f"Activity 建立成功：{activity.title}")

    arena_taken = create_arena_taken(activity, arena)
    session.add(arena_taken)
    session.commit()
    print(f"ArenaTaken 建立完成：{arena_taken.id}")

    tickets = create_ticket(activity)
    session.add_all(tickets)
    session.commit()
    print(f"共建立 {len(tickets)} 張票券")

