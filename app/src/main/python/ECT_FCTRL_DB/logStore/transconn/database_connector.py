from ..database.database_handler import DatabaseHandler as dataBaseHandler
from ..funcs.log import create_logger
from ..verific.verify_insertion import Verification

logger = create_logger('DatabaseConnector')
"""The database connector allows the network layer to access database functionality.

It is meant to be used mostly by logMerge and logSync for their purposes, however, others should feel free to
use it as well.
"""


class DatabaseConnector:
    """Database handler should be implemented by the network connection groups.

    It has the private fields of a database handler to access the necessary database functionality.
    """

    def __init__(self):
        self.__handler = dataBaseHandler()
        self.__verifier = Verification()

    def add_event(self, event_as_cbor):
        """"Add a cbor event to the two databases.

        Calls each the byte array handler as well as the event handler to insert the event in both databases
        accordingly. Gets called both by database connector as well as the function connector. Returns 1 if successful,
        otherwise -1 if any error occurred.
        @:parameter event_as_cbor: The new cbor event to be added
        @:returns 1 if successful, -1 if any error occurred
        """
        return self.__handler.add_to_db(event_as_cbor, False)

    def get_current_seq_no(self, feed_id):
        """"Return the current sequence number of a given feed_id, returns an integer with the currently largest
        sequence number for the given feed. Returns -1 if there is no such feed_id in the database.

        @:parameter feed_id: The feed id for which one wants to retrieve the sequence number
        @:returns -1 if any error occurred or the feed id is not in the database, otherwise the current sequence number.
        """
        return self.__handler.get_current_seq_no(feed_id)

    def get_event(self, feed_id, seq_no):
        """"Return a specific cbor event to the callee with the input feed_id and sequence number. Returns None if
        there is no such entry.

        @:parameter feed_id: The feed id for which one wants to retrieve the event
        @:parameter seq_no: The sequence id for which one wants to retrieve the event
        @:returns None if no such event exists or an error occured or the event.
        """
        return self.__handler.get_event(feed_id, seq_no)

    def get_current_event(self, feed_id):
        """Return the newest (the one with the highest sequence number) cbor event for a feed_id. Returns None if
        there is no such feed_id in the database.

        @:parameter feed_id: The sequence id for which one wants to retrieve the newest event
        @:returns None if no such event exists or an error occured or the event.
        """
        return self.__handler.get_current_event_as_cbor(feed_id)

    def get_all_feed_ids(self):
        """Return all current feed ids in the database.

        @:returns None if no feed id is in the database or an error occured or a list of feed ids.
        """
        return self.__handler.get_all_feed_ids()

    def check_incoming(self, feed_id, is_master=False):
        """"Whether an incoming feed id is whitelisted, bool tells us whether it is a master feed or not.

        @:parameter feed_id: The feed id for which one wants to check if it is whitelisted
        @:parameter is_master: (optional) Whether the feed id provided is from a master feed
        @:returns True if this feed id is whitelisted or False if not
        """
        return self.__verifier.check_incoming(feed_id, is_master)

    def check_outgoing(self, feed_id):
        """"Whether an outgoing feed id is whitelisted, bool tells us whether it is a master feed or not.

        @:parameter feed_id: The feed id for which one wants to check if it is whitelisted
        @:returns True if this feed id is whitelisted or False if not
        """
        return self.__verifier.check_outgoing(feed_id)

    def get_master_feed_id(self):
        return self.__handler.get_host_master_id()