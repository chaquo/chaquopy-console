# not static
import database.appconn.kotlin_connection as kotlin
import eventCreator.EventCreationTool as ect
import eventCreator.Event as event
from com.chaquo.python import Python
from time import gmtime, strftime
import main

#import hmac
#import nacl.signing
#import cbor
#import binascii

#if application_action == 'post':
#    username = content[1]['username']
#    timestamp = content[1]['timestamp']
#    text = content[1]['text']
#    self.__sqlAlchemyConnector.insert_kotlin_event(feed_id=feed_id, seq_no=seq_no,
#                                                   application=application_action,
#                                                   username=username, oldusername='',
#                                                   timestamp=timestamp, text=text)
#

#timestamp=timestamp, text=text)
#
#elif application_action == 'username':
#username = content[1]['newUsername']
#oldusername = content[1]['oldUsername']
#
#timestamp = content[1]['timestamp']
#self.__sqlAlchemyConnector.insert_kotlin_event(feed_id=feed_id, seq_no=seq_no,
#application=application_action,
#username=username, oldusername=oldusername,
#timestamp=timestamp, text='')

def change_uname(new_uname):
    path = str(Python.getPlatform().getApplication().getFilesDir())
    db = kotlin.KotlinFunction()
    eg = ect.EventFactory(last_event=db.get_last_kotlin_event(), path_to_keys= path, path_to_keys_relative= False)
    timestamp = strftime("%Y-%m-%d %H:%M", gmtime())
    uname_event = eg.next_event("KotlinUI/username", {"newUsername": new_uname, "oldUsername": main.get_uname(), "timestamp": timestamp})
    db.insert_data(uname_event)


def get_uname_by_key(db, key):
    list = db.get_usernames_and_feed_id()
    uname = ""
    found = False
    for tuple in list:
        if str(tuple[1]) == str(key):
            uname = str(tuple[0])
            found = True
            break
    if not found:
        return "NOT FOUND"
    return uname


#TODO make it such that the first event gets added as soon as the account is created or reset
def insert_cbor(type, text):
    path = str(Python.getPlatform().getApplication().getFilesDir())
    db = kotlin.KotlinFunction()
    timestamp = strftime("%Y-%m-%d %H:%M", gmtime())
    public_keys = ect.EventCreationTool.get_stored_feed_ids(directory_path=path, as_strings=False, relative=False)

    #if True:
    if not public_keys:
        eg = ect.EventFactory(path_to_keys=path, path_to_keys_relative=False)
        # very first event where the user get assigned the name Anonymous
        first_event = eg.next_event('KotlinUI/username', {"newUsername": "Anonymous", "oldUsername": "", "timestamp": timestamp})
        db.insert_data(first_event)

        # re-compute public_keys, now it should contain exactly one element
        public_keys = ect.EventCreationTool.get_stored_feed_ids(directory_path=path, as_strings=False, relative=False)

    public_key = str(public_keys[0])
    list = db.get_usernames_and_feed_id()

    uname = get_uname_by_key(db, public_key)

    # this should NEVER EVER be true, EVER
    if uname == "NOT FOUND":
        uname = "Anonymous"

    eg = ect.EventFactory(last_event=db.get_last_kotlin_event(), path_to_keys= path, path_to_keys_relative= False)
    if type == "username":
        new_event = eg.next_event("KotlinUI/username", {"newUsername": uname, "oldUsername": "Anonymous", "timestamp": timestamp})
    else:
        new_event = eg.next_event("KotlinUI/post", {"username": uname, "timestamp": timestamp, "text": text})
    db.insert_data(new_event)

    #print("it worked")

# DANGER: this only works if a public key already exists
def get_my_feed_events():
    path = str(Python.getPlatform().getApplication().getFilesDir())
    public_key = ect.EventCreationTool.get_stored_feed_ids(directory_path=path, as_strings=False, relative=False)

    if not public_key:
        db = kotlin.KotlinFunction()
        timestamp = strftime("%Y-%m-%d %H:%M", gmtime())
        eg = ect.EventFactory(path_to_keys=path, path_to_keys_relative=False)
        # very first event where the user get assigned the name Anonymous
        first_event = eg.next_event('KotlinUI/username', {"newUsername": "Anonymous", "oldUsername": "", "timestamp": timestamp})
        db.insert_data(first_event)

        # re-compute public_keys, now it should contain exactly one element
        public_key = ect.EventCreationTool.get_stored_feed_ids(directory_path=path, as_strings=False, relative=False)

    public_key = public_key[0]

    db = kotlin.KotlinFunction()
    query_output = db.get_all_entries_by_feed_id(public_key)
    pretty_output = []
    uname = get_uname_by_key(db, public_key)
    for tuple in query_output:
        type = tuple[0]
        if type == "post":
            timestamp = tuple[2]
            text = tuple[1]
            t = (type, uname, timestamp, text)
        elif type == "username":
            new = tuple[1]
            old = tuple[2]
            timestamp = tuple[3]
            t = (type, new, old, timestamp)

        pretty_output.append(t)

    #print("query output")
    #print(query_output)
    #print("printing output")
    #print(pretty_output)
    return pretty_output



def get_all_feed_events():
    path = str(Python.getPlatform().getApplication().getFilesDir())
    #public_key = ect.EventCreationTool.get_stored_feed_ids(directory_path=path, as_strings=False, relative=False)[0]

    db = kotlin.KotlinFunction()
    query_output = db.get_all_kotlin_events()
    pretty_output = []
    for tuple in query_output:
        type = tuple[0]
        if type == "post":
            timestamp = tuple[2]
            text = tuple[1]
            t = (type, get_uname_by_key(db, tuple[3]), timestamp, text)
        elif type == "username":
            new = tuple[1]
            old = tuple[2]
            timestamp = tuple[3]
            t = (type, new, old, timestamp)

        pretty_output.append(t)

    #print("query output")
    #print(query_output)
    #print("printing output")
    #print(pretty_output)
    return pretty_output

