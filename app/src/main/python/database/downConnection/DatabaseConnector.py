from database.DatabaseHandler import DatabaseHandler as dh
from functions.log import create_logger

logger = create_logger('DatabaseConnector')


class DatabaseConnector:

    def __init__(self):
        self.__handler = dh()

    def add_event(self, event_as_cbor):
        if self.__handler.add_to_db(event_as_cbor):
            return True

    def get_current_seq_no(self, feed_id):
        return self.__handler.get_current_seq_no(feed_id)

    def get_event(self, feed_id, seq_no):
        return self.__handler.get_event(feed_id, seq_no)

    def get_current_event(self, feed_id):
        return self.__handler.get_current_event_as_cbor(feed_id)
