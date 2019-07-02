
import sqlite3, logging, random, time
logger = logging.getLogger(__name__)

from View import MessageSource

class Database:
    # Using sqlite for simplicity, even though it doesn't store my dict in a convenient matter.
    def __init__(self):
        self.create_db()
    
    def create_db(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Levels (
            user TEXT PRIMARY KEY,
            code TEXT,
            id INTEGER
        )
        """
        logger.debug("Creating Database...")
        self.execute(sql)
        logger.debug("Database created.")
        sql = """
        CREATE TABLE IF NOT EXISTS LevelClear (
            time INTEGER
        )
        """
        logger.debug("Creating Database...")
        self.execute(sql)
        logger.debug("Database created.")

        clear_t = self.get_clear_time()
        if len(clear_t) == 0:
            self.set_clear_time()

    def execute(self, sql, values=None, fetch=False):
        with sqlite3.connect("Levels.db") as conn:
            cur = conn.cursor()
            if values is None:
                cur.execute(sql)
            else:
                cur.execute(sql, values)
            conn.commit()
            if fetch:
                return cur.fetchall()

    def add_level(self, user, code):
        # Is the user #1 in the queue?
        num_1_user = self.execute("SELECT user FROM Levels WHERE id = (SELECT MIN(id) FROM Levels)", fetch=True)
        if len(num_1_user) > 0 and num_1_user[0][0] == user:
            return MessageSource.ADD_LEVEL_ERROR

        warning = self.execute("SELECT SUM(user) FROM Levels WHERE user = ?;", values=(user,), fetch=True)[0][0] != None
        if warning:
            self.execute("DELETE FROM Levels WHERE user = ?;", values=(user,))
        self.execute("INSERT INTO Levels VALUES(?, ?, ?)", values=(user, code, self.get_new_id()))
        return MessageSource.ADD_LEVEL_WARNING if warning else MessageSource.ADD_LEVEL_SUCCESS

    def get_new_id(self):
        return self.execute("SELECT MAX(id)+1 FROM Levels;", fetch=True)[0][0] or 1

    def pop(self):
        self.execute("DELETE FROM Levels WHERE id = (SELECT MIN(id) FROM Levels)")

    def get_current_level(self):
        return self.execute("SELECT user, code FROM Levels ORDER BY id LIMIT 1;", fetch=True)

    def get_levels(self):
        return self.execute("SELECT user, code FROM Levels ORDER BY id;", fetch=True)

    def get_clear_time(self):
        return self.execute("SELECT time FROM LevelClear;", fetch=True)

    def clear(self):
        # Deletes all items
        self.execute("DELETE FROM Levels;")
        self.execute("DELETE FROM LevelClear;")
        self.set_clear_time()

    def set_clear_time(self):
        self.execute("INSERT INTO LevelClear VALUES(?);", values=(round(time.time()),))
