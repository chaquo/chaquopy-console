from .connection import Function

# TODO: Comment this class!

class ChatFunction(Function):

    def __init__(self):
        super(ChatFunction, self).__init__()

    def insert_chat_msg(self, cbor):
        self._handler.insert_event(cbor)

    def get_chat_since(self, application, timestamp, feed_Id, chat_id):
        return self._handler.get_event_since(application, timestamp, feed_Id, chat_id)

    def get_full_chat(self, application, feed_Id, chat_id):
        # TODO: Fix this method!
        return self._handler.get_all_chat_msgs('chat', chat_id)

    def get_last_event(self, feed_id):
        return self._handler.get_event(feed_id)
