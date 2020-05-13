from database.functions.Singleton import Singleton
from .SqlAlchemyConnector import SqLiteDatabase
from database.functions.Constants import SQLITE
from database.functions.Event import Event


class EventHandler(metaclass=Singleton):

    def __init__(self):
        self.__sqlAlchemyConnector = SqLiteDatabase(SQLITE, dbname='eventDatabase.sqlite')
        self.__sqlAlchemyConnector.create_chat_event_table()
        self.__sqlAlchemyConnector.create_kotlin_table()

    def init_event_table(self):
        return False

    def add_event(self, event_as_cbor):
        event = Event.from_cbor(event_as_cbor)
        seq_no = event.meta.seq_no
        feed_id = event.meta.feed_id.decode()
        content = event.content.content

        temp = content[0].split('/')
        application = temp[0]

        if application == 'chat':
            chatMsg = content[1]['messagekey']
            chat_id = content[1]['chat_id']
            timestamp = content[1]['timestampkey']

            self.__sqlAlchemyConnector.insert_event(feed_id=feed_id, seq_no=seq_no, application=application,
                                                    chat_id=chat_id,
                                                    timestamp=timestamp, data=chatMsg)
        if application == 'KotlinUI':
            username = content[1]['username']
            publickey = content[1]['publickey']
            timestamp = content[1]['timestamp']
            text = content[1]['text']
            self.__sqlAlchemyConnector.insert_kotlin_event(feed_id=feed_id, seq_no=seq_no, application=application,
                                                           username=username,
                                                           timestamp=timestamp, text=text, publickey=publickey)

    def get_event_since(self, application, timestamp, feed_id, chat_id):
        return self.__sqlAlchemyConnector.get_all_events_since(application, timestamp, feed_id, chat_id)

    def get_all_events(self, application, feed_id, chat_id):
        return self.__sqlAlchemyConnector.get_all_event_from_application(application, feed_id, chat_id)

    def get_Kotlin_usernames(self):
        return self.__sqlAlchemyConnector.get_all_usernames()

    def get_all_kotlin_events(self, feed_id):
        return self.__sqlAlchemyConnector.get_all_kotlin_events(feed_id=feed_id)

    def get_all_entries_by_publickey(self, publicKey):
        return self.__sqlAlchemyConnector.get_all_entries_by_publickey(publicKey)



    def create_table_for_feed(self, feedId):
        pass

    def read_data_from_event(self, byteArray):
        pass
