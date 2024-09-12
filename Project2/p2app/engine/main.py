# p2 app/engine/main.py
#
# ICS 33 Spring 2024
# Project 2: Learning to Fly
#
# An object that represents the engine of the application.
#
# This is the outermost layer of the part of the program that you'll need to build,
# which means that YOU WILL DEFINITELY NEED TO MAKE CHANGES TO THIS FILE.
import sqlite3
from .continent_queries import continent_search, continent_load, continent_new_save, continent_edit
from .country_queries import country_search, country_load,country_new_save, country_edit
from .region_queries import region_search, region_load, region_new_save, region_edit
from p2app.events import *


class Engine:
    """An object that represents the application's engine, whose main role is to
    process events sent to it by the user interface, then generate events that are
    sent back to the user interface in response, allowing the user interface to be
    unaware of any details of how the engine is implemented.
    """

    def __init__(self):
        """Initializes the engine"""
        self.connection = None


    def process_event(self, event):
        """A generator function that processes one event sent from the user interface,
        yielding zero or more events in response."""
        if isinstance(event, OpenDatabaseEvent):
            try:
                database_path = event.path()
                self.connection = sqlite3.connect(database_path)
                self.connection.execute('PRAGMA foreign_keys = ON;')
                cursor = self.connection.cursor()
                cursor.execute("SELECT * FROM continent")
                cursor.execute("SELECT * FROM country")
                cursor.execute("SELECT * FROM region")
                cursor.close()
                yield DatabaseOpenedEvent(database_path)
            except Exception as e:
                yield DatabaseOpenFailedEvent(f"Cannot open database: {e}")

        elif isinstance(event, QuitInitiatedEvent):
            yield EndApplicationEvent()

        elif isinstance(event, CloseDatabaseEvent):
            yield DatabaseClosedEvent()

        # Handling continent edits.
        elif isinstance(event, StartContinentSearchEvent):
            try:
                continent_code = event.continent_code()
                name = event.name()
                cursor = continent_search(self.connection,continent_code,name)
                while cursor:
                    obj = cursor.fetchone()
                    if obj is None:
                        break
                    else:
                        continent_ids, continent_codes, names = obj
                        info = continent_info(continent_ids, continent_codes, names)
                        yield ContinentSearchResultEvent(info)
            except IndexError:
                yield ()

        elif isinstance(event, LoadContinentEvent):
            continent_id = event.continent_id()
            cursor = continent_load(self.connection, continent_id)
            obj = cursor.fetchone()
            continent_ids, continent_codes, names = obj
            info = continent_info(continent_ids, continent_codes, names)
            yield ContinentLoadedEvent(info)

        elif isinstance(event,SaveNewContinentEvent):
            result = continent_new_save(event, self.connection)
            yield result

        elif isinstance(event, SaveContinentEvent):
            result = continent_edit(event, self.connection)
            yield result

        # Handling country edits
        elif isinstance(event, StartCountrySearchEvent):
            try:
                country_code = event.country_code()
                name = event.name()
                self.connection.cursor()
                cursor = country_search(self.connection,country_code,name)
                while cursor:
                    obj = cursor.fetchone()
                    if obj is None:
                        break
                    else:
                        country_ids,country_codes,names,continent_ids,wikipedia_link,keywords = obj
                        info = country_info(country_ids,country_codes,names,continent_ids,
                                            wikipedia_link,keywords)
                        yield CountrySearchResultEvent(info)
            except IndexError:
                yield ()

        elif isinstance(event,LoadCountryEvent):
            country_id = event.country_id()
            cursor = country_load(self.connection, country_id)
            obj = cursor.fetchone()
            country_ids, country_codes, names, continent_ids, wikipedia_link, keywords = obj
            info = country_info(country_ids, country_codes, names, continent_ids, wikipedia_link,
                                keywords)
            yield CountryLoadedEvent(info)

        elif isinstance(event,SaveNewCountryEvent):
            result = country_new_save(event, self.connection)
            yield result

        elif isinstance(event,SaveCountryEvent):
            result = country_edit(event, self.connection)
            yield result

        # Handling region events
        elif isinstance(event,StartRegionSearchEvent):
            try:
                region_code = event.region_code()
                name = event.name()
                local_code = event.local_code()
                self.connection.cursor()
                cursor = region_search(self.connection, region_code,local_code,name)
                while cursor:
                    obj = cursor.fetchone()
                    if obj is None:
                        break
                    else:
                        (region_ids,region_codes,local_code,names,continent_ids,country_ids,
                         wikipedia_link,keywords) = obj
                        region = region_info(region_ids,region_codes,local_code,names,continent_ids,
                                            country_ids,wikipedia_link,keywords)
                        yield RegionSearchResultEvent(region)
            except IndexError:
                yield ()

        elif isinstance(event,LoadRegionEvent):
            region_id = event.region_id()
            y = region_load(self.connection, region_id)
            obj = y.fetchone()
            (region_ids,region_codes,local_code,names,continent_ids,country_ids,
             wikipedia_link,keywords) = obj
            region =region_info(region_ids,region_codes,local_code,names,continent_ids,country_ids,
                         wikipedia_link,keywords)
            yield RegionLoadedEvent(region)

        elif isinstance(event, SaveNewRegionEvent):
            result = region_new_save(event, self.connection)
            yield result

        elif isinstance(event,SaveRegionEvent):
            result = region_edit(event, self.connection)
            yield result


def continent_info(continent_ids, continent_codes, names):
    """Saves the continent information into namedspace."""
    continent = Continent(continent_id = continent_ids,
                          continent_code = continent_codes,
                          name = names)
    return continent


def country_info(country_ids,country_codes,names,continent_ids,wikipedia_link,keywords):
    """Saves the country information into namedspace."""
    country = Country(country_id = country_ids, country_code = country_codes,
                      name = names, continent_id = continent_ids,
                      wikipedia_link = wikipedia_link, keywords = keywords)
    return country


def region_info(region_ids,region_codes,local_code,names,continent_ids,country_ids,
                         wikipedia_link,keywords):
    """Saves the region information into namedspace."""
    region = Region(region_id = region_ids, region_code = region_codes,
                    local_code = local_code, name = names,
                    continent_id = continent_ids, country_id = country_ids,
                    wikipedia_link = wikipedia_link, keywords = keywords)
    return region