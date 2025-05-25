from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from schemas.ticket import TicketStatus
from module.ticket import Ticket
import uuid


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