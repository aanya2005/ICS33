from .query_handling import executing_query
from p2app.events import *
import sqlite3
from typing import Union


def region_search(connection,region_code,local_code,name):
    """Returns queries for region search."""
    # Creating queries
    query = 'SELECT * FROM region WHERE True '
    if region_code and not name and not local_code:
        query += 'AND region_code = (?);'
        cursor = connection.execute(query, (region_code,))
    elif local_code and not region_code and not name:
        query += 'AND local_code = (?);'
        cursor = connection.execute(query, (local_code,))
    elif name and not region_code and not local_code:
        query += 'AND name = (?);'
        cursor = connection.execute(query, (name,))
    elif name and region_code and local_code:
        query += 'AND region_code = (?) AND local_code = (?) AND name = (?);'
        cursor = connection.execute(query,(region_code,local_code,name))
    elif name and region_code:
        query += 'AND region_code = (?) AND name = (?);'
        cursor = connection.execute(query,(region_code,name))
    elif region_code and local_code:
        query += 'AND region_code = (?) AND local_code = (?);'
        cursor = connection.execute(query,(region_code,local_code))
    elif name and local_code:
        query += 'AND local_code = (?) AND name = (?);'
        cursor = connection.execute(query,(local_code,name))
    return cursor


def region_load(connection, region_id):
    """Returns all information about selected region."""
    query = 'SELECT region_id, region_code, local_code, name,continent_id, country_id,wikipedia_link, keywords from region WHERE region_id = (?)'
    cursor = connection.execute(query, (region_id,))
    return cursor


def region_new_save(event: SaveNewRegionEvent, connection: sqlite3.Connection)-> Union[RegionSavedEvent, SaveRegionFailedEvent]:
    """Creates a new region with all information provided."""
    info_tuple = event.region()
    region_code = info_tuple[1]
    local_code = info_tuple[2]
    name = info_tuple[3]
    continent_id = info_tuple[4]
    country_id = info_tuple[5]
    wikipedia_link = info_tuple[6]
    keywords = info_tuple[7]
    # Creating SQL queries
    if keywords and wikipedia_link:
        query = 'INSERT INTO region (region_code, local_code, name,continent_id, country_id,wikipedia_link, keywords) VALUES ((:region_code),(:local_code),(:name),(:continent_id),(:country_id),(:wikipedia_link),(:keywords));'
        params={'region_code': region_code, 'local_code': local_code,
                                 'name': name, 'continent_id': continent_id,
                                 'country_id': country_id, 'wikipedia_link': wikipedia_link,
                                 'keywords': keywords}
        cursor = executing_query(connection, query, params)
    # accounting for NULL values
    elif not keywords and wikipedia_link:
        query = 'INSERT INTO region(region_code, local_code, name,continent_id, country_id,wikipedia_link, keywords) VALUES ((:region_code),(:local_code),(:name),(:continent_id),(:country_id),(:wikipedia_link),NULL);'
        params={'region_code': region_code, 'local_code': local_code,
                                 'name': name, 'continent_id': continent_id,
                                 'country_id': country_id,
                                 'wikipedia_link': wikipedia_link}
        cursor = executing_query(connection, query, params)
    elif keywords and not wikipedia_link:
        query = f"INSERT INTO region (region_code, local_code, name,continent_id, country_id,wikipedia_link, keywords) VALUES ((:region_code),(:local_code),(:name),(:continent_id),(:country_id),NULL,(:keywords));"
        params ={'region_code': region_code, 'local_code': local_code,
                                 'name': name, 'continent_id': continent_id,
                                 'country_id': country_id, 'keywords': keywords}
        cursor = executing_query(connection, query, params)
    elif not keywords and not wikipedia_link:
        query = f"INSERT INTO region (region_code, local_code, name,continent_id, country_id,wikipedia_link, keywords) VALUES ((:region_code),(:local_code),(:name),(:continent_id),(:country_id),NULL,NULL);"
        params = {'region_code': region_code, 'local_code': local_code,
                                 'name': name, 'continent_id': continent_id,
                                 'country_id': country_id}
        cursor = executing_query(connection, query, params)
    if isinstance(cursor, sqlite3.Cursor):
        connection.commit()
        result = RegionSavedEvent(info_tuple)
    else:
        connection.rollback()
        f_message = f"Insert failed because {cursor}"
        result = SaveRegionFailedEvent(f_message)
    return result


def region_edit(event: SaveRegionEvent, connection: sqlite3.Connection) -> Union[RegionSavedEvent, SaveRegionFailedEvent]:
    """Creates changes unto the selected region."""
    info_tuple = event.region()
    (region_id,region_code,local_code,name,continent_id,country_id,
     wikipedia_link,keywords) = info_tuple
    # Creating SQL queries
    query = 'UPDATE region SET region_code = (:region_code),local_code =(:local_code), name = (:name),continent_id =(:continent_id),country_id =(:country_id),'
    if wikipedia_link and keywords:
        query += 'wikipedia_link = (:wikipedia_link),keywords = (:keywords) WHERE region_id = (:region_id);'
        params ={'region_code': region_code, 'local_code': local_code, 'name': name,
                            'continent_id': continent_id, 'country_id': country_id,
                            'wikipedia_link': wikipedia_link, 'keywords': keywords,
                            'region_id': region_id}
        cursor = executing_query(connection, query, params)
    # Accounting for NULL values
    if not wikipedia_link and keywords:
        query += 'wikipedia_link = NULL, keywords = (:keywords) WHERE region_id = (:region_id);'
        params={'region_code': region_code, 'local_code': local_code,
                            'name': name, 'continent_id': continent_id,
                            'country_id': country_id, 'keywords': keywords,
                            'region_id': region_id}
        cursor = executing_query(connection, query, params)
    if not keywords and wikipedia_link:
        query += 'wikipedia_link = (:wikipedia_link),keywords = NULL WHERE region_id = (:region_id);'
        params={'region_code': region_code, 'local_code': local_code,
                            'name': name, 'continent_id': continent_id,
                            'country_id': country_id,
                            'wikipedia_link': wikipedia_link, 'region_id': region_id}
        cursor = executing_query(connection, query, params)
    if not keywords and not wikipedia_link:
        query += 'wikipedia_link = NULL,keywords = NULL WHERE region_id = (:region_id);'
        params={'region_code': region_code, 'local_code': local_code,
                            'name': name, 'continent_id': continent_id,
                            'country_id': country_id, 'region_id': region_id}
        cursor = executing_query(connection, query, params)
    if isinstance(cursor, sqlite3.Cursor):
        connection.commit()
        result = RegionSavedEvent(info_tuple)
    else:
        connection.rollback()
        f_message = f"Update failed because {cursor}"
        result = SaveRegionFailedEvent(f_message)
    return result