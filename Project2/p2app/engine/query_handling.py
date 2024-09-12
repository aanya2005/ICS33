import sqlite3
from typing import Union

def executing_query(conn: sqlite3.Connection, query: str, params) -> Union[sqlite3.Cursor, str]:
    """Executes a parametrized SQL query on the SQLite connection."""
    try:
        cur = conn.execute(query, params)
    except sqlite3.Error as e:
        # If an error occurs during query execution, return the error message
        err_msg = ' '.join(e.args)
        cur = f'{err_msg}'
    return cur