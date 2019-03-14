# Telegram token
# TODO: discover options to hide value
token = '660816078:AAG2GMt_u1J4akSGQETs-_Jf0f6qYuL4foE'


# States
class State(enumerate):
    """
    Class for defining states for all stages in dialogue
    States: Start, Enter_event_name, Enter_date, Choose_event, Choose_tickets, Order_tickets
    """
    S_START = 0
    S_ENTER_EVENT_NAME = 1
    S_ENTER_DATE = 2
    S_CHOOSE_EVENT = 3
    S_CHOOSE_TICKETS = 4
    S_ORDER_TICKETS = 5
