
from TwitchWebsocket import TwitchWebsocket
import random, time, json, logging, re

from Log import Log
Log(__file__)

from Settings import Settings
from Database import Database
from App import App
from View import View
from View import MessageSource

class Level:
    # Simple data structure to store weight and time of a user who chatted.
    def __init__(self, user, code, weight):
        self.user = user
        self.code = code
        self.weight = weight

class MMLevelQueue:
    def __init__(self, db):
        self.host = None
        self.port = None
        self.chan = None
        self.nick = None
        self.auth = None
        self.capability = "tags"
        self.db = db
        self.app = None
        self.view = View(self)
        
        # Fill previously initialised variables with data from the settings.txt file
        Settings(self)

    def start(self):
        self.ws = TwitchWebsocket(host=self.host, 
                                  port=self.port,
                                  chan=self.chan,
                                  nick=self.nick,
                                  auth=self.auth,
                                  callback=self.message_handler,
                                  capability=self.capability,
                                  live=True)
        self.ws.start_nonblocking()

    def stop(self):
        try:
            self.ws.join()
        except AttributeError:
            # If self.ws has not yet been instantiated. 
            # In this case we have essentially already stopped
            pass

    # Used from GUI
    def set_login_settings(self, host, port, chan, nick, auth):
        self.host = host
        self.port = port
        self.chan = chan
        self.nick = nick
        self.auth = auth
    
    def set_settings(self, host, port, chan, nick, auth, allowed_ranks, allowed_people):
        self.set_login_settings(host, port, chan, nick, auth)
        self.allowed_ranks = allowed_ranks
        self.allowed_people = allowed_people

    def message_handler(self, m):
        try:
            if m.type == "366":
                self.app.now_running()
            
            if m.type == "PRIVMSG":
                if m.message.startswith("!addlevel"):
                    self.handle_add_level(m)
                elif m.message.startswith("!nextlevel") and self.check_permissions(m):
                    self.handle_next_level()
                elif m.message.startswith(("!level", "!current")):
                    self.handle_current_level()
                elif m.message.startswith("!clearlevel") and self.check_permissions(m):
                    self.handle_clear_level()
                elif m.message.startswith(("!levelhelp", "!helplevel")):
                    self.handle_help()
                elif m.message.startswith(("!queue")):
                    self.handle_queue(m)

        except Exception as e:
            logging.exception(e)

    def check_permissions(self, m):
        for rank in self.allowed_ranks:
            if rank in m.tags["badges"]:
                return True
        for name in self.allowed_people:
            if m.user.lower() == name.lower():
                return True
        return False
    
    def handle_add_level(self, m):
        # Get the full message
        message = m.message
        # Split by space
        message_list = message.split()
        if len(message_list) != 2:
            self.view.output("The command is !addlevel XXX-XXX-XXX.", MessageSource.ADD_LEVEL_ERROR)
        else:
            # Get the code
            code = message_list[-1].upper()
            # Check if the code matches the correct format of XXX-XXX-XXX
            if re.match("[A-Z|0-9]{3}-[A-Z|0-9]{3}-[A-Z|0-9]{3}", code):
                # Add the level. It might return a warning
                source = self.db.add_level(m.tags["display-name"], code)
                if source == MessageSource.ADD_LEVEL_WARNING:
                    self.view.output("Your previous code has been overridden.", MessageSource.ADD_LEVEL_WARNING)
                elif source == MessageSource.ADD_LEVEL_ERROR:
                    self.view.output("Your level is already in the #1 slot.", MessageSource.ADD_LEVEL_ERROR)
                elif source == MessageSource.ADD_LEVEL_SUCCESS:
                    self.view.output("Your code has been added.", MessageSource.ADD_LEVEL_SUCCESS)
                self.app.update_levels()
            else:
                self.view.output("The format for the code is: XXX-XXX-XXX.", MessageSource.ADD_LEVEL_ERROR)
    
    def handle_next_level(self):
        # Pop the lowest index
        self.db.pop()

        # Update the GUI
        self.app.update_levels()

        # Get the new level
        current = self.db.get_current_level()
        if len(current) == 0:
            self.view.output("No levels currently in queue.", MessageSource.NEXT_LEVEL_ERROR)
            return
        
        # Send output to chat
        user = current[0][0]
        code = current[0][1]
        self.view.output(f"{user}'s level with code {code} is up next!", MessageSource.NEXT_LEVEL_SUCCESS)

    def handle_current_level(self):
        # Get the current level
        current = self.db.get_current_level()
        if len(current) == 0:
            self.view.output("There is no current level.", MessageSource.CURRENT_LEVEL_ERROR)
            return

        self.view.output(f"Creator: {current[0][0]}, Code: {current[0][1]}", MessageSource.CURRENT_LEVEL_SUCCESS)

    def handle_clear_level(self):
        # Clear the database of levels
        self.db.clear()

        # Send to chat
        self.view.output(f"The levels have been cleared.", MessageSource.CLEAR_LEVEL_SUCCESS)

        # Update the GUI
        self.app.update_levels()
    
    def handle_help(self):       
        self.view.output(f"Commands: !addlevel XXX-XXX-XXX to add your level, !current/!level to get the code of the current level. !queue to find your placement in the queue", MessageSource.HELP)
    
    def handle_queue(self, m):
        # Get all the data from the levels
        data = self.db.get_levels()

        user = m.tags["display-name"]
        #user = str(random.randint(0, 10))
        for index, tup in enumerate(data):
            if tup[0] == user:
                self.view.output(f"@{user} , You are #{index+1} in the queue with your level: {tup[1]}.", MessageSource.QUEUE_SUCCESS)
                return
        
        self.view.output(f"@{user} , You are currently not in the queue.", MessageSource.QUEUE_SUCCESS)

if __name__ == "__main__":
    db = Database()
    bot = MMLevelQueue(db)
    app = App(bot, db)
    bot.app = app
