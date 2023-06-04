import sqlite3
from opera_cripto import ORIGIN_DATA

class Conexion:
    def __init__(self, query, params=()):
        self.conn = sqlite3.connect(ORIGIN_DATA)
        self.cur = self.conn.cursor()
        self.res = self.cur.execute(query, params)
