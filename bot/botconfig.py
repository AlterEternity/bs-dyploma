PROJECT_NAME = "TicketBot"
# Telegram token
# TODO: discover options to hide value
TOKEN = '660816078:AAG2GMt_u1J4akSGQETs-_Jf0f6qYuL4foE'
BOT_URL = PROJECT_NAME

# General info for starting with webhook
WEBHOOK_HOST = None  # TODO: add server IP address
WEBHOOK_PORT = 443
WEBHOOK_LISTEN_HOST = '127.0.0.1'
WEBHOOK_LISTEN_PORT = 10010

WEBHOOK_SSL_CERT = None  # TODO: generate certificate

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % BOT_URL


# States TODO: redesign to use mongoDB
class State(enumerate):
    """
    Class for defining states for all stages in dialogue
    States: Start, Enter_event_name, Enter_date, Choose_event, Choose_tickets, Order_tickets
    """
    S_START = 0
    S_ENTER_LANG = 1
    S_ENTER_EVENT_NAME = 2
    S_ENTER_DATE = 3
    S_CHOOSE_EVENT = 4
    S_CHOOSE_TICKETS = 5
    S_ORDER_TICKETS = 6
