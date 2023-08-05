import sqlite3
from typing import List, Union


def migrate(connection: sqlite3.Connection,
            current_migrations: Union[List[int], None] = None):
    connection.execute(
        'CREATE TABLE IF NOT EXISTS table1 ('
        '    table1_id INTEGER PRIMARY KEY,'
        '    name TEXT NOT NULL UNIQUE'
        ')')
