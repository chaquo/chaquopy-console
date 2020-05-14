from sqlalchemy import create_engine
from database.functions.Constants import SQLITE, CBORTABLE, EVENTTABLE, KOTLINTABLE
from database.functions.log import create_logger
from sqlalchemy import Table, Column, Integer, String, MetaData, Binary, func
from sqlalchemy.orm import sessionmaker, mapper

logger = create_logger('SqlAlchemyConnector')
SQLITE = 'sqlite'


class SqLiteDatabase:
    DB_ENGINE = {
        SQLITE: 'sqlite:///{DB}'
    }
    __db_engine = None

    def __init__(self, dbtype, username='', password='', dbname=''):
        dbtype = dbtype.lower()
        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)
            self.__db_engine = create_engine(engine_url)
        else:
            logger.debug("DBType is not found in DB_ENGINE")

    def create_db_tables(self):
        metadata = MetaData()
        cbor_table = Table(CBORTABLE, metadata,
                           Column('id', Integer, primary_key=True),
                           Column('feed_id', String),
                           Column('seq_no', Integer),
                           Column('event_as_cbor', Binary))
        mapper(Event, cbor_table)
        try:
            metadata.create_all(self.__db_engine)
        except Exception as e:
            logger.error(e)

    def create_chat_event_table(self):
        metadata = MetaData()
        chat_event_table = Table(EVENTTABLE, metadata,
                                 Column('id', Integer, primary_key=True),
                                 Column('feed_id', String),
                                 Column('seq_no', Integer),
                                 Column('application', String),
                                 Column('chat_id', String),
                                 Column('timestamp', Integer),
                                 Column('chatMsg', String))
        mapper(up_event, chat_event_table)
        try:
            metadata.create_all(self.__db_engine)
        except Exception as e:
            logger.error(e)

    def create_kotlin_table(self):
        metadata = MetaData()
        kotlin_event_table = Table(KOTLINTABLE, metadata,
                                   Column('id', Integer, primary_key=True),
                                   Column('feed_id', String),
                                   Column('seq_no', Integer),
                                   Column('application', String),
                                   Column('username', String),
                                   Column('timestamp', Integer),
                                   Column('text', String),
                                   Column('publickey', String))
        mapper(kotlin_event, kotlin_event_table)
        try:
            metadata.create_all(self.__db_engine)
        except Exception as e:
            logger.error(e)

    def insert_byte_array(self, feed_id, seq_no, event_as_cbor):
        session = sessionmaker(self.__db_engine)()
        obj = Event(feed_id, seq_no, event_as_cbor)
        session.add(obj)
        session.commit()
        session.expunge_all()

    def insert_event(self, feed_id, seq_no, application, chat_id, timestamp, data):
        session = sessionmaker(self.__db_engine)()
        obj = up_event(feed_id=feed_id, seq_no=seq_no, application=application, chat_id=chat_id, timestamp=timestamp,
                       data=data)
        session.add(obj)
        session.commit()
        session.expunge_all()

    def insert_kotlin_event(self, feed_id, seq_no, application, username, timestamp, text, publickey):
        session = sessionmaker(self.__db_engine)()
        obj = kotlin_event(feed_id=feed_id, seq_no=seq_no, application=application, username=username,
                           timestamp=timestamp,
                           text=text, publickey=publickey)
        session.add(obj)
        session.commit()
        session.expunge_all()

    def get_event(self, feed_id, seq_no):
        session = sessionmaker(self.__db_engine)()
        qry = session.query(Event).filter(feed_id == feed_id, Event.seq_no == seq_no)
        res = qry.first()
        if res is not None:
            return res.event_as_cbor
        else:
            return None

    def get_current_seq_no(self, feed_id):
        session = sessionmaker(self.__db_engine)()
        q = session.query(func.max(Event.seq_no)).filter(feed_id == feed_id)
        res = q.first()
        if res is not None:
            return res[0]
        else:
            return -1

    def get_current_event_as_cbor(self, feed_id):
        session = sessionmaker(self.__db_engine)()
        subqry = session.query(func.max(Event.seq_no)).filter(feed_id == feed_id)
        qry = session.query(Event).filter(feed_id == feed_id, Event.seq_no == subqry)
        res = qry.first()
        if res is not None:
            return res.event_as_cbor
        else:
            return None

    def get_all_events_since(self, application, timestamp, feed_id, chat_id):
        session = sessionmaker(self.__db_engine)()
        # subqry = session.query(up_event).filter(up_event.timestamp > timestamp,
        #                                         up_event.application == application,
        #                                         up_event.chat_id == chat_id)
        qry = session.query(up_event).filter(up_event.feed_id == feed_id)
        liste = []
        for row in qry:
            if row.timestamp > timestamp:
                if row.chat_id == chat_id:
                    if row.application == application:
                        liste.append(row.chatMsg)

        if liste is not None:
            return liste
        else:
            return None

    def get_all_event_from_application(self, application, feed_id, chat_id):
        session = sessionmaker(self.__db_engine)()
        subqry = session.query(up_event).filter(up_event.application == application,
                                                up_event.chat_id == chat_id)

        if subqry is not None:
            return subqry
        else:
            return None

    def get_all_usernames(self):
        session = sessionmaker(self.__db_engine)()
        subqry = session.query(kotlin_event)
        liste = []
        for row in subqry:
            liste.append((row.username, row.publickey))
        if liste is not None:
            return liste
        else:
            return None

    def get_all_kotlin_events(self, feed_id):
        session = sessionmaker(self.__db_engine)()
        # kotlin_event.feed_id == feed_id geht nicht
        subqry = session.query(kotlin_event).filter(feed_id == feed_id)
        liste = []
        for row in subqry:
            liste.append((row.text, row.username, row.publickey.hex(), row.timestamp))

        if liste is not None:
            return liste
        else:
            return None

    def get_all_entries_by_publickey(self, publicKey):
        session = sessionmaker(self.__db_engine)()
        subqry = session.query(kotlin_event).filter(kotlin_event.publickey == publicKey)
        liste = []
        for row in subqry:
            liste.append((row.text, row.username, row.publickey, row.timestamp))

        if liste is not None:
            return liste
        else:
            return None


    def get_last_kotlin_event(self):
        session = sessionmaker(self.__db_engine)()
        subqry = session.query(kotlin_event).order_by(kotlin_event.id.desc()).first()

        result = (subqry.text, subqry.username, subqry.publickey, subqry.timestamp)
        return result



class Event(object):
    def __init__(self, feed_id, seq_no, event_as_cbor):
        self.feed_id = feed_id
        self.seq_no = seq_no
        self.event_as_cbor = event_as_cbor


class up_event(object):
    def __init__(self, feed_id, seq_no, application, chat_id, timestamp, data):
        self.feed_id = feed_id
        self.seq_no = seq_no
        self.application = application
        self.chat_id = chat_id
        self.timestamp = timestamp
        self.chatMsg = data


class kotlin_event(object):
    def __init__(self, feed_id, seq_no, application, username, timestamp, text, publickey):
        self.feed_id = feed_id
        self.seq_no = seq_no
        self.application = application
        self.username = username
        self.timestamp = timestamp
        self.text = text
        self.publickey = publickey
