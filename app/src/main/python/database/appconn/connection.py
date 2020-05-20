from ..database.database_handler import DatabaseHandler


class Function:
    """To be used when there has not been a specific table implemented for a group:"""

    def __init__(self):
        self._handler = DatabaseHandler()

    def insert_event(self, cbor):
        """"Add a cbor event to the two databases.

        Calls each the byte array handler as well as the event handler to insert the event in both databases
        accordingly. Gets called both by database connector as well as the function connector. Returns 1 if successful,
        otherwise -1 if any error occurred.
        """
        self._handler.add_to_db(event_as_cbor=cbor, app=True)

    def get_current_seq_no(self, feed_id):
        """"Return the current sequence number of a given feed_id, returns an integer with the currently largest
                        sequence number for the given feed. Returns -1 if there is no such feed_id in the database."""
        return self._handler.get_current_seq_no(feed_id)

    def get_event(self, feed_id, seq_no):
        """"Return a specific cbor event to the callee with the input feed_id and sequence number. Returns None if
                        there is no such entry."""
        return self._handler.get_event(feed_id, seq_no)

    def get_current_event(self, feed_id):
        """"Return the newest (the one with the highest sequence number) cbor event for a feed_id. Returns None if
                        there is no such feed_id in the database."""
        return self._handler.get_current_event_as_cbor(feed_id)

    def get_all_feed_ids(self):
        """"Return all current feed ids in the database."""
        return self._handler.get_all_feed_ids()
