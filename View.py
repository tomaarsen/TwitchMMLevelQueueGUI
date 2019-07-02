
from enum import Enum, auto

class MessageSource(Enum):
    ADD_LEVEL_SUCCESS = auto()
    ADD_LEVEL_WARNING = auto()
    ADD_LEVEL_ERROR = auto()
    NEXT_LEVEL_SUCCESS = auto()
    NEXT_LEVEL_ERROR = auto()
    CURRENT_LEVEL_SUCCESS = auto()
    CURRENT_LEVEL_ERROR = auto()
    CLEAR_LEVEL_SUCCESS = auto()
    CLEAR_LEVEL_ERROR = auto()
    HELP = auto()
    QUEUE_SUCCESS = auto()

class View:
    def __init__(self, bot):
        self.bot = bot
    
    def output(self, message, source):
        try:
            self.bot.ws.send_message(message)
        except:
            pass