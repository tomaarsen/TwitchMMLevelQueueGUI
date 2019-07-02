
import logging

from TwitchWebsocket.Message import Message

from Settings import Settings
from Log import Log
Log(__file__)

# Modules
import tkinter as tk
import tkinter.scrolledtext as tkst
import tkinter.font as tkFont
import time, json
from datetime import datetime
from functools import reduce
import threading

class App(threading.Thread):

    # Initialise the thread
    def __init__(self, bot, db):
        threading.Thread.__init__(self)
        
        # Attributes
        self.bot = bot
        self.db = db
        self.running = False

        # Start the thread
        self.start()

    # Quit properly
    def callback(self):
        # Quit the GUI
        self.root.quit()
        # Join the bot thread
        self.bot.stop()
        # This terminates the entire program

    # Clear output field
    def clear(self):
        self.txt.delete("1.0", tk.END)

    # Hide the OAUTH password
    def hide(self):
        if self.login_entries[4]['state'] == 'normal':
            self.oauth = self.login_entries[4].get()
            self.login_entries[4].delete(0, tk.END)
            self.login_entries[4].insert(0, "*" * 44)
            self.login_entries[4].configure(state='readonly')
        else:
            self.login_entries[4].configure(state='normal')
            self.login_entries[4].delete(0, tk.END)
            self.login_entries[4].insert(0, self.oauth)
    
    def now_running(self):
        self.running = True

    def update_login(self):
        # Get settings
        login = [entry.get() for entry in self.login_entries]
        # Set the settings on the bot
        chan = login[2] if len(login[2]) > 0 and login[2][0] == "#" else "#" + login[2]
        try:
            port = int(login[1])
        except:
            port = 0
        if self.login_entries[4]['state'] == 'normal':
            auth = login[4]
        else:
            auth = self.oauth

        self.bot.set_login_settings(login[0], port, chan, login[3], auth)

    def next_level(self):
        # Pick the next level
        self.bot.handle_next_level()

    def run(self):
        self.login_dict = {"Host": self.bot.host, "Port":self.bot.port, "Chan": self.bot.chan.replace("#", ""), "User": self.bot.nick, "Auth": self.bot.auth}

        # Set up GUI
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.resizable(0, 1)
        self.root.minsize(width=283, height=205)
        self.root.title("Twitch Bot GUI")
        self.root.grid_rowconfigure(6, weight=1)
        
        self.login_entries = []
        self.oauth = ""
        
        # Handle Run/Stop button functionality
        def run_stop():
            if self.run_stop_button['text'] == "Run":
                self.update_login()
                self.bot.start()
            else:
                self.bot.stop()
                self.running = False
            if self.run_stop_button['text'] == "Stop":
                self.run_stop_button.configure(text="Run")
            else:
                self.run_stop_button.configure(text="Stop")

        self.m = max([len(str(self.login_dict[i])) for i in self.login_dict]) + 1

        # Fields for the GUI main page
        for x, i in enumerate(self.login_dict):
            if x == 4:
                self.hide_button = tk.Button(self.root, text=i, command=self.hide)
                self.hide_button.grid(row=x, padx=(12, 4))
                self.hide_button.config(width=4)
            else:
                tk.Label(self.root, text=i + ":").grid(row=x, padx=(12, 4))
            e = tk.Entry(self.root, width=self.m)
            e.grid(row=x, column=1, sticky="W", columnspan=5, pady=2)
            e.insert(0, self.login_dict[i])
            self.login_entries.append(e)
        
        # Hide the OAUTH password.
        self.hide()

        # Run/Stop Button
        self.run_stop_button = tk.Button(self.root, text='Run', command=run_stop)
        self.run_stop_button.grid(row=len(self.login_dict), column=0, pady=4, padx=(9, 0))
        self.run_stop_button.config(width=4)

        # Clear, Vote and Settings buttons
        tk.Button(self.root, text="{:^18}".format("Move to Next Level"), command=self.next_level).grid(row=len(self.login_dict), column=1, columnspan=2, pady=4)
        self.clear_button = tk.Button(self.root, text='Clear', command=self.clear_db)
        self.clear_button.grid(row=len(self.login_dict), column=5, pady=4)
        #tk.Button(self.root, text='Settings', command=self.settings).grid(row=len(self.login_dict), column=5, pady=4, padx=(74, 25))

        # Output field
        self.txt = tkst.ScrolledText(self.root, undo=True, borderwidth=3, relief="groove", width=self.m, height=17)
        self.txt.config(font=('consolas', '8'), undo=True, wrap='word') #font=('consolas', '12')
        self.txt.grid(column=0, padx=(10, 6), pady=(2, 5), sticky="news", columnspan=6)

        # Configure bold font for specific output messages to use
        self.bold_font = tkFont.Font(self.txt, self.txt.cget("font"))
        self.bold_font.configure(weight="bold")
        self.txt.tag_configure("bold", font=self.bold_font)
        
        self.update_levels()

        # GUI Loop
        self.root.mainloop()
    
    def update_levels(self):
        # Get all levels
        level_data = self.db.get_levels()

        # Clear out
        self.txt.delete("1.0", tk.END)
        # Insert headers
        self.txt.insert(tk.END, "ID : Level's Creator     : Code\n", "bold")

        # Insert non-current levels
        for index, tup in enumerate(level_data):
            if index == 0:
                self.txt.insert(tk.END, f"{index + 1: >2} : {tup[0]: <19} : {tup[1]: <12} \n", "bold")
            else:
                self.txt.insert(tk.END, f"{index + 1: >2} : {tup[0]: <19} : {tup[1]: <12} \n")

        # Update clear time
        clear_time = self.db.get_clear_time()
        if clear_time:
            self.clear_button.configure(text="Clear: " + time.strftime('%b-%d %H:%M', time.localtime(clear_time[0][0])))
        
    def clear_db(self):
        self.db.clear()
        self.update_levels()
