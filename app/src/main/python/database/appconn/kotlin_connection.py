from .connection import Function

# TODO: Comment this class!

class KotlinFunction(Function):

    def __init__(self):
        super(KotlinFunction, self).__init__()

    def insert_data(self, cbor):
        self.insert_event(cbor)

    def get_usernames_and_feed_id(self):
        return self._handler.get_usernames_and_feed_id()

    def get_all_entries_by_feed_id(self, feed_id):
        return self._handler.get_all_entries_by_feed_id(feed_id)

    def get_all_kotlin_events(self):
        return self._handler.get_all_kotlin_events()

    def get_last_kotlin_event(self):
        return self._handler.get_last_kotlin_event()
