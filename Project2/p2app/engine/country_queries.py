from .query_handling import executing_query
from p2app.events import *
import sqlite3
from typing import Union


def country_search(connection, country_code, name):
    """Returns queries for country search."""
    query = 'SELECT * FROM country WHERE True '
    if country_code and not name:
        query += 'AND country_code = (?);'
        cursor = connection.execute(query, (country_code,))
    elif name and not country_code:
        query += f"AND name = (?);"
        cursor = connection.execute(query, (name,))
    elif name and country_code:
        query += 'AND country_code = (:country_code) AND name = (:name);'
        cursor = connection.execute(query,
                                    {'name': name, 'country_code': country_code})
    return cursor


def country_load(connection, country_id):
    """Returns all information about selected country."""
    query = 'SELECT country_id,country_code,name,continent_id,wikipedia_link,keywords from country WHERE country_id = (?)'
    cursor = connection.execute(query, (country_id,))
    return cursor


def country_new_save(event: SaveNewCountryEvent, connection: sqlite3.Connection) -> Union[CountrySavedEvent, SaveCountryFailedEvent]:
    """Creates a new country with all information provided."""
    info = event.country()
    code = info[1]
    name = info[2]
    continent_id = info[3]
    wikipedia_link = info[4]
    keywords = info[5]
    # Creating SQL query
    if keywords:
        statement = ('INSERT INTO country (country_code, name, continent_id, wikipedia_link, keywords) VALUES(?, ?, ?, ?, ?);')
        params = (code, name, continent_id, wikipedia_link, keywords)
        cursor = executing_query(connection, statement, params)
    # Accounting for NULL value
    else:
        statement = ('INSERT INTO country (country_code, name, continent_id, wikipedia_link, keywords) VALUES(?, ?, ?, ?, NULL);')
        params = (code, name, continent_id, wikipedia_link)
        cursor = executing_query(connection, statement, params)

    # Check if the insertion was successful and return the appropriate event
    if isinstance(cursor, sqlite3.Cursor):
        connection.commit()
        result = CountrySavedEvent(info)
    else:
        connection.rollback()
        f_message = f"Insert failed because {cursor}"
        result = SaveCountryFailedEvent(f_message)
    return result


def country_edit(event: SaveCountryEvent, connection: sqlite3.Connection) -> Union[CountrySavedEvent, SaveCountryFailedEvent]:
    """Creates changes unto the selected country."""
    info = event.country()
    info_id,code,name,continent_id,wikipedia_link,keywords = info
    # Creating query
    query = 'UPDATE country SET country_code =(:country_code), name = (:name), continent_id =(:continent_id),wikipedia_link = (:wikipedia_link),'
    if keywords:
        query += 'keywords = (:keywords) WHERE country_id = (:country_id);'
        params = {'country_code': code, 'name': name,
                                   'continent_id': continent_id,
                                   'wikipedia_link': wikipedia_link, 'keywords': keywords,
                                   'country_id': info_id}
        cursor = executing_query(connection, query, params)
    # Accounting for NULL keyword
    if not keywords:
        query += 'keywords = NULL WHERE country_id = (:country_id);'
        params ={'country_code': code, 'name': name,
                                   'continent_id': continent_id,
                                   'wikipedia_link': wikipedia_link, 'country_id': info_id}
        cursor = executing_query(connection, query, params)
    if isinstance(cursor, sqlite3.Cursor):
        connection.commit()
        result = CountrySavedEvent(info)
    else:
        connection.rollback()
        f_message = f"Update failed because {cursor}"
        result = SaveCountryFailedEvent(f_message)
    return result