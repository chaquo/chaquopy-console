from .SqlAlchemyConnector import SqLiteDatabase
from database.functions.log import create_logger
from database.functions.Constants import SQLITE
from database.functions.Singleton import Singleton
from database.functions.Event import Event

logger = create_logger('ByteArrayHandler')


class ByteArrayHandler(metaclass=Singleton):
    __dbname = 'cborFilesDatabase'
    __tname = 'cborTable'

    def __init__(self):
        self.__sqlAlchemyConnector = SqLiteDatabase(SQLITE, dbname='cborDatabase.sqlite')
        self.__sqlAlchemyConnector.create_db_tables()

    def get_current_seq_no(self, feed_id):
        res = self.__sqlAlchemyConnector.get_current_seq_no(feed_id)
        return res

    def get_event(self, feed_id, seq_no):
        res = self.__sqlAlchemyConnector.get_event(feed_id, seq_no)
        return res

    def get_current_event_as_cbor(self, feed_id):
        res = self.__sqlAlchemyConnector.get_current_event_as_cbor(feed_id)
        return res

    def insert_byte_array(self, event_as_cbor):
        event = Event.from_cbor(event_as_cbor)
        seq_no = event.meta.seq_no
        feed_id = event.meta.feed_id.decode()
        self.__sqlAlchemyConnector.insert_byte_array(feed_id, seq_no, event_as_cbor)
