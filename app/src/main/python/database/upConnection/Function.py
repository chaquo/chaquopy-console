from database.database.DatabaseHandler import DatabaseHandler


class Function:

    def __init__(self):
        self.__handler = DatabaseHandler()

    def get_feed_ids(self):
        pass

    def insert_event(self, cbor):
        self.__handler.add_to_db(event_as_cbor=cbor)

    def get_event(self, feedId, Hash):
        pass

    def get_all_events_since(self, feedId, Hash):
        pass

    def get_full_feed(self, feedId):
        pass
