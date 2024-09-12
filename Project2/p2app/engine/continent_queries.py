import sqlite3
from typing import Union
from .query_handling import executing_query
from p2app.events import *


def continent_search(connection, continent_code=None,name=None):
    """Returns queries for continent search."""
    query = 'SELECT * FROM continent WHERE True '
    if continent_code and not name:
        query += 'AND continent_code = (?);'
        cursor = connection.execute(query, (continent_code,))
    elif name and not continent_code:
        query += 'AND name = (?);'
        cursor = connection.execute(query, (name,))
    elif name and continent_code:
        query += 'AND continent_code = (:continent_code) AND name = (:name);'
        cursor = connection.execute(query,
                                         {'name': name, 'continent_code': continent_code})
    return cursor

def continent_load(connection, continent_id):
    """Returns all information about selected continent."""
    query = 'SELECT continent_id,continent_code,name from continent WHERE continent_id = (?)'
    y = connection.execute(query, (continent_id,))
    return y


def continent_new_save(event: SaveNewContinentEvent, connection: sqlite3.Connection) -> Union[
        ContinentSavedEvent, SaveContinentFailedEvent]:
    """Creates a new continent with all information provided."""
    info_tuple = event.continent()
    ids, code, name = info_tuple
    # Creating SQL statement
    statement = ("INSERT INTO continent (continent_code, name) VALUES(?, ?);")
    params = (code, name)
    cursor = executing_query(connection, statement, params)
    if isinstance(cursor, sqlite3.Cursor):
        connection.commit()
        result = ContinentSavedEvent(info_tuple)
    else:
        connection.rollback()
        f_message = f"Insert failed because {cursor}"
        result = SaveContinentFailedEvent(f_message)
    return result


def continent_edit(event: SaveContinentEvent, connection: sqlite3.Connection) -> Union[ContinentSavedEvent, SaveContinentFailedEvent]:
    """Creates changes unto the selected continent."""
    info_tuple = event.continent()
    ids, code, name = info_tuple
    # Creating query
    statement = ("UPDATE continent "
                 "SET continent_code = ?, "
                 "name = ? "
                 "WHERE continent_id = ?")
    params = (code, name, ids)
    cursor = executing_query(connection, statement, params)

    if isinstance(cursor, sqlite3.Cursor):
        connection.commit()
        result = ContinentSavedEvent(info_tuple)
    else:
        connection.rollback()
        f_message = f"Update failed because {cursor}"
        result = SaveContinentFailedEvent(f_message)
    return result
