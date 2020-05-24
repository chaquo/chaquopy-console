from .connection import Function


class ChatFunction(Function):
    """Connection to the group chat to insert and output the chat elements"""

    def __init__(self):
        super(ChatFunction, self).__init__()

    def insert_chat_msg(self, cbor):
        """adds a new chat element as cbor

                Tested and works!"""
        self.insert_event(cbor)

    def get_chat_since(self, timestamp, chat_id):
        """returns all elements which have a higher timestamp and the correct chat id

                Tested and works!"""
        return self._handler.get_event_since('chat', timestamp, chat_id)

    def get_full_chat(self, chat_id):
        """returns all chat elements with the correct chat id

                Tested and works!"""
        return self._handler.get_all_chat_msgs('chat', chat_id)
