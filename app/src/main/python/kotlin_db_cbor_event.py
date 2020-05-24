# not static
import ECT_FCTRL_DB.logStore.appconn.kotlin_connection as kotlin
import ECT_FCTRL_DB.eventCreationTool.EventCreationTool as ect
import ECT_FCTRL_DB.feed_control as feedCTRL
import ECT_FCTRL_DB.eventCreationTool.Event as Event
from com.chaquo.python import Python
from time import gmtime, strftime
import main


def start():
    feedCTRL.cli('')

def change_uname(new_uname):
    path = str(Python.getPlatform().getApplication().getFilesDir())
    db = kotlin.KotlinFunction()
    eg = ect.EventFactory(last_event=db.get_last_kotlin_event(), path_to_keys= path, path_to_keys_relative= False)
    timestamp = strftime("%Y-%m-%d %H:%M", gmtime())
    uname_event = eg.next_event("KotlinUI/username", {"newUsername": new_uname, "oldUsername": main.get_uname(), "timestamp": timestamp})
    db.insert_data(uname_event)

def get_all_usernames():
    db = kotlin.KotlinFunction()
    list = []
    print(db.get_usernames_and_feed_id())
    for tuple in db.get_usernames_and_feed_id():
        name, key = tuple
        list.append(name)
    return list

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
    db.get_host_master_id()
    timestamp = strftime("%Y-%m-%d %H:%M", gmtime())
    public_keys = ect.EventCreationTool.get_stored_feed_ids(directory_path=path, as_strings=False, relative=False)

    #if True:
    if not public_keys:
        eg = ect.EventFactory(path_to_keys=path, path_to_keys_relative=False)
        # VERY first event (for feedCTRL)
        first_event = eg.first_event('KotlinUI', db.get_host_master_id())
        db.insert_data(first_event)
        # first event (INSERTED BY user) where the user get assigned the name Anonymous
        first_event_byApp = eg.next_event('KotlinUI/username', {"newUsername": "Anonymous", "oldUsername": "", "timestamp": timestamp})
        db.insert_data(first_event_byApp)

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
        # VERY first event (for feedCTRL)
        first_event = eg.first_event('KotlinUI', db.get_host_master_id())
        db.insert_data(first_event)
        # first event (INSERTED BY user) where the user get assigned the name Anonymous
        first_event_byApp = eg.next_event('KotlinUI/username', {"newUsername": "Anonymous", "oldUsername": "", "timestamp": timestamp})
        db.insert_data(first_event_byApp)

        # re-compute public_keys, now it should contain exactly one element
        public_key = ect.EventCreationTool.get_stored_feed_ids(directory_path=path, as_strings=False, relative=False)

    public_key = public_key[0]

    db = kotlin.KotlinFunction()
    print("printing master id")
    print(db.get_host_master_id().hex())
    print("----------------------------------------------------------------")
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

    print('printing last kotlin event-------------------')
    event = Event.Event.from_cbor(db.get_last_kotlin_event())
    print(event.meta.seq_no)
    print('------------------------------------------------------------------------')
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

