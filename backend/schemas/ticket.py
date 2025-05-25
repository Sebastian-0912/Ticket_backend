from enum import Enum

class TicketStatus(str, Enum):
    UNSOLD = "unsold"
    UNPAID = "unpaid"
    SOLD = "sold"
