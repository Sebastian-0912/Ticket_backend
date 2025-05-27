from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from schemas.ticket import TicketStatus
from models.ticket import Ticket
import uuid
from models.user import User
from db.base_class import Base
from models.arena import Arena
from models.activity import Activity
from models.arena_taken import ArenaTaken
from datetime import datetime

# 資料庫連線
db_url = "cockroachdb+psycopg2://root@localhost:26257/mydb?sslmode=disable"
engine = create_engine(db_url, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

##################### 請修改你需要的input ######################
# 缺少盡量給予連號票卷的功能
func = "buy ticket" # pay for ticket / 
client_id = uuid.UUID("33e62d67-5740-4fe2-887e-465c42147371")  # Alice(client)
activity_id = uuid.UUID("a8b8b827-3582-41a6-beec-99fe78fd0c23")  # Blackpink 活動
num_tickets = 3

if func == "buy ticket":
    def purchase_ticket(session, user_id, activity_id, num_tickets):
        if num_tickets > 4:
            raise ValueError("最多只能購買 4 張票")
        
        tickets = session.query(Ticket).filter_by(
            activity_id=activity_id,
            status=TicketStatus.UNSOLD
        ).limit(num_tickets).all()

        if len(tickets) < num_tickets:
            raise ValueError("剩餘票數不足")

        for ticket in tickets:
            ticket.user_id = user_id
            ticket.status = TicketStatus.UNPAID

        session.commit()
        return tickets

    try:
        tickets = purchase_ticket(session, client_id, activity_id, num_tickets)
        for t in tickets:
            print(f"購票成功，座位：{t.seat_number}")
    except ValueError as e:
        print(f"購票失敗：{e}")

    session.commit()
elif func == "pay for ticket":
    def pay_ticket(session, user_id, activity_id):
        # find 該用戶在該活動的 UNPAID 票券
        unpaid_tickets = session.query(Ticket).filter_by(
            user_id=user_id,
            activity_id=activity_id,
            status=TicketStatus.UNPAID
        ).all()

        if not unpaid_tickets:
            print("沒有未付款的票券")
            return

        # 票券狀態更新為 SOLD
        for ticket in unpaid_tickets:
            ticket.status = TicketStatus.SOLD

        session.commit()
        print(f"已成功付款，票券數量：{len(unpaid_tickets)}")

        for ticket in unpaid_tickets:
            print(f"已付款票券：{ticket.seat_number}")

    pay_ticket(
        session,
        user_id=client_id,
        activity_id=activity_id
    )
    
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