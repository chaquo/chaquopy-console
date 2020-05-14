import hashlib
import nacl.signing
import nacl.encoding
import nacl.exceptions
from eventCreator import EventCreationTool
from eventCreator import Event
from com.chaquo.python import Python
from os.path import join
from database.upConnection import Function
from database.database import EventHandler

# LOOK AT THE README THIS FILE IS GOING TO BE THE TESTFILE LATER ON

FILES_DIR = str(Python.getPlatform().getApplication().getFilesDir())

def verify_event(event, previous_event=None):
    if previous_event is not None:
        previous_hash_type, hash_of_previous = event.meta.hash_of_prev
        prev_meta_as_cbor = previous_event.meta.get_as_cbor()
        if previous_event.meta.feed_id != event.meta.feed_id:
            return False
        if event.meta.seq_no - 1 != previous_event.meta.seq_no:
            return False
        if not (previous_hash_type == 0 and hashlib.sha256(prev_meta_as_cbor).digest() == hash_of_previous):
            return False

    content_hash_type, hash_of_content = event.meta.hash_of_content
    signature_identifier = event.meta.signature_info
    signature = event.signature

    content = event.content.get_as_cbor()
    meta_as_cbor = event.meta.get_as_cbor()

    if not (content_hash_type == 0 and hashlib.sha256(content).digest() == hash_of_content):
        return False

    if signature_identifier == 0:
        verification_key = nacl.signing.VerifyKey(event.meta.feed_id)
        try:
            verification_key.verify(meta_as_cbor, signature)
        except nacl.exceptions.BadSignatureError:
            return False
    #elif signature_identifier == 1:
    #    secret_key = DB.get_secret_hmac_key(event.meta.feed_id)
    #    if secret_key is None:
    #        return False
    #    generated_signature = hmac.new(secret_key, meta_as_cbor, hashlib.sha256).hexdigest()
    #    if signature != generated_signature:
    #        return False
    else:
        return False

    return True


def main():
    eg = EventCreationTool.EventFactory(path_to_keys=str(Python.getPlatform().getApplication().getFilesDir()), path_to_keys_relative=False)
    first_event = eg.next_event('KotlinUI/post', {'username' : "Bob", 'publickey' : eg.get_feed_id(),
                                                  'timestamp' : 1, 'text' : "HELOOOO"})
    second_event = eg.next_event('KotlinUI/post', {'username' : "Bob", 'publickey' : eg.get_feed_id(),
                                                   'timestamp' : 2, 'text' : "HELOOOO"})
    third_event = eg.next_event('KotlinUI/post', {'username' : "Bob", 'publickey' : eg.get_feed_id(),
                                                  'timestamp' : 3, 'text' : "HELOOOO"})
    first_event_object = Event.Event.from_cbor(first_event)
    #print(first_event_object.meta.seq_no)
    second_event_object = Event.Event.from_cbor(second_event)
    #print(second_event_object.meta.seq_no)
    third_event_object = Event.Event.from_cbor(third_event)
    #print(third_event_object.meta.seq_no)
    #egt = EventCreationTool.EventFactory(path_to_keys=FILES_DIR, path_to_keys_relative=False, last_event=third_event)
    #fourth_event = egt.next_event('KotlinUI/post', {'username' : "Bob", 'publickey' : eg.get_feed_id(),
    #                                                'timestamp' : 4, 'text' : "HELOOOO"})
    #fourth_event_object = Event.Event.from_cbor(fourth_event)
    #print(fourth_event_object.meta.seq_no)

    event = Event.Event.from_cbor(first_event)
    seq_no = event.meta.seq_no
    #feed_id = event.meta.feed_id.decode()
    content = event.content.content
    #print(seq_no)
    #print(feed_id)
    #print(content)


    print("--------------------------------------------------")
    DB_ABSOLUTE_PATH = join(FILES_DIR, "eventDatabase.sqlite")
    connector = EventHandler.EventHandler(name=DB_ABSOLUTE_PATH)
    connector.add_event(first_event)
    connector.add_event(second_event)
    connector.add_event(third_event)
    #connector.add_event(fourth_event)
    s = connector.get_all_kotlin_events(eg.get_feed_id())
    #print(s)