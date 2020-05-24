from .connection import Function


class KotlinFunction(Function):
    """Connection to the group kotlin to insert and output the chat elements"""

    def __init__(self):
        super(KotlinFunction, self).__init__()

    def insert_data(self, cbor):
        """adds a new chat element as cbor

                Tested and works!"""
        self.insert_event(cbor)

    def get_usernames_and_feed_id(self):
        """returns all current usernames with the corresponding feed id

                Tested and works!"""
        return self._handler.get_usernames_and_feed_id()

    def get_all_entries_by_feed_id(self, feed_id):
        """returns all elements with the corresponding feed id, thus all events of a user

                Tested and works!"""
        return self._handler.get_all_entries_by_feed_id(feed_id)

    def get_all_kotlin_events(self):
        """returns all existing kotlin elements that are in the database

                Tested and works!"""
        return self._handler.get_all_kotlin_events()

    def get_last_kotlin_event(self):
        """returns only the last added kotlin element

                Tested and works!"""
        return self._handler.get_last_kotlin_event()
