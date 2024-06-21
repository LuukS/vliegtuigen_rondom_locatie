from config import Config
import mysql.connector

dbConnected = False

class Connection:
    def __init__(self):
        global dbConnected
        try:
            self.db=mysql.connector.connect(
                host=Config.DATABASE_CONFIG['host'],
                port=Config.DATABASE_CONFIG['port'],
                user=Config.DATABASE_CONFIG['user'],
                password=Config.DATABASE_CONFIG['password'],
                database=Config.DATABASE_CONFIG['dbname']
            )
            dbConnected = True
        except:
            print("Database kon niet benaderd worden")

    def isConnected(self):
        global dbConnected
        return dbConnected

    def commit(self):
        self.db.cursor().execute("COMMIT")

    def close(self):
        self.db.close()