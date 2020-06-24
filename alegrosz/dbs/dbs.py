import os
import sqlite3

from flask import g


# połączenie z baza danych:
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db_abs_path = os.path.dirname(os.path.realpath(__file__))
        db_path = os.path.join(db_abs_path, 'alegrosz.db')

        db = g._database = sqlite3.connect(db_path)
    return db