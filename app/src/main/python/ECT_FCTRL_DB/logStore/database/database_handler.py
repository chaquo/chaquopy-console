from .cbor_handler import ByteArrayHandler, InvalidSequenceNumber
from .event_handler import EventHandler, InvalidApplicationError
from ..funcs.log import create_logger
from ..funcs.event import Event
from ..funcs.EventCreationTool import EventFactory

logger = create_logger('DatabaseHandler')
"""The database handler allows both the application as well as the network layer to access database functionality.

It is strictly meant for internal purposes and should not be directly accesses or called by any module importing this
module.
"""


class DatabaseHandler:
    """Database handler gets each created by the database connector as well as the function connector.

    It has the private fields of an byte array handler as well as an event handler to access the two databases
    accordingly.
    """

    def __init__(self):
        self.__byteArrayHandler = ByteArrayHandler()
        self.__eventHandler = EventHandler()

    def add_to_db(self, event_as_cbor, app):
        """"Add a cbor event to the two databases.
        Calls each the byte array handler as well as the event handler to insert the event in both databases
        accordingly. Gets called both by database connector as well as the function connector. Returns 1 if successful,
        otherwise -1 if any error occurred.
        If a new feed is created for an app, the first event has to contain appname/MASTER and data as {'master_feed': master_feed_id}
        """
        if app:
            event = Event.from_cbor(event_as_cbor)
            feed_id = event.meta.feed_id
            content = event.content.content
            cont_ident = content[0].split('/')
            application = cont_ident[0]
            if application != 'MASTER':
                orig_master = self.get_master_id_from_feed(feed_id)
                if orig_master is None:
                    try:
                        master_feed = content[1]['master_feed']
                    except KeyError as e:
                        logger.error(e)
                        return
                    orig_master_feed = self.__eventHandler.get_host_master_id()
                    if master_feed == orig_master_feed or orig_master_feed is None:
                        last_event = self.__eventHandler.get_my_last_event()
                        cont_ident = content[0].split('/')[0]
                        ecf = EventFactory(last_event)
                        event = ecf.next_event('MASTER/NewFeed', {'feed_id': feed_id, 'app_name': cont_ident})
                        self.add_to_db(event, False)
                        event = ecf.next_event('MASTER/Trust', {'feed_id': feed_id})
                        self.add_to_db(event, False)
                    else:
                        return -1
        try:
            self.__byteArrayHandler.insert_byte_array(event_as_cbor)
        except InvalidSequenceNumber as e:
            print("ERROR FROM DB_HANDLER")
            print("LINE 61")
            print("printing application: {}".format(application))
            logger.error(e)
            return -1
        try:
            self.__eventHandler.add_event(event_as_cbor)
        except InvalidApplicationError as e:
            print("ERROR FROM DB_HANDLER")
            print("LINE 69")
            print("printing application: {}".format(application))
            logger.error(e)
            return -1
        return 1

    def get_current_seq_no(self, feed_id):
        """"Return the current sequence number of a given feed_id, returns an integer with the currently largest
                sequence number for the given feed. Returns -1 if there is no such feed_id in the database."""
        return self.__byteArrayHandler.get_current_seq_no(feed_id)

    def get_event(self, feed_id, seq_no):
        """"Return a specific cbor event to the callee with the input feed_id and sequence number. Returns None if
                there is no such entry."""
        return self.__byteArrayHandler.get_event(feed_id, seq_no)

    def get_current_event_as_cbor(self, feed_id):
        """"Return the newest (the one with the highest sequence number) cbor event for a feed_id. Returns None if
                there is no such feed_id in the database."""
        return self.__byteArrayHandler.get_current_event_as_cbor(feed_id)

    def get_all_feed_ids(self):
        """"Return all current feed ids in the database."""
        return self.__byteArrayHandler.get_all_feed_ids()

    """Follwing are the feed control methods to be used from feed_ctrl_connection:"""

    def get_event_since(self, application, timestamp, chat_id):
        return self.__eventHandler.get_event_since(application, timestamp, chat_id)

    def get_all_chat_msgs(self, application, chat_id):
        return self.__eventHandler.get_all_events(application, chat_id)

    def get_usernames_and_feed_id(self):
        return self.__eventHandler.get_Kotlin_usernames()

    def get_all_entries_by_feed_id(self, feed_id):
        return self.__eventHandler.get_all_entries_by_feed_id(feed_id)

    def get_all_kotlin_events(self):
        return self.__eventHandler.get_all_kotlin_events()

    def get_last_kotlin_event(self):
        result = self.__eventHandler.get_last_kotlin_event()
        return self.__byteArrayHandler.get_event(result[0], result[1])

    def get_trusted(self, master_id):
        return self.__eventHandler.get_trusted(master_id)

    def get_blocked(self, master_id):
        return self.__eventHandler.get_blocked(master_id)

    def get_all_master_ids(self):
        return self.__eventHandler.get_all_master_ids()

    def get_all_master_ids_feed_ids(self, master_id):
        return self.__eventHandler.get_all_master_ids_feed_ids(master_id)

    def get_username(self, master_id):
        return self.__eventHandler.get_username(master_id)

    def get_my_last_event(self):
        return self.__eventHandler.get_my_last_event()

    def get_host_master_id(self):
        return self.__eventHandler.get_host_master_id()

    def get_radius(self):
        return self.__eventHandler.get_radius()

    def get_master_id_from_feed(self, feed_id):
        return self.__eventHandler.get_master_id_from_feed(feed_id)

    def get_application_name(self, feed_id):
        return self.__eventHandler.get_application_name(feed_id)

    def get_feed_ids_from_application_in_master_id(self, master_id, application_name):
        return self.__eventHandler.get_feed_ids_from_application_in_master_id(master_id, application_name)

    def get_feed_ids_in_radius(self):
        return self.__eventHandler.get_feed_ids_in_radius()

    def set_feed_ids_radius(self, feed_id, radius):
        return self.__eventHandler.set_feed_ids_radius(feed_id, radius)
