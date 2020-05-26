from ECT_FCTRL_DB.logStore.funcs.EventCreationTool import EventFactory
from ECT_FCTRL_DB.logStore.appconn.feed_ctrl_connection import FeedCtrlConnection
from nacl.signing import SigningKey
import secrets
from .eventCreationWrapper import EventCreationWrapper
import random


class UiFunctionHandler:

    def __init__(self):
        self._fcc = FeedCtrlConnection()
        # try catch or if None??
        lastEvent = self._fcc.get_my_last_event()
        if lastEvent is not None:
            self._ecf = EventFactory(lastEvent)
            self._eventCreationWrapper = EventCreationWrapper(self._ecf)
        else:
            self._ecf = EventFactory()
            self._eventCreationWrapper = EventCreationWrapper(self._ecf)
            _firstEvent = self._eventCreationWrapper.create_MASTER()
            _secondEvent = self._eventCreationWrapper.create_radius(1)
            _thirdEvent = self._eventCreationWrapper.create_name('Anon')
            self._fcc.add_event(_firstEvent)
            self._fcc.add_event(_secondEvent)
            self._fcc.add_event(_thirdEvent)
        self._masterID = self._fcc.get_host_master_id()

    def get_host_master_id(self):
        # returns the host masterID
        return self._masterID

    def get_master_ids(self):
        # return list of masterIDs from FeedCtrlConnection
        return self._fcc.get_all_master_ids()

    def get_all_master_ids_feed_ids(self, masterID):
        # return a list of feed_ids which belong to the given masterID
        return self._fcc.get_all_master_ids_feed_ids(masterID)

    def get_radius_list(self):
        # return a list of feed_ids which are inside the radius
        return self._fcc.get_feed_ids_in_radius()

    def get_trusted(self):
        # return a list of trusted feed_ids
        return self._fcc.get_trusted(self._masterID)

    def set_trusted(self, feed_id, state):
        # sets a feed to trusted or untrusted (event)
        if state:
            new_event = self._eventCreationWrapper.create_trust(feed_id)
        else:
            new_event = self._eventCreationWrapper.create_block(feed_id)

        self._fcc.add_event(new_event)

    def get_blocked(self):
        # return a list of blocked feed_ids
        return self._fcc.get_blocked(self._masterID)

    def get_radius(self):
        # return the current radius
        return self._fcc.get_radius()

    def set_radius(self, radius):
        # sets the new radius
        # calls calcRadius() to recalculate the new Elements, which are in the radius
        self._fcc.set_feed_ids_radius(self._masterID, radius)

    def get_username(self, masterID):
        # return username from given masterID
        return self._fcc.get_username(masterID)

    def set_username(self, name):

        new_event = self._eventCreationWrapper.create_name(name)
        self._fcc.add_event(new_event)

    def get_application(self, feed_id):
        # return application name from given feed_id
        return self._fcc.get_application_name(feed_id)


"""Used for generating test data for testing the UI"""


def generate_random_feed_id():
    private_key = secrets.token_bytes(32)
    signing_key = SigningKey(private_key)
    public_key_feed_id = signing_key.verify_key.encode()
    return public_key_feed_id


"""
    This method is used to generate data for testing the UI.
    Add here if more data is needed.
"""

def generate_test_friend():
    ufh = UiFunctionHandler()
    fcc = FeedCtrlConnection()
    ecf = EventFactory()

    new_event = ecf.next_event('KotlinUI/MASTER', {})
    fcc.add_event(new_event)

    feed = generate_random_feed_id()
    timestamp = "101010"
    first_event_byApp = ecf.next_event('KotlinUI/username', {"newUsername": "Anonymous", "oldUsername": "", "timestamp": timestamp})
    fcc.add_event(first_event_byApp)

    ufh.set_trusted(feed, random.choice([True, False]))

def create_friend(name):
    ufh = UiFunctionHandler()

    fcc = FeedCtrlConnection()

    ecf2 = EventFactory()
    new_event = ecf2.next_event('MASTER/MASTER', {})
    fcc.add_event(new_event)
    trust_id3 = generate_random_feed_id()
    new_event = ecf2.next_event('MASTER/NewFeed', {'feed_id': trust_id3, 'app_name': 'KotlinUI'})
    fcc.add_event(new_event)
    new_event = ecf2.next_event('MASTER/Name', {'name': name})
    fcc.add_event(new_event)

    new_event = ecf2.next_event('KotlinUI/MASTER', {'master_feed_id': trust_id3})
    fcc.add_event(new_event)
    first_event_byApp = ecf2.next_event('KotlinUI/username', {"newUsername": "Anonymous", "oldUsername": "", "timestamp": "101010"})
    fcc.add_event(first_event_byApp)


    ufh.set_trusted(trust_id3, random.choice([True, False]))

    ufh.set_radius(2)


def generate_test_data():
    ufh = UiFunctionHandler()

    fcc = FeedCtrlConnection()
    #ecf = EventFactory()
    #new_event = ecf.next_event('MASTER/MASTER', {})
    #fcc.add_event(new_event)
    #trust_id1 = generate_random_feed_id()
    #new_event = ecf.next_event('MASTER/NewFeed', {'feed_id': trust_id1, 'app_name': 'TestApp1'})
    #fcc.add_event(new_event)
    #trust_id2 = generate_random_feed_id()
    #new_event = ecf.next_event('MASTER/NewFeed', {'feed_id': trust_id2, 'app_name': 'TestApp2'})
    #fcc.add_event(new_event)
    #new_event = ecf.next_event('MASTER/Name', {'name': 'Alice'})
    #fcc.add_event(new_event)

    ecf2 = EventFactory()
    new_event = ecf2.next_event('KotlinUI/MASTER', {})
    #new_event = ecf2.next_event('MASTER/KotlinUI', {})
    fcc.add_event(new_event)
    trust_id3 = generate_random_feed_id()
    new_event = ecf2.next_event('KotlinUI/post', {'feed_id': trust_id3, 'app_name': 'KotlinUI'})
    #####uname_event = eg.next_event("KotlinUI/username", {"newUsername": new_uname, "oldUsername": get_uname_by_key(db, get_pk()), "timestamp": timestamp})
    fcc.add_event(new_event)
    new_event = ecf2.next_event('KotlinUI/post', {'feed_id': trust_id3, 'app_name': 'KotlinUI'})
    fcc.add_event(new_event)
    new_event = ecf2.next_event('KotlinUI/post', {'name': 'Bob'})
    fcc.add_event(new_event)

    #new_event = ecf.next_event('MASTER/Trust', {'feed_id': trust_id3})

    #ufh.set_trusted(trust_id1, True)
    ufh.set_trusted(trust_id3, True)
    #ufh.set_trusted(trust_id4, True)
    #ufh.set_trusted(trust_id2, False)

    ufh.set_radius(2)
