import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from models.ticket import Ticket, TicketStatus
from models.activity import Activity
from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError

def create_tickets_for_activity(db: Session, activity_id: uuid.UUID, capacity: int) -> None:
    for seat_num in range(1, capacity + 1):
        ticket = Ticket(
            id=uuid.uuid4(),
            user_id=None,
            activity_id=activity_id,
            seat_number=str(seat_num),
            status=TicketStatus.UNSOLD,
            is_finish=False,
            create_at=datetime.now(timezone.utc),
        )
        db.add(ticket)

def get_tickets_by_user(db: Session, user_id: uuid.UUID) -> list[Ticket]:
    return db.query(Ticket).filter_by(user_id=user_id).all()

def reserve_ticket(db: Session, user_id: UUID, activity_id: UUID, num_tickets: int):
    try:
        activity = db.query(Activity).filter(Activity.id == activity_id).first()
        if not activity:
            return None, "Invalid data"

        # sold_tickets = db.query(Ticket).filter(
        #     Ticket.activity_id == activity_id,
        #     Ticket.status == TicketStatus.SOLD).count()
        unsold_tickets = db.query(Ticket).filter(
            Ticket.activity_id == activity_id,
            Ticket.status == TicketStatus.UNSOLD
            ).with_for_update(skip_locked=True).limit(num_tickets).all()

        
        if len(unsold_tickets) < num_tickets:
            return None, "Tickets sold out"

        for ticket in unsold_tickets:
            ticket.user_id = user_id
            ticket.status = TicketStatus.UNPAID

        db.commit()
        return unsold_tickets, None
    
    except SQLAlchemyError as e:
        db.rollback()
        return None, str(e)


def buy_ticket(db: Session, ticket_id: UUID):
    try:
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not ticket:
            return None
        if ticket.status != TicketStatus.UNPAID:
            print(ticket.status)
            return "invalid_state"

        ticket.status = TicketStatus.SOLD
        db.commit()
        return ticket
    except SQLAlchemyError as e:
        db.rollback()
        print(e)
        return None, str(e)


def refund_ticket(db: Session, ticket_id: UUID):
    try:
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not ticket:
            return None, "Ticket not found"
        if ticket.status != TicketStatus.SOLD:
            return None, "Ticket already used or cannot refund"

        ticket.status = TicketStatus.UNSOLD
        ticket.user_id = None
        # activity = db.query(Activity).filter(Activity.id == ticket.activity_id).first()
        # if activity:
        #     activity.remaining_slots += 1

        db.commit()
        return ticket, None
    except SQLAlchemyError as e:
        db.rollback()
        return None, str(e)

def get_ticket_by_id(db: Session, ticket_id: UUID):
    try:
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        return ticket if ticket else (None, "Ticket not found")
    except SQLAlchemyError as e:
        return None, str(e)


def get_tickets_by_user(db: Session, user_id: UUID):
    try:
        tickets = db.query(Ticket).filter(Ticket.user_id == user_id).all()
        return tickets, None
    except SQLAlchemyError as e:
        return None, str(e)
