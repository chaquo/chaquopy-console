from ECT_FCTRL_DB.logStore.funcs.singleton import Singleton
from ECT_FCTRL_DB.logStore.database.sql_alchemy_connector import SqLiteDatabase
from ECT_FCTRL_DB.logStore.funcs.constants import SQLITE
from ECT_FCTRL_DB.logStore.funcs.event import Event
from ECT_FCTRL_DB.logStore.funcs.log import create_logger
from os.path import join
from com.chaquo.python import Python

logger = create_logger('EventHandler')


class EventHandler(metaclass=Singleton):

    def __init__(self):
        DB_PATH = str(Python.getPlatform().getApplication().getFilesDir())
        DB_PATH = join(DB_PATH, "KotlinDB.sqlite")
        self.sqlAlchemyConnector = SqLiteDatabase(SQLITE, dbname=DB_PATH)
        self.sqlAlchemyConnector.create_chat_event_table()
        self.sqlAlchemyConnector.create_kotlin_table()
        self.sqlAlchemyConnector.create_master_table()


    def add_event(self, event_as_cbor):
        try:
            event = Event.from_cbor(event_as_cbor)
            seq_no = event.meta.seq_no
            feed_id = event.meta.feed_id
            content = event.content.content

            cont_ident = content[0].split('/')
            application = cont_ident[0]
            application_action = cont_ident[1]

            if application == 'chat':
                if application_action == 'MASTER':
                    return
                chatMsg = content[1]['messagekey']
                chat_id = content[1]['chat_id']
                timestamp = content[1]['timestampkey']

                self.sqlAlchemyConnector.insert_event(feed_id=feed_id, seq_no=seq_no, application=application,
                                                        chat_id=chat_id,
                                                        timestamp=timestamp, data=chatMsg)

            elif application == 'KotlinUI':
                if application_action == 'post':
                    username = content[1]['username']
                    timestamp = content[1]['timestamp']
                    text = content[1]['text']
                    self.sqlAlchemyConnector.insert_kotlin_event(feed_id=feed_id, seq_no=seq_no,
                                                                   application=application_action,
                                                                   username=username, oldusername='',
                                                                   timestamp=timestamp, text=text)

                elif application_action == 'username':
                    username = content[1]['newUsername']
                    oldusername = content[1]['oldUsername']

                    timestamp = content[1]['timestamp']
                    self.sqlAlchemyConnector.insert_kotlin_event(feed_id=feed_id, seq_no=seq_no,
                                                                   application=application_action,
                                                                   username=username, oldusername=oldusername,
                                                                   timestamp=timestamp, text='')
            elif application == 'MASTER':
                self.master_handler(seq_no, feed_id, content, cont_ident, event_as_cbor)

            else:
                raise InvalidApplicationError('Invalid application called %s' % application)
        except KeyError as e:
            logger.error(e)
            return -1

    def get_event_since(self, application, timestamp, chat_id):
        return self.sqlAlchemyConnector.get_all_events_since(application, timestamp, chat_id)

    def get_all_events(self, application, chat_id):
        return self.sqlAlchemyConnector.get_all_event_with_chat_id(application, chat_id)

    def get_Kotlin_usernames(self):
        return self.sqlAlchemyConnector.get_all_usernames()

    def get_all_kotlin_events(self):
        return self.sqlAlchemyConnector.get_all_kotlin_events()

    def get_all_entries_by_feed_id(self, feed_id):
        return self.sqlAlchemyConnector.get_all_entries_by_feed_id(feed_id)

    def get_last_kotlin_event(self):
        return self.sqlAlchemyConnector.get_last_kotlin_event()

    """"Structure of insert_master_event:
    insert_master_event(self, master, feed_id, app_feed_id, trust_feed_id, seq_no, trust, name, radius, event_as_cbor, app_name)"""

    def master_handler(self, seq_no, feed_id, content, cont_ident, event_as_cbor):
        """Handle master events and insert the events corresponding to their definition:"""
        event = cont_ident[1]
        if event == 'MASTER':
            self.sqlAlchemyConnector.insert_master_event(True, feed_id, None, None, seq_no, None, None, 0,
                                                           event_as_cbor, None)
        elif event == 'Trust':
            self.sqlAlchemyConnector.insert_master_event(False, feed_id, None, content[1]['feed_id'], seq_no, True,
                                                           None, None, event_as_cbor, None)
            from ECT_FCTRL_DB.feedCtrl import radius
            r = radius.Radius()
            r.calculate_radius()
        elif event == 'Block':
            self.sqlAlchemyConnector.insert_master_event(False, feed_id, None, content[1]['feed_id'], seq_no, False,
                                                           None, None, event_as_cbor, None)
            from ECT_FCTRL_DB.feedCtrl import radius
            r = radius.Radius()
            r.calculate_radius()
        elif event == 'Name':
            self.sqlAlchemyConnector.insert_master_event(False, feed_id, None, None, seq_no, None,
                                                           content[1]['name'], None, event_as_cbor, None)
        elif event == 'NewFeed':
            self.sqlAlchemyConnector.insert_master_event(False, feed_id, content[1]['feed_id'], None, seq_no, True,
                                                           None, None, event_as_cbor, content[1]['app_name'])
        elif event == 'Radius':
            self.sqlAlchemyConnector.insert_master_event(False, feed_id, None, None, seq_no,
                                                           None, None, content[1]['radius'], event_as_cbor, None)
        else:
            raise InvalidApplicationError('Invalid action called %s' % event)

    """"Following come the feed control mechanisms used by database_handler:"""

    def get_trusted(self, master_id):
        return self.sqlAlchemyConnector.get_trusted(master_id)

    def get_blocked(self, master_id):
        return self.sqlAlchemyConnector.get_blocked(master_id)

    def get_all_master_ids(self):
        return self.sqlAlchemyConnector.get_all_master_ids()

    def get_all_master_ids_feed_ids(self, master_id):
        return self.sqlAlchemyConnector.get_all_master_ids_feed_ids(master_id)

    def get_username(self, master_id):
        return self.sqlAlchemyConnector.get_username(master_id)

    def get_my_last_event(self):
        return self.sqlAlchemyConnector.get_my_last_event()

    def get_host_master_id(self):
        return self.sqlAlchemyConnector.get_host_master_id()

    def get_radius(self):
        return self.sqlAlchemyConnector.get_radius()

    def get_master_id_from_feed(self, feed_id):
        return self.sqlAlchemyConnector.get_master_id_from_feed(feed_id)

    def get_application_name(self, feed_id):
        return self.sqlAlchemyConnector.get_application_name(feed_id)

    def get_feed_ids_from_application_in_master_id(self, master_id, application_name):
        return self.sqlAlchemyConnector.get_feed_ids_from_application_in_master_id(master_id, application_name)

    def get_feed_ids_in_radius(self):
        return self.sqlAlchemyConnector.get_feed_ids_in_radius()

    def set_feed_ids_radius(self, feed_id, radius):
        return self.sqlAlchemyConnector.set_feed_ids_radius(feed_id, radius)


class InvalidApplicationError(Exception):
    def __init__(self, message):
        super(InvalidApplicationError, self).__init__(message)
